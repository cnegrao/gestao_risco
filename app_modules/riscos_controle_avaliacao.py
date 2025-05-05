import streamlit as st
import pandas as pd
from pathlib import Path
from database_utils import run_select, run_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


def riscos_controle_avaliacao():
    """
    Tela de Controle de Controles por Evento de Risco.
    Gerencia inserção, edição e remoção de controles vinculados a um risco.
    """
    # Injeção de CSS
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

    # Cabeçalho
    st.title("Controle de Controles por Evento de Risco")
    st.markdown("_Associação e gestão dos controles existentes para cada risco_")
    st.markdown("---")

    # 1️⃣ Seleção de risco
    riscos_df = run_select(
        "SELECT id_risco, nome_risco FROM tb_riscos ORDER BY id_risco;")
    if riscos_df.empty:
        st.error("Nenhum risco cadastrado.")
        return
    riscos_df['label'] = riscos_df['id_risco'].astype(
        str) + ' – ' + riscos_df['nome_risco']
    escolha = st.selectbox("Selecionar Risco:",
                           riscos_df['label'], key='rca_risco')
    id_risco = int(escolha.split(' – ')[0])

    # 2️⃣ Carrega domínios
    situ_df = run_select(
        "SELECT id_situacao_controle, descricao FROM tb_situacao_controle ORDER BY id_situacao_controle;"
    )
    exec_df = run_select(
        "SELECT id_execucao_controle, descricao FROM tb_execucao_controle ORDER BY id_execucao_controle;"
    )
    situ_map = dict(zip(situ_df['descricao'], situ_df['id_situacao_controle']))
    exec_map = dict(zip(exec_df['descricao'], exec_df['id_execucao_controle']))

    # 3️⃣ Layout
    col_form, col_grid = st.columns([1, 2], gap='large')

    # 4️⃣ Formulário de inserção/edição
    with col_form:
        st.subheader("➕ Novo / ✏️ Editar Controle")
        if 'is_new' not in st.session_state:
            st.session_state.is_new = True
        st.session_state.is_new = st.checkbox(
            "Novo Controle", st.session_state.is_new, key='rca_new')

        # Normaliza seleção para edição
        raw = st.session_state.get('grid_state', {}).get('selected_rows')
        if isinstance(raw, pd.DataFrame):
            sel_list = raw.to_dict('records')
        elif isinstance(raw, list):
            sel_list = raw
        else:
            sel_list = []
        selected = sel_list[0] if sel_list and not st.session_state.is_new else None

        with st.expander("Formulário de Controle", expanded=True):
            with st.form(key='rca_form'):
                desc = st.text_area(
                    "Descrição do Controle:",
                    value='' if selected is None else selected['descricao_controle'],
                    height=120
                )
                situ_opts = situ_df['descricao'].tolist()
                situ_idx = situ_opts.index(
                    selected['situacao_controle']) if selected else 0
                situ = st.selectbox("Situação:", situ_opts, index=situ_idx)

                exec_opts = exec_df['descricao'].tolist()
                exec_idx = exec_opts.index(
                    selected['execucao_controle']) if selected else 0
                execu = st.selectbox("Execução:", exec_opts, index=exec_idx)

                submitted = st.form_submit_button("Salvar")
                if submitted:
                    if not desc.strip():
                        st.error("Descrição obrigatória.")
                    else:
                        if st.session_state.is_new:
                            run_query(
                                "INSERT INTO tb_risco_controle (id_risco, descricao_controle, id_situacao_controle, id_execucao_controle, usuario_criacao) VALUES (%s,%s,%s,%s,%s);",
                                (id_risco, desc.strip(), situ_map[situ], exec_map[execu], st.session_state.get(
                                    'current_user', ''))
                            )
                            st.success("Controle adicionado com sucesso.")
                        else:
                            run_query(
                                "UPDATE tb_risco_controle SET descricao_controle=%s, id_situacao_controle=%s, id_execucao_controle=%s WHERE id_controle=%s;",
                                (desc.strip(
                                ), situ_map[situ], exec_map[execu], selected['id_controle'])
                            )
                            st.success("Controle atualizado com sucesso.")
                        # Limpa estado para refresh do grid
                        st.session_state.is_new = True
                        if 'grid_state' in st.session_state:
                            del st.session_state['grid_state']
                        # Refresh
                        if hasattr(st, 'experimental_rerun'):
                            st.experimental_rerun()

    # 5️⃣ Grid de controles
    with col_grid:
        st.subheader("Controles Existentes")
        df_controls = run_select(
            """
            SELECT rc.id_controle, rc.descricao_controle,
                   sc.descricao AS situacao_controle,
                   ec.descricao AS execucao_controle
            FROM tb_risco_controle rc
             JOIN tb_situacao_controle sc ON rc.id_situacao_controle = sc.id_situacao_controle
             JOIN tb_execucao_controle ec ON rc.id_execucao_controle = ec.id_execucao_controle
            WHERE rc.id_risco = %s
            ORDER BY rc.data_criacao DESC;
            """, (id_risco,)
        )
        gb = GridOptionsBuilder.from_dataframe(df_controls)
        gb.configure_selection('single', use_checkbox=True)
        gb.configure_column('id_controle', editable=False)
        opts = gb.build()
        grid_resp = AgGrid(
            df_controls,
            gridOptions=opts,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT,
            theme='ag-theme-alpine-dark',
            height=350,
            fit_columns_on_grid_load=True
        )
        st.session_state.grid_state = grid_resp

        # Normaliza seleção para remoção
        raw2 = grid_resp.get('selected_rows')
        if isinstance(raw2, pd.DataFrame):
            sel_list2 = raw2.to_dict('records')
        elif isinstance(raw2, list):
            sel_list2 = raw2
        else:
            sel_list2 = []

        if st.button("🗑️ Remover Selecionado", key='rm_ctrl'):
            if not sel_list2:
                st.warning("Selecione um registro para remover.")
            else:
                run_query("DELETE FROM tb_risco_controle WHERE id_controle=%s;",
                          (sel_list2[0]['id_controle'],))
                st.success("Controle removido com sucesso.")
                # limpa estado e recarrega
                if 'grid_state' in st.session_state:
                    del st.session_state['grid_state']
                if hasattr(st, 'experimental_rerun'):
                    st.experimental_rerun()


# Execução direta
if __name__ == '__main__':
    riscos_controle_avaliacao()
