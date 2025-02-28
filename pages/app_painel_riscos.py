import streamlit as st
from database_utils import run_select
import pandas as pd
import io
import plotly.express as px

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(
    page_title="Gestão de Riscos - Painel de Riscos", layout="wide")

# Função principal


def main():
    st.title("📊 Painel de Monitoramento de Riscos")

    # ---------------------- Funções Auxiliares ----------------------
    @st.cache_data
    def consultar_dados(query):
        """Executa uma consulta SQL e retorna os dados como DataFrame."""
        return run_select(query)

    def gerar_excel(df, sheet_name="Painel_Riscos"):
        """Gera um arquivo Excel com os dados fornecidos."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        return output

    # ---------------------- Painel de Indicadores ----------------------
    st.subheader("📊 Resumo Geral de Riscos")

    query_resumo = """
        SELECT categoria, COUNT(*) as total 
        FROM riscos 
        GROUP BY categoria
    """
    df_resumo = consultar_dados(query_resumo)

    if not df_resumo.empty:
        fig = px.pie(df_resumo, values='total', names='categoria',
                     title="Distribuição de Riscos por Categoria")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado disponível para exibição.")

    # ---------------------- Lista de Riscos Recentes ----------------------
    st.subheader("📋 Últimos Riscos Identificados")
    query_riscos = """
        SELECT id_risco, nome_risco, descricao, impacto_estimado, probabilidade, status, data_identificacao 
        FROM riscos 
        ORDER BY data_identificacao DESC 
        LIMIT 10
    """
    df_riscos = consultar_dados(query_riscos)

    if not df_riscos.empty:
        st.dataframe(df_riscos, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum risco recente encontrado.")

    # ---------------------- Exportação ----------------------
    if not df_riscos.empty:
        excel_file = gerar_excel(df_riscos)
        st.download_button(
            label="📥 Baixar Relatório Completo de Riscos",
            data=excel_file,
            file_name="Painel_Gestao_Riscos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


if __name__ == "__main__":
    main()
