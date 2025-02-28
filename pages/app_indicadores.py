import streamlit as st
from database_utils import run_select
import pandas as pd
import io

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Gestão de Riscos - Indicadores", layout="wide")

# Função principal


def main():
    st.title("📊 Indicadores de Desempenho de Riscos")

    # ---------------------- Funções Auxiliares ----------------------
    @st.cache_data
    def consultar_dados(query):
        """Executa uma consulta SQL e retorna os dados como DataFrame."""
        return run_select(query)

    def gerar_excel(df, sheet_name="Indicadores"):
        """Gera um arquivo Excel com os dados fornecidos."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        return output

    # ---------------------- Interface Principal ----------------------
    st.sidebar.header("Filtros de Indicadores")

    # 🔹 Seleção de Indicador
    indicador = st.sidebar.selectbox("Selecione um Indicador", [
                                     "Taxa de Ocorrência", "Custo Total de Riscos", "Tempo Médio de Mitigação", "Percentual de Riscos Encerrados"])

    # 🔹 Filtro de Período
    data_inicio = st.sidebar.date_input(
        "📅 Data Inicial", value=pd.to_datetime("2023-01-01"))
    data_fim = st.sidebar.date_input(
        "📅 Data Final", value=pd.to_datetime("today"))

    # 🔹 Botão para Buscar Dados
    if st.sidebar.button("🔍 Buscar Indicadores"):
        query = f"""
        SELECT nome_kpi, descricao_kpi, valor_atual, meta, unidade_medida, data_atualizacao 
        FROM indicadores 
        WHERE nome_kpi = '{indicador}' 
        AND data_atualizacao BETWEEN '{data_inicio}' AND '{data_fim}'
        ORDER BY data_atualizacao DESC"""
        df_indicadores = consultar_dados(query)

        if df_indicadores.empty:
            st.warning(
                "⚠️ Nenhum indicador encontrado para os filtros selecionados.")
        else:
            st.subheader("📈 Indicadores de Desempenho")
            st.dataframe(df_indicadores, use_container_width=True)

            # Exportação para Excel
            excel_file = gerar_excel(df_indicadores)
            st.download_button(
                label="📥 Baixar Relatório Excel",
                data=excel_file,
                file_name="Relatorio_Indicadores.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


if __name__ == "__main__":
    main()
