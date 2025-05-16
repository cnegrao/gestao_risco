import streamlit as st
from database_utils import run_query, run_select

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Resposta ao Risco", layout="wide")
st.title("🛡️ Resposta ao Risco")

# ---------------------- Seleção do Risco ----------------------
st.subheader("📌 Escolha um Risco para Definir a Estratégia de Resposta")

query_riscos = "SELECT id_risco, nome_risco FROM riscos WHERE nivel_risco IS NOT NULL ORDER BY nivel_risco DESC"
df_riscos = run_select(query_riscos)

if df_riscos.empty:
    st.warning("⚠️ Nenhum risco avaliado disponível para resposta.")
else:
    risco_selecionado = st.selectbox("Selecione um Risco para Resposta", df_riscos["nome_risco"])
    id_risco = df_riscos[df_riscos["nome_risco"] == risco_selecionado]["id_risco"].values[0]

    estrategia = st.selectbox(
        "Estratégia de Resposta", ["Evitar", "Reduzir", "Compartilhar", "Aceitar"]
    )
    justificativa = st.text_area("Justificativa para a escolha da estratégia")

    if st.button("💾 Salvar Resposta ao Risco"):
        query = """
        UPDATE riscos 
        SET estrategia_resposta = %s, justificativa_resposta = %s
        WHERE id_risco = %s
        """
        run_query(query, (estrategia, justificativa, id_risco))
        st.success("✅ Resposta ao risco registrada com sucesso!")

# ---------------------- Exibição das Estratégias de Resposta ----------------------
st.subheader("📋 Estratégias de Resposta Registradas")

query_respostas = """
    SELECT nome_risco, estrategia_resposta, justificativa_resposta 
    FROM riscos
    WHERE estrategia_resposta IS NOT NULL
    ORDER BY nome_risco
"""
df_respostas = run_select(query_respostas)

if not df_respostas.empty:
    st.dataframe(df_respostas, use_container_width=True)
else:
    st.info("Nenhuma estratégia de resposta registrada até o momento.")

st.markdown("---")
st.write("📊 Utilize esta tela para definir estratégias eficazes de resposta ao risco.")

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para acessar outras funcionalidades.")
