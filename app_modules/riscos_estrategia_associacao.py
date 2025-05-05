import streamlit as st
import pandas as pd
from pathlib import Path
from database_utils import run_select, run_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


def riscos_estrategia_associacao():
    """
    Tela de Associação Riscos ↔ Estratégia (multi-tenant SaaS).
    Permite criar, ler, atualizar e deletar vínculos entre riscos e metas estratégicas.
    """
    # Injeção de CSS
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

    # Cabeçalho principal
    st.title("Associação de Riscos a Estratégia")
    st.markdown("_Gerencie vínculos entre riscos e metas estratégicas_")
    st.markdown("---")

    # 1️⃣ Seleção de Empresa
    emp_df = run_select(
        "SELECT id_empresa, nome_empresa FROM tb_empresas ORDER BY nome_empresa;")
    if emp_df.empty:
        st.error("Nenhuma empresa cadastrada. Cadastre empresas antes de prosseguir.")
        return
    emp_df['label'] = emp_df['id_empresa'].astype(
        str) + ' – ' + emp_df['nome_empresa']
    escolha_emp = st.selectbox(
        "Selecione a Empresa:", emp_df['label'], key='rea_empresa')
    id_empresa = int(escolha_emp.split(' – ')[0])

    # 2️⃣ Seleção de Risco
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
        "Selecione o Risco:", riscos_df['label'], key='rea_risco')
    id_risco = int(escolha_risco.split(' – ')[0])

    # 3️⃣ Carrega Objetivos e Metas para formulário
    obj_df = run_select(
        "SELECT id_objetivo, descricao FROM tb_objetivo_estrategico WHERE id_empresa = %s ORDER BY id_objetivo;",
        (id_empresa,)
    )
    meta_df = run_select(
        "SELECT id_meta, id_objetivo, descricao FROM tb_meta_estrategica WHERE id_empresa = %s ORDER BY id_objetivo, id_meta;",
        (id_empresa,)
    )

    # 4️⃣ Layout: formulário à esquerda, grid à direita
    col_form, col_grid = st.columns([1, 2], gap='large')

    with col_form:
        st.subheader("📌 Nova Associação / Editar Existente")
        # Identifica seleção existente se estiver editando
        raw = st.session_state.get('assoc_grid', {}).get('selected_rows')
        if isinstance(raw, pd.DataFrame):
            sel_list = raw.to_dict('records')
        elif isinstance(raw, list):
            sel_list = raw
        else:
            sel_list = []
        is_edit = st.checkbox("Editar Associação", value=False, key='rea_edit')
        selected = sel_list[0] if is_edit and sel_list else None

        with st.form(key='rea_form'):
            # Objetivo dropdown
            obj_opts = obj_df['descricao'].tolist()
            obj_idx = obj_df[obj_df['id_objetivo'] ==
                             selected['id_objetivo']].index[0] if selected else 0
            escolha_obj = st.selectbox(
                "Objetivo Estratégico:", obj_opts, index=obj_idx)
            id_obj = obj_df.loc[obj_idx, 'id_objetivo']

            # Filtra metas pelo objetivo
            metas_filtradas = meta_df[meta_df['id_objetivo'] == id_obj]
            meta_opts = metas_filtradas['descricao'].tolist()
            if selected:
                # encontra índice da meta selecionada
                idx_meta = metas_filtradas.index[metas_filtradas['id_meta']
                                                 == selected['id_meta']][0]
            else:
                idx_meta = 0
            escolha_meta = st.selectbox(
                "Meta Estratégica:", meta_opts, index=idx_meta)
            id_meta = metas_filtradas.iloc[idx_meta]['id_meta']

            btn_label = "Atualizar Associação" if is_edit else "Criar Associação"
            if st.form_submit_button(btn_label):
                if is_edit:
                    run_query(
                        "UPDATE tb_risco_meta SET id_meta=%s WHERE id_risco_meta=%s",
                        (id_meta, selected['id_risco_meta'])
                    )
                    st.success("Associação atualizada com sucesso.")
                else:
                    run_query(
                        "INSERT INTO tb_risco_meta (id_empresa,id_risco,id_meta,usuario_criacao) VALUES (%s,%s,%s,%s);",
                        (id_empresa, id_risco, id_meta,
                         st.session_state.get('current_user', ''))
                    )
                    st.success("Associação criada com sucesso.")
                # limpa estado para recarga
                if 'assoc_grid' in st.session_state:
                    del st.session_state['assoc_grid']
                st.experimental_rerun()

    with col_grid:
        st.subheader("🎯 Associações Existentes")
        assoc_df = run_select(
            """
            SELECT rm.id_risco_meta, o.descricao AS objetivo, m.descricao AS meta
            FROM tb_risco_meta rm
             JOIN tb_meta_estrategica m ON rm.id_meta = m.id_meta
             JOIN tb_objetivo_estrategico o ON m.id_objetivo = o.id_objetivo
            WHERE rm.id_empresa = %s AND rm.id_risco = %s
            ORDER BY rm.data_criacao DESC;
            """, (id_empresa, id_risco)
        )
        if assoc_df.empty:
            st.info("Nenhuma associação existente para este risco.")
        else:
            gb = GridOptionsBuilder.from_dataframe(assoc_df)
            gb.configure_selection('single', use_checkbox=True)
            gb.configure_column(
                'id_risco_meta', header_name='ID', editable=False)
            gb.configure_column(
                'objetivo', header_name='Objetivo Estratégico', wrapText=True)
            gb.configure_column(
                'meta', header_name='Meta Estratégica', wrapText=True)
            opts = gb.build()
            grid_resp = AgGrid(
                assoc_df,
                gridOptions=opts,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                data_return_mode=DataReturnMode.AS_INPUT,
                theme='ag-theme-alpine-dark',
                height=300,
                fit_columns_on_grid_load=True
            )
            st.session_state['assoc_grid'] = grid_resp
            # Remoção
            if st.button("🗑️ Remover Associação", key='rea_rm'):
                raw = grid_resp.get('selected_rows')
                if isinstance(raw, pd.DataFrame):
                    rows = raw.to_dict('records')
                else:
                    rows = raw or []
                if not rows:
                    st.warning("Selecione uma associação para remover.")
                else:
                    run_query(
                        "DELETE FROM tb_risco_meta WHERE id_risco_meta=%s;", (rows[0]['id_risco_meta'],))
                    st.success("Associação removida com sucesso.")
                    del st.session_state['assoc_grid']
                    st.experimental_rerun()


# Execução direta
if __name__ == '__main__':
    riscos_estrategia_associacao()
