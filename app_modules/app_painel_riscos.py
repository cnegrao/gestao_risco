import streamlit as st
import pandas as pd
from database_utils import run_select, run_query
import datetime

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Painel de Gestão de Riscos", layout="wide")
st.title("📊 Painel de Gestão de Riscos")

# ---------------------- Resumo de Riscos ----------------------
st.subheader("📌 Visão Geral dos Riscos")

query_resumo = """
    SELECT categoria, COUNT(*) AS total
    FROM riscos
    GROUP BY categoria
"""
df_resumo = run_select(query_resumo)

if not df_resumo.empty:
    st.bar_chart(df_resumo.set_index("categoria"))
else:
    st.warning("Nenhum dado disponível para exibição.")

# ---------------------- Alertas e Prazos ----------------------
st.subheader("⚠️ Alertas e Prazos Críticos")

query_alertas = """
    SELECT nome_risco, impacto_estimado, probabilidade, status, data_identificacao 
    FROM riscos 
    WHERE status IN ('Aberto', 'Em Análise') 
    AND impacto_estimado > 50000 AND probabilidade > 0.7
    ORDER BY data_identificacao DESC
"""
df_alertas = run_select(query_alertas)

if df_alertas.empty:
    st.success("✅ Nenhum alerta crítico no momento.")
else:
    st.error("🚨 Existem riscos críticos que requerem atenção!")
    st.dataframe(df_alertas, use_container_width=True)

# ---------------------- Monitoramento e Insights Preditivos ----------------------
st.subheader("🧠 Insights Preditivos sobre Riscos")

query_insights = """
    SELECT nome_risco, categoria, impacto_estimado, probabilidade
    FROM riscos
    WHERE impacto_estimado > 40000
    ORDER BY probabilidade DESC
    LIMIT 5
"""
df_insights = run_select(query_insights)

if not df_insights.empty:
    st.dataframe(df_insights, use_container_width=True)
else:
    st.info("Nenhum risco de alto impacto detectado.")

st.markdown("---")
st.write("🔍 O painel de gestão de riscos exibe análises preditivas e permite uma visão estratégica dos riscos em tempo real.")

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para acessar módulos específicos.")
