import streamlit as st
from database_utils import run_select
import pandas as pd
import io

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Gestão de Riscos - Visualização", layout="wide")

# Função principal


def main():
    st.title("📊 Visualização de Riscos")

    # ---------------------- Funções Auxiliares ----------------------
    @st.cache_data
    def consultar_dados(query):
        """Executa uma consulta SQL e retorna os dados como DataFrame."""
        return run_select(query)

    def gerar_excel(df, sheet_name="Riscos"):
        """Gera um arquivo Excel com os dados fornecidos."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        return output

    # ---------------------- Interface Principal ----------------------
    st.sidebar.header("Filtros de Risco")

    # 🔹 Seleção de Categoria de Risco
    categoria = st.sidebar.selectbox("Selecione a Categoria de Risco", [
                                     "Operacional", "Financeiro", "Tecnológico", "Legal", "Estratégico"])

    # 🔹 Filtro de Status do Risco
    status = st.sidebar.selectbox(
        "Status do Risco", ["Aberto", "Em Análise", "Mitigado", "Encerrado"])

    # 🔹 Botão para Buscar Dados
    if st.sidebar.button("🔍 Buscar Riscos"):
        query = f"""
        SELECT id_risco, nome_risco, descricao, impacto_estimado, probabilidade, status, data_identificacao 
        FROM riscos 
        WHERE categoria = '{categoria}' AND status = '{status}'
        ORDER BY data_identificacao DESC"""
        df_riscos = consultar_dados(query)

        if df_riscos.empty:
            st.warning(
                "⚠️ Nenhum risco encontrado para os filtros selecionados.")
        else:
            st.subheader("📋 Riscos Identificados")
            st.dataframe(df_riscos, use_container_width=True)

            # Exportação para Excel
            excel_file = gerar_excel(df_riscos)
            st.download_button(
                label="📥 Baixar Relatório Excel",
                data=excel_file,
                file_name="Relatorio_Riscos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


if __name__ == "__main__":
    main()
