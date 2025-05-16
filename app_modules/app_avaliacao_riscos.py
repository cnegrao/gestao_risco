import streamlit as st
from database_utils import run_query, run_select

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Avaliação de Riscos", layout="wide")
st.title("📊 Avaliação de Riscos")

# ---------------------- Formulário de Avaliação ----------------------
st.subheader("📌 Avaliação de Probabilidade e Impacto")

# Seleção do risco para avaliação
query_riscos = "SELECT id_risco, nome_risco FROM riscos ORDER BY data_identificacao DESC"
df_riscos = run_select(query_riscos)

if df_riscos.empty:
    st.warning("⚠️ Nenhum risco cadastrado para avaliação.")
else:
    risco_selecionado = st.selectbox("Selecione um Risco para Avaliação", df_riscos["nome_risco"])
    id_risco = df_riscos[df_riscos["nome_risco"] == risco_selecionado]["id_risco"].values[0]

    probabilidade = st.slider("Probabilidade de Ocorrência (1 a 5)", 1, 5, 3)
    impacto = st.selectbox("Impacto do Risco", ["Baixo", "Médio", "Alto", "Crítico"])
    nivel_risco = probabilidade * (
        1 if impacto == "Baixo" else 2 if impacto == "Médio" else 3 if impacto == "Alto" else 4
    )

    if st.button("💾 Salvar Avaliação"):
        query = """
        UPDATE riscos 
        SET probabilidade = %s, impacto = %s, nivel_risco = %s 
        WHERE id_risco = %s
        """
        run_query(query, (probabilidade, impacto, nivel_risco, id_risco))
        st.success("✅ Avaliação salva com sucesso!")

# ---------------------- Exibição das Avaliações ----------------------
st.subheader("📋 Avaliações Realizadas")

query_avaliacoes = """
    SELECT nome_risco, probabilidade, impacto, nivel_risco 
    FROM riscos
    WHERE probabilidade IS NOT NULL AND impacto IS NOT NULL
    ORDER BY nivel_risco DESC
"""
df_avaliacoes = run_select(query_avaliacoes)

if not df_avaliacoes.empty:
    st.dataframe(df_avaliacoes, use_container_width=True)
else:
    st.info("Nenhuma avaliação de risco realizada até o momento.")

st.markdown("---")
st.write("📊 Utilize esta tela para avaliar riscos e definir estratégias de mitigação.")

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para acessar outras funcionalidades.")
