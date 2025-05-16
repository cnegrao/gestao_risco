import streamlit as st
from database_utils import run_query, run_select

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Identificação de Riscos", layout="wide")
st.title("⚠️ Identificação de Riscos")

# ---------------------- Cadastro de Riscos ----------------------
st.subheader("📌 Cadastro e Detalhamento do Risco")

# Formulário para inserção de riscos
nome_risco = st.text_input("Nome do Risco")
descricao = st.text_area("Descrição do Risco")
categoria = st.selectbox(
    "Categoria do Risco",
    ["Operacional", "Financeiro", "Tecnológico", "Legal", "Estratégico"],
)
causas = st.text_area("Causas (separadas por vírgula)")
consequencias = st.text_area("Consequências (separadas por vírgula)")

if st.button("💾 Salvar Risco"):
    if nome_risco and descricao:
        query = """
        INSERT INTO riscos (nome_risco, descricao, categoria, causas, consequencias, data_identificacao)
        VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
        """
        run_query(query, (nome_risco, descricao, categoria, causas, consequencias))
        st.success("✅ Risco cadastrado com sucesso!")
    else:
        st.warning("⚠️ Preencha todos os campos obrigatórios.")

# ---------------------- Lista de Riscos Cadastrados ----------------------
st.subheader("📋 Riscos Identificados")

query_listagem = """
    SELECT nome_risco, categoria, descricao, causas, consequencias, data_identificacao
    FROM riscos
    ORDER BY data_identificacao DESC
"""
df_riscos = run_select(query_listagem)

if not df_riscos.empty:
    st.dataframe(df_riscos, use_container_width=True)
else:
    st.info("Nenhum risco cadastrado até o momento.")

st.markdown("---")
st.write("📊 Utilize esta tela para registrar e acompanhar os riscos organizacionais.")

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para acessar outras funcionalidades.")
