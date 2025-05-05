import streamlit as st
import pandas as pd
from pathlib import Path
from database_utils import run_select
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


def riscos_estrategia():
    """
    Tela de Estratégia de Riscos (Multi-tenant SaaS).
    Permite seleção de empresa, definição de objetivos, exibição de metas e indicadores.
    """
    # 1. Injeção de CSS global
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        css = css_file.read_text(encoding='utf-8')
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # 2. Cabeçalho
    st.title("Estratégia de Riscos")
    st.markdown("_Definição de Objetivos, Metas e Indicadores por Empresa_")
    st.markdown("---")

    # 3. Seleção de Empresa (multi-tenant)
    emp_df = run_select(
        "SELECT id_empresa, nome_empresa FROM tb_empresas ORDER BY nome_empresa;"
    )
    if emp_df.empty:
        st.error("Nenhuma empresa cadastrado. Verifique a base de dados.")
        return
    emp_df['label'] = emp_df['id_empresa'].astype(
        str) + ' – ' + emp_df['nome_empresa']
    escolha_emp = st.selectbox(
        "Selecione a Empresa:", emp_df['label'], key='re_empresa')
    id_empresa = int(escolha_emp.split(' – ')[0])

    # 4. Recupera Objetivos Estratégicos
    obj_df = run_select(
        "SELECT id_objetivo, descricao FROM tb_objetivo_estrategico "
        "WHERE id_empresa = %s ORDER BY id_objetivo;",
        (id_empresa,)
    )
    if obj_df.empty:
        st.info("Nenhum Objetivo Estratégico cadastrado para esta empresa.")
        return
    obj_df['label'] = obj_df['id_objetivo'].astype(
        str) + ' – ' + obj_df['descricao']
    escolha_obj = st.selectbox(
        "Selecione o Objetivo Estratégico:", obj_df['label'], key='re_objetivo')
    id_objetivo = int(escolha_obj.split(' – ')[0])

    # 5. Consulta Metas Estratégicas
    metas_df = run_select(
        "SELECT id_meta, descricao, ano FROM tb_meta_estrategica "
        "WHERE id_empresa = %s AND id_objetivo = %s ORDER BY id_meta;",
        (id_empresa, id_objetivo)
    )
    st.subheader("Metas Estratégicas")
    if metas_df.empty:
        st.info("Nenhuma Meta cadastrada para este Objetivo.")
    else:
        gb_meta = GridOptionsBuilder.from_dataframe(metas_df)
        gb_meta.configure_selection('single', use_checkbox=True)
        gb_meta.configure_column('id_meta', header_name='ID', editable=False)
        gb_meta.configure_column(
            'descricao', header_name='Meta Anual', wrapText=True, autoHeight=True)
        gb_meta.configure_column('ano', header_name='Ano')
        opts_meta = gb_meta.build()
        AgGrid(
            metas_df,
            gridOptions=opts_meta,
            update_mode=GridUpdateMode.NO_UPDATE,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            theme='ag-theme-alpine-dark',
            height=200,
            fit_columns_on_grid_load=True
        )

    # 6. Consulta Indicadores vinculados
    ind_df = run_select(
        "SELECT i.id_indicador, i.descricao, i.valor_alvo, m.id_meta FROM tb_indicador i "
        "JOIN tb_meta_estrategica m ON i.id_meta = m.id_meta "
        "WHERE i.id_empresa = %s AND m.id_objetivo = %s ORDER BY i.id_indicador;",
        (id_empresa, id_objetivo)
    )
    st.subheader("Indicadores")
    if ind_df.empty:
        st.info("Nenhum Indicador cadastrado para este Objetivo.")
    else:
        gb_ind = GridOptionsBuilder.from_dataframe(ind_df)
        gb_ind.configure_column(
            'id_indicador', header_name='ID', editable=False)
        gb_ind.configure_column(
            'descricao', header_name='Indicador', wrapText=True, autoHeight=True)
        gb_ind.configure_column('valor_alvo', header_name='Valor Alvo')
        opts_ind = gb_ind.build()
        AgGrid(
            ind_df,
            gridOptions=opts_ind,
            update_mode=GridUpdateMode.NO_UPDATE,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            theme='ag-theme-alpine-dark',
            height=200,
            fit_columns_on_grid_load=True
        )


# Execução direta
if __name__ == '__main__':
    riscos_estrategia()
