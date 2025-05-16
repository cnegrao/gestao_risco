import streamlit as st
from database_utils import run_query, run_select

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Validação do Plano de Controle", layout="wide")
st.title("✅ Validação do Plano de Controle")

# ---------------------- Seleção do Plano ----------------------
st.subheader("📌 Selecione um Plano de Controle para Validação")

query_planos = "SELECT id_plano, descricao_plano FROM planos_acao WHERE status = 'Pendente' ORDER BY prazo_execucao ASC"
df_planos = run_select(query_planos)

if df_planos.empty:
    st.warning("⚠️ Nenhum plano pendente para validação.")
else:
    plano_selecionado = st.selectbox(
        "Selecione um Plano para Validação", df_planos["descricao_plano"]
    )
    id_plano = df_planos[df_planos["descricao_plano"] == plano_selecionado]["id_plano"].values[0]

    avaliacao = st.selectbox("Avaliação do Gestor", ["Aprovado", "Reprovado"])
    justificativa = st.text_area("Justificativa (obrigatória em caso de reprovação)")

    if st.button("💾 Registrar Validação"):
        if avaliacao == "Reprovado" and not justificativa:
            st.warning("⚠️ Justificativa obrigatória para reprovação do plano.")
        else:
            query = """
            UPDATE planos_acao 
            SET status = %s, justificativa = %s 
            WHERE id_plano = %s
            """
            run_query(query, (avaliacao, justificativa, id_plano))
            st.success("✅ Validação registrada com sucesso!")

# ---------------------- Exibição das Validações ----------------------
st.subheader("📋 Histórico de Validações")

query_validacoes = """
    SELECT descricao_plano, status, justificativa, prazo_execucao 
    FROM planos_acao
    WHERE status IN ('Aprovado', 'Reprovado')
    ORDER BY prazo_execucao DESC
"""
df_validacoes = run_select(query_validacoes)

if not df_validacoes.empty:
    st.dataframe(df_validacoes, use_container_width=True)
else:
    st.info("Nenhuma validação registrada até o momento.")

st.markdown("---")
st.write(
    "📊 Utilize esta tela para validar planos de controle e garantir a efetividade da gestão de riscos."
)

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para acessar outras funcionalidades.")
