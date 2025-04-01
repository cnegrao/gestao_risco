import streamlit as st
import pandas as pd
from database_utils import run_select, run_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def main():
    st.markdown("### Busca Inteligente de Riscos (POC)")
    st.write(
        "Digite sua consulta para buscar riscos. Nesta versão POC, a busca é simulada utilizando condições ILIKE "
        "para aproximar uma busca semântica. Em produção, recomenda-se utilizar embeddings e similaridade de cosseno."
    )

    # Inicializa variáveis de sessão para persistência
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "df_riscos" not in st.session_state:
        st.session_state.df_riscos = None

    # Formulário para a busca
    with st.form(key="search_form"):
        search_query = st.text_input(
            "Digite sua consulta:",
            value=st.session_state.search_query,
            key="input_search_query"
        )
        submit_search = st.form_submit_button("🔍 Buscar Riscos")
        if submit_search:
            if search_query.strip():
                st.session_state.search_query = search_query.strip()
                like_query = f"%{st.session_state.search_query}%"
                query = """
                SELECT 
                    r.id_risco as id_risco,
                    r.id_empresa as id_empresa,
                    r.nome_risco,
                    r.descricao,
                    r.causa,
                    r.consequencia,
                    r.impacto_estimado,
                    r.probabilidade,
                    r.status,
                    r.data_identificacao,
                    r.criticidade,
                    p.nome_processo,
                    sp.nome_subprocesso,
                    c.nome_categoria,
                    sc.nome_subcategoria
                FROM tb_riscos r
                JOIN tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
                JOIN tb_processos p ON sp.id_processo = p.id_processo
                JOIN tb_subcategorias sc ON r.id_subcategoria = sc.id_subcategoria
                JOIN tb_categorias c ON sc.id_categoria = c.id_categoria
                WHERE r.nome_risco ILIKE %s
                   OR r.descricao ILIKE %s
                   OR c.nome_categoria ILIKE %s
                   OR sp.nome_subprocesso ILIKE %s
                ORDER BY r.data_identificacao DESC;
                """
                params = (like_query, like_query, like_query, like_query)
                df = run_select(query, params)
                st.session_state.df_riscos = df
            else:
                st.warning("Digite uma consulta para buscar riscos.")

    # Se houver resultados na busca, exiba-os em uma grid com checkboxes para seleção múltipla
    if st.session_state.df_riscos is not None:
        df_riscos = st.session_state.df_riscos
        if df_riscos.empty:
            st.info("Nenhum risco encontrado para a consulta.")
        else:
            st.write("Selecione os riscos desejados:")
            gb = GridOptionsBuilder.from_dataframe(df_riscos)
            gb.configure_selection("multiple", use_checkbox=True,
                                   groupSelectsChildren=True, suppressRowClickSelection=False)
            grid_options = gb.build()
            grid_response = AgGrid(
                df_riscos,
                gridOptions=grid_options,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                height=300,
                fit_columns_on_grid_load=True
            )

            # Verifica se "selected_rows" é um DataFrame e converte para lista de dicionários, se necessário
            selected_rows = grid_response.get("selected_rows")
            if isinstance(selected_rows, pd.DataFrame):
                selected_rows = selected_rows.to_dict("records")
            elif selected_rows is None:
                selected_rows = []

            selected_ids = []
            for row in selected_rows:
                if isinstance(row, dict):
                    risk_id = row.get("id_risco")
                    company_id = row.get("id_empresa")
                    if risk_id is not None and company_id is not None:
                        selected_ids.append((risk_id, company_id))
                    else:
                        st.error(
                            f"Chave 'id_risco' ou 'id_empresa' não encontrada na linha: {row}")
                else:
                    st.error(f"Tipo inesperado: {type(row)} - {row}")

            st.write(
                "IDs dos riscos selecionados (id_risco, id_empresa):", selected_ids)

            # Formulário para salvar os riscos selecionados
            with st.form(key="save_selected_form"):
                usuario = st.text_input(
                    "Usuário", value="usuario_padrão", key="input_usuario")
                observacoes = st.text_area(
                    "Observações (opcional)", key="input_observacoes")
                submit_save = st.form_submit_button(
                    "💾 Salvar Riscos Selecionados")
                if submit_save:
                    # Cria a tabela de associação, se ainda não existir
                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS tb_risco_selecionado (
                        id_risco_selecionado SERIAL PRIMARY KEY,
                        id_empresa INT REFERENCES tb_empresas(id_empresa),
                        id_risco INT REFERENCES tb_riscos(id_risco),
                        data_selecao DATE NOT NULL DEFAULT CURRENT_DATE,
                        usuario VARCHAR(100),
                        observacoes TEXT
                    );
                    """
                    run_query(create_table_query)

                    count = 0
                    st.write("IDs que serão gravados:", selected_ids)
                    for risk_id, company_id in selected_ids:
                        insert_query = """
                        INSERT INTO tb_risco_selecionado (id_empresa, id_risco, usuario, observacoes)
                        VALUES (%s, %s, %s, %s);
                        """
                        params_insert = (company_id, risk_id,
                                         usuario, observacoes)
                        run_query(insert_query, params_insert)
                        count += 1
                    st.success(
                        f"{count} risco(s) selecionado(s) e associados à empresa com sucesso!")

    st.markdown("---")
    st.write("Utilize esta ferramenta para buscar e associar riscos à sua empresa de forma inteligente (POC).")


if __name__ == "__main__":
    main()
