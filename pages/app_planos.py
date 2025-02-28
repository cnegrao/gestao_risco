import streamlit as st
from database_utils import run_select
import pandas as pd
import io

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(
    page_title="Gestão de Riscos - Planos de Ação", layout="wide")

# Função principal


def main():
    st.title("🛠️ Planos de Ação para Mitigação de Riscos")

    # ---------------------- Funções Auxiliares ----------------------
    @st.cache_data
    def consultar_dados(query):
        """Executa uma consulta SQL e retorna os dados como DataFrame."""
        return run_select(query)

    def gerar_excel(df, sheet_name="Planos"):
        """Gera um arquivo Excel com os dados fornecidos."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        return output

    # ---------------------- Interface Principal ----------------------
    st.sidebar.header("Filtros de Planos de Ação")

    # 🔹 Seleção de Status do Plano de Ação
    status_plano = st.sidebar.selectbox(
        "Status do Plano", ["Pendente", "Em Execução", "Concluído"])

    # 🔹 Botão para Buscar Dados
    if st.sidebar.button("🔍 Buscar Planos"):
        query = f"""
        SELECT id_plano, descricao_plano, id_risco, prazo_execucao, responsavel, custo_estimado, status 
        FROM planos_acao 
        WHERE status = '{status_plano}'
        ORDER BY prazo_execucao ASC"""
        df_planos = consultar_dados(query)

        if df_planos.empty:
            st.warning(
                "⚠️ Nenhum plano encontrado para os filtros selecionados.")
        else:
            st.subheader("📋 Planos de Ação")
            st.dataframe(df_planos, use_container_width=True)

            # Exportação para Excel
            excel_file = gerar_excel(df_planos)
            st.download_button(
                label="📥 Baixar Relatório Excel",
                data=excel_file,
                file_name="Relatorio_Planos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


if __name__ == "__main__":
    main()
