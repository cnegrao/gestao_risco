import streamlit as st
import pandas as pd
from database_utils import run_select, run_query

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Plano de Controle", layout="wide")
st.title("📑 Plano de Controle de Riscos")

# ---------------------- Cadastro de Ações de Controle ----------------------
st.subheader("📌 Definição de Ações para Mitigação")

query_riscos = "SELECT id_risco, nome_risco FROM riscos WHERE estrategia_resposta IS NOT NULL ORDER BY nivel_risco DESC"
df_riscos = run_select(query_riscos)

if df_riscos.empty:
    st.warning("⚠️ Nenhum risco disponível para planejamento de controle.")
else:
    risco_selecionado = st.selectbox(
        "Selecione um Risco para Definir Ações de Controle", df_riscos["nome_risco"])
    id_risco = df_riscos[df_riscos["nome_risco"]
                         == risco_selecionado]["id_risco"].values[0]

    descricao_acao = st.text_area("Descrição da Ação de Controle")
    responsavel = st.text_input("Responsável pela Execução")
    prazo_execucao = st.date_input(
        "Prazo para Execução", min_value=pd.to_datetime("today").date())
    custo_estimado = st.number_input(
        "Custo Estimado (R$)", min_value=0.0, format="%.2f")
    beneficio_estimado = st.text_area("Benefício Esperado")

    if st.button("💾 Salvar Plano de Controle"):
        query = """
        INSERT INTO planos_acao (id_risco, descricao_plano, responsavel, prazo_execucao, custo_estimado, beneficio_estimado, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Pendente')
        """
        run_query(query, (id_risco, descricao_acao, responsavel,
                  prazo_execucao, custo_estimado, beneficio_estimado))
        st.success("✅ Plano de Controle registrado com sucesso!")

# ---------------------- Exibição dos Planos de Controle ----------------------
st.subheader("📋 Planos de Controle Definidos")

query_planos = """
    SELECT riscos.nome_risco, planos_acao.descricao_plano, planos_acao.responsavel, planos_acao.prazo_execucao, planos_acao.status
    FROM planos_acao
    JOIN riscos ON planos_acao.id_risco = riscos.id_risco
    ORDER BY planos_acao.prazo_execucao ASC
"""
df_planos = run_select(query_planos)

if not df_planos.empty:
    st.dataframe(df_planos, use_container_width=True)
else:
    st.info("Nenhum plano de controle registrado até o momento.")

st.markdown("---")
st.write("📊 Utilize esta tela para definir e acompanhar ações para mitigação de riscos.")

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para acessar outras funcionalidades.")
