import streamlit as st
from database_utils import run_select
import pandas as pd
import io

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Gestão de Riscos - Usuários", layout="wide")

# Função principal


def main():
    st.title("👤 Gerenciamento de Usuários")

    # ---------------------- Funções Auxiliares ----------------------
    @st.cache_data
    def consultar_dados(query):
        """Executa uma consulta SQL e retorna os dados como DataFrame."""
        return run_select(query)

    def gerar_excel(df, sheet_name="Usuarios"):
        """Gera um arquivo Excel com os dados fornecidos."""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        return output

    # ---------------------- Interface Principal ----------------------
    st.sidebar.header("Filtros de Usuários")

    # 🔹 Seleção de Tipo de Usuário
    tipo_usuario = st.sidebar.selectbox(
        "Tipo de Usuário", ["Todos", "Analista", "Gestor", "Administrador"])

    # 🔹 Filtro de Status do Usuário
    status_usuario = st.sidebar.selectbox(
        "Status do Usuário", ["Ativo", "Inativo"])

    # 🔹 Botão para Buscar Dados
    if st.sidebar.button("🔍 Buscar Usuários"):
        query = f"""
        SELECT id_usuario, nome, email, tipo_usuario, ativo 
        FROM usuarios 
        WHERE ativo = {True if status_usuario == "Ativo" else False}
        {f"AND tipo_usuario = '{tipo_usuario}'" if tipo_usuario != "Todos" else ""}
        ORDER BY nome ASC"""
        df_usuarios = consultar_dados(query)

        if df_usuarios.empty:
            st.warning(
                "⚠️ Nenhum usuário encontrado para os filtros selecionados.")
        else:
            st.subheader("📋 Usuários Cadastrados")
            st.dataframe(df_usuarios, use_container_width=True)

            # Exportação para Excel
            excel_file = gerar_excel(df_usuarios)
            st.download_button(
                label="📥 Baixar Relatório Excel",
                data=excel_file,
                file_name="Relatorio_Usuarios.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


if __name__ == "__main__":
    main()
