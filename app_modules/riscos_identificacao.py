import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database_utils import run_select, run_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def evenly_spaced_positions(n, start=0.1, end=0.9):
    """Retorna uma lista de posições y distribuídas uniformemente para n nós."""
    if n == 1:
        return [0.5]
    return [start + i * (end - start) / (n - 1) for i in range(n)]


def main():
    st.markdown("### Fase 2 - Identificação de Riscos ###")
    st.write("Digite sua consulta para buscar riscos. A busca é feita textual (usando ILIKE) e os dados normalizados são usados para gerar o diagrama Sankey.")

    # Variáveis de sessão
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "df_riscos" not in st.session_state:
        st.session_state.df_riscos = None

    # Formulário de busca
    with st.form(key="search_form"):
        search_query = st.text_input(
            "Digite o contexto do mapeamento de riscos:", value=st.session_state.search_query, key="input_search_query")
        submit_search = st.form_submit_button("🔍 Buscar Riscos")
        if submit_search:
            if search_query.strip():
                st.session_state.search_query = search_query.strip()
                like_query = f"%{st.session_state.search_query}%"
                # Query simplificada: retorna 1 linha por risco
                query = """
                SELECT 
                  r.id_risco,
                  r.nome_risco,
                  r.descricao,
                  r.criticidade,
                  p.nome_processo
                FROM tb_riscos r
                LEFT JOIN tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
                LEFT JOIN tb_processos p ON sp.id_processo = p.id_processo
                WHERE r.nome_risco ILIKE %s
                   OR r.descricao ILIKE %s
                   OR p.nome_processo ILIKE %s
                ORDER BY r.data_identificacao DESC;
                """
                params = (like_query, like_query, like_query)
                df = run_select(query, params)
                st.session_state.df_riscos = df
            else:
                st.warning("Digite uma consulta para buscar riscos.")

    # Exibe o grid se houver resultados
    if st.session_state.df_riscos is not None:
        df_riscos = st.session_state.df_riscos
        if df_riscos.empty:
            st.info("Nenhum risco encontrado para a consulta.")
        else:
            st.write("Riscos encontrados:")
            # Exibir apenas as colunas desejadas
            df_display = df_riscos[["id_risco", "nome_risco",
                                    "descricao", "criticidade", "nome_processo"]]
            gb = GridOptionsBuilder.from_dataframe(df_display)
            gb.configure_selection("multiple", use_checkbox=True,
                                   groupSelectsChildren=True, suppressRowClickSelection=True)
            grid_options = gb.build()
            grid_response = AgGrid(df_display, gridOptions=grid_options,
                                   update_mode=GridUpdateMode.SELECTION_CHANGED,
                                   height=300, fit_columns_on_grid_load=True)

            # Extração dos riscos selecionados
            selected_rows = grid_response.get("selected_rows")
            if isinstance(selected_rows, pd.DataFrame):
                selected_rows = selected_rows.to_dict("records")
            elif selected_rows is None:
                selected_rows = []

            st.write("IDs dos riscos selecionados:", [
                     row["id_risco"] for row in selected_rows])

            # Geração do Sankey para os riscos selecionados
            if selected_rows:
                for row in selected_rows:
                    risk_id = row["id_risco"]
                    # Query para obter causas e consequências (dados normalizados)
                    sankey_query = """
                    SELECT 
                        ca.descricao_causa AS causa,
                        cons.descricao_consequencia AS consequencia
                    FROM tb_risco_causa rc
                    LEFT JOIN tb_causas ca ON rc.id_causa = ca.id_causa
                    LEFT JOIN tb_risco_consequencia rcons ON rc.id_risco = rcons.id_risco
                    LEFT JOIN tb_consequencias cons ON rcons.id_consequencia = cons.id_consequencia
                    WHERE rc.id_risco = %s;
                    """
                    sankey_df = run_select(sankey_query, (risk_id,))
                    if sankey_df.empty:
                        st.info(
                            f"Nenhuma causa ou consequência encontrada para o risco {risk_id}.")
                    else:
                        # Extrai valores únicos
                        unique_causes = sankey_df['causa'].dropna(
                        ).unique().tolist()
                        unique_cons = sankey_df['consequencia'].dropna(
                        ).unique().tolist()
                        # Constrói os nós: causas, nome do risco e consequências
                        nodes = unique_causes + \
                            [row["nome_risco"]] + unique_cons
                        N_c = len(unique_causes)
                        risk_index = N_c  # O nó do risco fica logo após as causas

                        # Define os links: de cada causa para o risco e do risco para cada consequência
                        # índices 0 até N_c-1 (causas)
                        sources = list(range(N_c))
                        targets = [risk_index] * N_c
                        values = [1] * N_c
                        sources += [risk_index] * len(unique_cons)
                        targets += [risk_index + 1 +
                                    i for i in range(len(unique_cons))]
                        values += [1] * len(unique_cons)

                        # Define posições para os nós
                        x_causes = [0] * N_c
                        y_causes = evenly_spaced_positions(N_c)
                        x_risk = [0.5]
                        y_risk = [0.5]
                        x_cons = [1] * len(unique_cons)
                        y_cons = evenly_spaced_positions(len(unique_cons))
                        x_positions = x_causes + x_risk + x_cons
                        y_positions = y_causes + y_risk + y_cons

                        fig = go.Figure(data=[go.Sankey(
                            arrangement="fixed",
                            node=dict(
                                pad=15,
                                thickness=10,
                                line=dict(color="black", width=1),
                                label=nodes,
                                color="skyblue",
                                x=x_positions,
                                y=y_positions
                            ),
                            link=dict(
                                source=sources,
                                target=targets,
                                value=values,
                                line=dict(color="black", width=1)
                            )
                        )])
                        fig.update_layout(
                            title_text=f"Sankey para Risco {risk_id}: {row['nome_risco']}", font_size=10)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selecione pelo menos um risco para visualizar o Sankey.")

            # Formulário para salvar os riscos selecionados
            with st.form(key="save_selected_form"):
                usuario = st.text_input(
                    "Usuário", value="usuario_padrão", key="input_usuario")
                observacoes = st.text_area(
                    "Observações (opcional)", key="input_observacoes")
                submit_save = st.form_submit_button(
                    "💾 Salvar Riscos Selecionados")
                if submit_save:
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
                    for row in selected_rows:
                        risk_id = row["id_risco"]
                        insert_query = """
                        INSERT INTO tb_risco_selecionado (id_empresa, id_risco, usuario, observacoes)
                        VALUES (%s, %s, %s, %s);
                        """
                        params_insert = (1, risk_id, usuario, observacoes)
                        run_query(insert_query, params_insert)
                        count += 1
                    st.success(
                        f"{count} risco(s) selecionado(s) salvos com sucesso!")

    st.markdown("---")
    st.write("Utilize esta ferramenta para buscar e associar riscos à sua empresa de forma inteligente (POC).")


if __name__ == "__main__":
    main()
