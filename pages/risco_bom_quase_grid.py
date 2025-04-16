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
    st.markdown("### Busca Inteligente de Riscos (POC)")
    st.write(
        "Digite sua consulta para buscar riscos. Nesta versão POC, a busca é feita textual (usando ILIKE) "
        "e os dados normalizados (modelo 3FN) são utilizados para gerar o diagrama Sankey."
    )

    # Variáveis de sessão
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "df_riscos" not in st.session_state:
        st.session_state.df_riscos = None

    # Formulário de busca
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
                  r.id_risco,
                  r.id_empresa,
                  r.nome_risco,
                  r.descricao,
                  r.impacto_estimado,
                  r.probabilidade,
                  r.status,
                  r.data_identificacao,
                  r.criticidade,
                  p.nome_processo,
                  sp.nome_subprocesso,
                  ca.descricao_causa AS causa,
                  cons.descricao_consequencia AS consequencia
                FROM tb_riscos r
                LEFT JOIN tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
                LEFT JOIN tb_processos p ON sp.id_processo = p.id_processo
                LEFT JOIN tb_risco_causa rc ON r.id_risco = rc.id_risco
                LEFT JOIN tb_causas ca ON rc.id_causa = ca.id_causa
                LEFT JOIN tb_risco_consequencia rcons ON r.id_risco = rcons.id_risco
                LEFT JOIN tb_consequencias cons ON rcons.id_consequencia = cons.id_consequencia
                WHERE r.nome_risco ILIKE %s
                   OR r.descricao ILIKE %s
                   OR ca.descricao_causa ILIKE %s
                   OR sp.nome_subprocesso ILIKE %s
                   OR p.nome_processo ILIKE %s
                ORDER BY r.data_identificacao DESC;
                """
                params = (like_query, like_query,
                          like_query, like_query, like_query)
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

            # Extração dos riscos selecionados
            selected_rows = grid_response.get("selected_rows")
            if isinstance(selected_rows, pd.DataFrame):
                selected_rows = selected_rows.to_dict("records")
            elif selected_rows is None:
                selected_rows = []

            # Criação do Sankey (apenas para os riscos selecionados)
            if selected_rows:
                selected_df = pd.DataFrame(selected_rows)
                unique_risks = selected_df['nome_risco'].unique()
                for risk in unique_risks:
                    group = selected_df[selected_df['nome_risco'] == risk]
                    # Como os dados já estão normalizados, extraímos os valores únicos
                    unique_causes = group['causa'].dropna().unique().tolist()
                    unique_cons = group['consequencia'].dropna(
                    ).unique().tolist()
                    nodes = unique_causes + [risk] + unique_cons
                    N_c = len(unique_causes)
                    risk_index = N_c  # índice do nó do risco

                    sources = list(range(N_c))  # de cada causa para o risco
                    targets = [risk_index] * N_c
                    values = [1] * N_c
                    # Links do risco para cada consequência
                    sources += [risk_index] * len(unique_cons)
                    targets += [risk_index + 1 +
                                i for i in range(len(unique_cons))]
                    values += [1] * len(unique_cons)

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
                        title_text=f"Sankey para Risco: {risk}", font_size=10)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selecione pelo menos um risco para visualizar o Sankey.")

            # Exibe os IDs dos riscos selecionados
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
