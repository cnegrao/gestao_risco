import streamlit as st
import pandas as pd
from pathlib import Path
from database_utils import run_select, run_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import plotly.graph_objects as go

# ----------------------
# Configurações de estilo Sankey e CSS
# ----------------------
NODE_PAD = 30           # Espaçamento interno dos nós
NODE_THICKNESS = 16     # Espessura dos nós
NODE_LINE_WIDTH = 1     # Borda dos nós
LINK_OPACITY = 0.5      # Opacidade dos links
LINK_LINE_WIDTH = 1     # Borda dos links


def main():
    """
    Tela de Controle de Controles por Evento de Risco
    Seleciona um risco e gerencia controles associados.
    """
    # Carrega CSS customizado (assets/style.css)
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # Cabeçalho
    st.title("Controle de Controles por Evento de Risco")
    st.markdown(
        "_Associação e gestão dos controles existentes para cada risco_\n---")

    # 1) Recupera riscos (ID e nome) no formato "ID - Nome"
    riscos_df = run_select(
        "SELECT id_risco, nome_risco FROM tb_riscos ORDER BY id_risco"
    )
    if riscos_df.empty:
        st.error("Nenhum risco cadastrado.\nVerifique a base de dados.")
        return
    # Concatena ID e nome em label
    riscos_df['label'] = riscos_df['id_risco'].astype(
        str) + ' - ' + riscos_df['nome_risco']
    escolhido = st.selectbox("Escolha o Risco:", riscos_df['label'])
    # Extrai id_risco do label
    id_risco = int(escolhido.split(' - ')[0])

    # 2) Carrega domínios de situação e execução de controle
    situ_df = run_select(
        "SELECT id_situacao_controle, descricao FROM tb_situacao_controle ORDER BY id_situacao_controle")
    exec_df = run_select(
        "SELECT id_execucao_controle, descricao FROM tb_execucao_controle ORDER BY id_execucao_controle")
    situ_map = dict(zip(situ_df['descricao'], situ_df['id_situacao_controle']))
    exec_map = dict(zip(exec_df['descricao'], exec_df['id_execucao_controle']))

    # 3) Consulta controles já existentes para o risco
    controles_df = run_select(
        """
        SELECT rc.id_controle,
               rc.descricao_controle,
               sc.descricao AS situacao_controle,
               ec.descricao AS execucao_controle
        FROM tb_risco_controle rc
        JOIN tb_situacao_controle sc ON rc.id_situacao_controle = sc.id_situacao_controle
        JOIN tb_execucao_controle ec ON rc.id_execucao_controle = ec.id_execucao_controle
        WHERE rc.id_risco = %s
        ORDER BY rc.data_criacao DESC
        """, (id_risco,)
    )

    # Layout: duas colunas
    col1, col2 = st.columns([1, 2])

    # Coluna esquerda: Formulário de Adição/Edição
    with col1:
        st.subheader("➕ Novo / ✏️ Editar Controle")
        # Checkbox para novo
        is_new = st.checkbox("Novo Controle", value=True)
        selected = None
        # Se não for novo, obtém seleção da grid
        if not is_new and 'grid_resp' in st.session_state:
            rows = st.session_state.grid_resp.get('selected_rows', [])
            if rows:
                selected = rows[0]
        # Formulário
        with st.form(key='form_controle'):
            desc = st.text_area(
                'Descrição do Controle',
                value='' if is_new or not selected else selected['descricao_controle'],
                height=80
            )
            situ_choices = situ_df['descricao'].tolist()
            situ_default = situ_choices[0] if is_new or not selected else selected['situacao_controle']
            situ = st.selectbox(
                'Situação do Controle', situ_choices, index=situ_choices.index(situ_default))
            exec_choices = exec_df['descricao'].tolist()
            exec_default = exec_choices[0] if is_new or not selected else selected['execucao_controle']
            execu = st.selectbox(
                'Execução do Controle', exec_choices, index=exec_choices.index(exec_default))
            btn_label = 'Salvar Novo Controle' if is_new else 'Atualizar Controle'
            if st.form_submit_button(btn_label):
                if not desc.strip():
                    st.error('A descrição do controle é obrigatória.')
                else:
                    if is_new:
                        run_query(
                            "INSERT INTO tb_risco_controle (id_risco, descricao_controle, id_situacao_controle, id_execucao_controle, usuario_criacao) VALUES (%s,%s,%s,%s,%s)",
                            (id_risco, desc.strip(), situ_map[situ], exec_map[execu], st.session_state.get(
                                'current_user', ''))
                        )
                        st.success('Controle adicionado com sucesso.')
                    else:
                        run_query(
                            "UPDATE tb_risco_controle SET descricao_controle=%s, id_situacao_controle=%s, id_execucao_controle=%s WHERE id_controle=%s",
                            (desc.strip(
                            ), situ_map[situ], exec_map[execu], selected['id_controle'])
                        )
                        st.success('Controle atualizado com sucesso.')
                    st.experimental_rerun()

    # Coluna direita: Grade de Controles
    with col2:
        st.subheader('Controles Existentes')
        if controles_df.empty:
            st.info('Nenhum controle cadastrado para este risco.')
        else:
            gb = GridOptionsBuilder.from_dataframe(controles_df)
            gb.configure_selection('single', use_checkbox=True)
            gb.configure_column('id_controle', editable=False)
            grid_opts = gb.build()
            grid_resp = AgGrid(
                controles_df,
                gridOptions=grid_opts,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                data_return_mode=DataReturnMode.AS_INPUT,
                theme='ag-theme-alpine-dark',
                height=300,
                fit_columns_on_grid_load=True
            )
            st.session_state.grid_resp = grid_resp
            # Botão Remover
            if st.button('🗑️ Remover Controle Selecionado'):
                rows = grid_resp.get('selected_rows', [])
                if not rows:
                    st.warning('Selecione um controle para remover.')
                else:
                    run_query(
                        'DELETE FROM tb_risco_controle WHERE id_controle=%s', (rows[0]['id_controle'],))
                    st.success('Controle removido com sucesso.')
                    st.experimental_rerun()


if __name__ == '__main__':
    main()
