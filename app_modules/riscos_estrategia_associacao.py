from pathlib import Path

import pandas as pd
import streamlit as st
from st_aggrid import (AgGrid, DataReturnMode, GridOptionsBuilder,
                       GridUpdateMode)

from database_utils import run_query, run_select


def riscos_estrategia_associacao():
    """
    Tela de Associação Riscos ↔ Estratégia (multi-tenant SaaS).
    Permite CRUD de vínculos entre riscos e metas estratégicas.
    """
    # Injeção de CSS global
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True
        )

    # Cabeçalho
    st.title("Associação de Riscos a Estratégia")
    st.markdown("_Gerencie vínculos entre riscos e metas estratégicas_")
    st.markdown("---")

    # ── 1️⃣ Selecione a Empresa
    emp_df = run_select(
        "SELECT id_empresa, nome_empresa FROM tb_empresas ORDER BY nome_empresa;"
    )
    if emp_df.empty:
        st.error("Nenhuma empresa cadastrada.")
        return
    emp_df["label"] = emp_df["id_empresa"].astype(
        str) + " – " + emp_df["nome_empresa"]
    escolha_emp = st.selectbox(
        "Selecione a Empresa:", emp_df["label"], key="rea_empresa")
    id_empresa = int(escolha_emp.split(" – ")[0])

    # ── 2️⃣ Selecione o Risco
    riscos_df = run_select(
        "SELECT id_risco, nome_risco FROM tb_riscos WHERE id_empresa = %s ORDER BY id_risco;",
        (id_empresa,)
    )
    if riscos_df.empty:
        st.info("Nenhum risco cadastrado para esta empresa.")
        return
    riscos_df["label"] = riscos_df["id_risco"].astype(
        str) + " – " + riscos_df["nome_risco"]
    escolha_risco = st.selectbox(
        "Selecione o Risco:", riscos_df["label"], key="rea_risco")
    id_risco = int(escolha_risco.split(" – ")[0])

    # ── 3️⃣ Carrega Objetivos e Metas
    obj_df = run_select(
        "SELECT id_objetivo, descricao FROM tb_objetivo_estrategico WHERE id_empresa = %s ORDER BY id_objetivo;",
        (id_empresa,)
    )
    meta_df = run_select(
        "SELECT id_meta, id_objetivo, descricao FROM tb_meta_estrategica WHERE id_empresa = %s ORDER BY id_objetivo, id_meta;",
        (id_empresa,)
    )
    # garanta tipos inteiros
    obj_df["id_objetivo"] = obj_df["id_objetivo"].astype(int)
    meta_df[["id_meta", "id_objetivo"]] = meta_df[[
        "id_meta", "id_objetivo"]].astype(int)

    # Layout: formulário à esquerda, grid à direita
    col_form, col_grid = st.columns([1, 2], gap="large")

    # ── 4️⃣ Formulário de criação/edição
    with col_form:
        st.subheader("📌 Nova Associação / ✏️ Editar Existente")
        # defina se é edição
        if "rea_is_edit" not in st.session_state:
            st.session_state["rea_is_edit"] = False
        st.session_state["rea_is_edit"] = st.checkbox(
            "Editar Associação", value=st.session_state["rea_is_edit"], key="rea_edit")

        # seleção para edição (se houver)
        grid_sel = st.session_state.get(
            "assoc_grid", {}).get("selected_rows", [])
        if isinstance(grid_sel, pd.DataFrame):
            sel_list = grid_sel.to_dict("records")
        else:
            sel_list = grid_sel or []
        selected = sel_list[0] if st.session_state["rea_is_edit"] and sel_list else None

        # filtro de metas
        obj_labels = obj_df["descricao"].tolist()
        escolha_obj = st.selectbox(
            "Objetivo Estratégico:", obj_labels, key="rea_objetivo_sel")
        id_obj = int(obj_df.loc[obj_df["descricao"] ==
                     escolha_obj, "id_objetivo"].iloc[0])
        metas_filtradas = meta_df[meta_df["id_objetivo"]
                                  == id_obj].reset_index(drop=True)
        if metas_filtradas.empty:
            st.warning("Nenhuma meta disponível para o objetivo selecionado.")

        with st.form(key="rea_form"):
            meta_opts = metas_filtradas["descricao"].tolist()
            default_idx = 0
            if selected:
                # encontra índice da meta selecionada
                match = metas_filtradas[metas_filtradas["id_meta"] == int(
                    selected.get("id_meta", -1))]
                if not match.empty:
                    default_idx = match.index[0]
            escolha_meta = st.selectbox(
                "Meta Estratégica:", meta_opts, index=default_idx, key="rea_meta_sel")
            id_meta = int(metas_filtradas.loc[default_idx, "id_meta"])

            if st.form_submit_button("Salvar Associação"):
                try:
                    if st.session_state["rea_is_edit"] and selected:
                        run_query(
                            "UPDATE tb_risco_meta SET id_meta = %s WHERE id_risco_meta = %s;",
                            (id_meta, int(selected["id_risco_meta"]))
                        )
                        st.success("Associação atualizada com sucesso.")
                    else:
                        run_query(
                            "INSERT INTO tb_risco_meta (id_empresa, id_risco, id_meta, usuario_criacao) VALUES (%s, %s, %s, %s);",
                            (id_empresa, id_risco, id_meta,
                             st.session_state.get("current_user", "script"))
                        )
                        st.success("Associação criada com sucesso.")
                except Exception as e:
                    if hasattr(e, "pgcode"):
                        st.warning(
                            "Esta associação já existe para o risco e meta selecionados.")
                    else:
                        st.error(f"Erro ao salvar associação: {e}")
                # limpa estado e força reload
                st.session_state.pop("assoc_grid", None)
                st.session_state["rea_is_edit"] = False
                st.stop()

    # ── 5️⃣ Grid de Associações
    with col_grid:
        st.subheader("🎯 Associações Existentes")
        assoc_df = run_select(
            """
            SELECT rm.id_risco_meta,
                   rm.id_meta,
                   m.id_objetivo,
                   o.descricao AS objetivo,
                   m.descricao AS meta
              FROM tb_risco_meta rm
              JOIN tb_meta_estrategica m ON rm.id_meta = m.id_meta
              JOIN tb_objetivo_estrategico o ON m.id_objetivo = o.id_objetivo
             WHERE rm.id_empresa = %s
               AND rm.id_risco = %s
             ORDER BY rm.data_criacao DESC;
            """,
            (id_empresa, id_risco)
        )
        if assoc_df.empty:
            st.info("Nenhuma associação encontrada para este risco.")
        else:
            gb = GridOptionsBuilder.from_dataframe(assoc_df)
            gb.configure_selection("single", use_checkbox=True)
            gb.configure_column(
                "id_risco_meta", header_name="ID", editable=False, width=80)
            gb.configure_column("id_meta", header_name="ID Meta", hide=True)
            gb.configure_column(
                "id_objetivo", header_name="ID Objetivo", hide=True)
            gb.configure_column("objetivo", wrapText=True)
            gb.configure_column("meta", wrapText=True)
            opts = gb.build()
            grid_resp = AgGrid(
                assoc_df,
                gridOptions=opts,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                data_return_mode=DataReturnMode.AS_INPUT,
                theme="ag-theme-alpine-dark",
                height=300,
                fit_columns_on_grid_load=True
            )
            st.session_state["assoc_grid"] = grid_resp

            # botão de remoção
            if st.button("🗑️ Remover Associação", key="rea_rm"):
                selected_rows = st.session_state["assoc_grid"].get(
                    "selected_rows", [])
                if not selected_rows:
                    st.warning("Selecione uma associação para remover.")
                else:
                    rm_id = int(selected_rows[0]["id_risco_meta"])
                    run_query(
                        "DELETE FROM tb_risco_meta WHERE id_risco_meta = %s;", (rm_id,))
                    st.success("Associação removida com sucesso.")
                    st.session_state.pop("assoc_grid", None)
                    st.stop()


# Execução direta
if __name__ == "__main__":
    riscos_estrategia_associacao()
