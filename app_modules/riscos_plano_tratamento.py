import streamlit as st
import pandas as pd
from pathlib import Path
from database_utils import run_select, run_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import datetime


def riscos_plano_tratamento():
    """
    Fase 5 – Plano de Tratamento de Riscos
    Permite ao gestor criar, editar e remover ações de tratamento associadas a um risco.
    Segue o padrão visual e CSS global da aplicação.
    """
    # Injeção de CSS global
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

    # Cabeçalho da página
    st.title("Fase 5 – Plano de Tratamento de Riscos")
    st.markdown(
        "_Defina ações, responsáveis e prazos para mitigar riscos identificados._")
    st.markdown("---")

    # 1️⃣ Seleção de Empresa e Risco
    emp_df = run_select(
        "SELECT id_empresa, nome_empresa FROM tb_empresas ORDER BY nome_empresa;")
    if emp_df.empty:
        st.error("Nenhuma empresa cadastrada.")
        return
    emp_df['label'] = emp_df['id_empresa'].astype(
        str) + ' – ' + emp_df['nome_empresa']
    escolha_emp = st.selectbox(
        "Selecione a Empresa:", emp_df['label'], key='pt_empresa')
    id_empresa = int(escolha_emp.split(' – ')[0])

    riscos_df = run_select(
        "SELECT id_risco, nome_risco FROM tb_riscos WHERE id_empresa = %s ORDER BY id_risco;",
        (id_empresa,)
    )
    if riscos_df.empty:
        st.info("Nenhum risco cadastrado para esta empresa.")
        return
    riscos_df['label'] = riscos_df['id_risco'].astype(
        str) + ' – ' + riscos_df['nome_risco']
    escolha_risco = st.selectbox(
        "Selecione o Risco:", riscos_df['label'], key='pt_risco')
    id_risco = int(escolha_risco.split(' – ')[0])

    st.markdown("---")
    # Carrega domínios
    tipo_df = run_select(
        "SELECT id_tipo_tratamento, descricao FROM tb_tipo_tratamento ORDER BY id_tipo_tratamento;")
    status_df = run_select(
        "SELECT id_status, descricao FROM tb_status_plano ORDER BY id_status;")
    area_df = run_select(
        "SELECT id_area, nome_area FROM tb_area_responsavel ORDER BY id_area;")
    tipo_df['id_tipo_tratamento'] = tipo_df['id_tipo_tratamento'].astype(int)
    status_df['id_status'] = status_df['id_status'].astype(int)
    area_df['id_area'] = area_df['id_area'].astype(int)

    # Layout em duas colunas: formulário e grid
    col_form, col_grid = st.columns([1, 2], gap='large')

    # 2️⃣ Formulário de criação/edição
    with col_form:
        st.subheader("📋 Nova/Editar Ação de Tratamento")
        raw = st.session_state.get('pt_grid', {}).get('selected_rows')
        sel_list = raw.to_dict('records') if isinstance(
            raw, pd.DataFrame) else raw or []
        is_edit = st.checkbox("Modo Edição", key='pt_edit')
        selected = sel_list[0] if is_edit and sel_list else None

        with st.form(key='pt_form'):
            # Tipo de Tratamento
            tipo_opts = tipo_df['descricao'].tolist()
            if selected:
                default_tipo = int(selected.get(
                    'id_tipo_tratamento', tipo_df.at[0, 'id_tipo_tratamento']))
                default_idx = tipo_df.index[tipo_df['id_tipo_tratamento'] == default_tipo].tolist()[
                    0]
            else:
                default_idx = 0
            escolha_tipo = st.selectbox(
                "Tipo de Tratamento:", tipo_opts, index=default_idx, key='pt_tipo')
            id_tipo = int(tipo_df.at[default_idx, 'id_tipo_tratamento'])

            # Status
            status_opts = status_df['descricao'].tolist()
            if selected:
                default_status = int(selected.get(
                    'id_status', status_df.at[0, 'id_status']))
                status_idx = status_df.index[status_df['id_status'] == default_status].tolist()[
                    0]
            else:
                status_idx = 0
            escolha_status = st.selectbox(
                "Status:", status_opts, index=status_idx, key='pt_status')
            id_status = int(status_df.at[status_idx, 'id_status'])

            # Área Responsável
            area_opts = area_df['nome_area'].tolist()
            if selected:
                default_area = int(selected.get(
                    'id_area_responsavel', area_df.at[0, 'id_area']))
                area_idx = area_df.index[area_df['id_area'] == default_area].tolist()[
                    0]
            else:
                area_idx = 0
            escolha_area = st.selectbox(
                "Área Responsável:", area_opts, index=area_idx, key='pt_area')
            id_area = int(area_df.at[area_idx, 'id_area'])

            # Campos adicionais
            descricao = st.text_area("Descrição da Ação", value=selected.get(
                'descricao_acao', '') if selected else "")
            hoje = datetime.date.today()
            data_inicio = st.date_input("Data de Início", value=hoje if not selected else pd.to_datetime(
                selected['data_inicio']).date())
            prazo = st.date_input("Prazo Limite", value=hoje if not selected else pd.to_datetime(
                selected['data_prazo_limite']).date())
            termino = st.date_input("Data de Conclusão (opcional)", value=None if not selected or pd.isna(
                selected.get('data_real_termino')) else pd.to_datetime(selected['data_real_termino']).date())
            comentarios = st.text_area("Comentários", value=selected.get(
                'comentarios', '') if selected else "")

            if st.form_submit_button("Salvar Ação"):
                try:
                    if is_edit and selected:
                        run_query(
                            "UPDATE tb_plano_tratamento SET id_tipo_tratamento=%s, descricao_acao=%s, id_status=%s, id_area_responsavel=%s, data_inicio=%s, data_prazo_limite=%s, data_real_termino=%s, comentarios=%s WHERE id_plano=%s;",
                            (id_tipo, descricao, id_status, id_area, data_inicio,
                             prazo, termino, comentarios, int(selected['id_plano']))
                        )
                        st.success("Ação atualizada com sucesso.")
                    else:
                        run_query(
                            "INSERT INTO tb_plano_tratamento (id_risco, id_tipo_tratamento, descricao_acao, id_status, id_area_responsavel, data_inicio, data_prazo_limite, data_real_termino, comentarios, usuario_criacao) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                            (int(id_risco), int(id_tipo), descricao, int(id_status), int(
                                id_area), data_inicio, prazo, termino, comentarios, st.session_state.get('current_user', ''))
                        )
                        st.success("Ação criada com sucesso.")
                except Exception as e:
                    st.error(f"Erro ao salvar ação: {e}")
                finally:
                    st.session_state.pop('pt_grid', None)
                    if hasattr(st, 'experimental_rerun'):
                        st.experimental_rerun()

    # 3️⃣ Grid de Ações Existentes
    with col_grid:
        st.subheader("📊 Ações de Tratamento Existentes")
        plans_df = run_select(
            "SELECT pt.id_plano, tt.descricao AS tipo, pt.descricao_acao, sp.descricao AS status, ar.nome_area AS area, pt.data_inicio, pt.data_prazo_limite, pt.data_real_termino FROM tb_plano_tratamento pt JOIN tb_tipo_tratamento tt ON pt.id_tipo_tratamento=tt.id_tipo_tratamento JOIN tb_status_plano sp ON pt.id_status=sp.id_status JOIN tb_area_responsavel ar ON pt.id_area_responsavel=ar.id_area WHERE pt.id_risco=%s ORDER BY pt.data_inicio DESC;",
            (int(id_risco),)
        )
        if plans_df.empty:
            st.info("Nenhuma ação de tratamento cadastrada para este risco.")
        else:
            gb2 = GridOptionsBuilder.from_dataframe(plans_df)
            gb2.configure_selection('single', use_checkbox=True)
            gb2.configure_column('id_plano', header_name='ID', editable=False)
            gb2.configure_column('descricao_acao', wrapText=True)
            opts2 = gb2.build()
            grid_resp = AgGrid(plans_df, gridOptions=opts2, update_mode=GridUpdateMode.SELECTION_CHANGED,
                               data_return_mode=DataReturnMode.AS_INPUT, theme='ag-theme-alpine-dark', height=300, fit_columns_on_grid_load=True)
            st.session_state['pt_grid'] = grid_resp
            if st.button("🗑️ Remover Ação", key='pt_rm'):
                raw = grid_resp.get('selected_rows')
                rows = raw.to_dict('records') if isinstance(
                    raw, pd.DataFrame) else raw or []
                if not rows:
                    st.warning("Selecione uma ação para remover.")
                else:
                    run_query("DELETE FROM tb_plano_tratamento WHERE id_plano=%s;", (int(
                        rows[0]['id_plano']),))
                    st.success("Ação removida com sucesso.")
                    st.session_state.pop('pt_grid', None)
                    if hasattr(st, 'experimental_rerun'):
                        st.experimental_rerun()


# Alias de importação em app.py
main = riscos_plano_tratamento

# Execução direta para debug
if __name__ == '__main__':
    riscos_plano_tratamento()
