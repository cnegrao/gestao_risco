import pandas as pd
import streamlit as st
from database_utils import run_query, run_select

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Monitoramento de Riscos", layout="wide")
st.title("📡 Monitoramento e Acompanhamento de Riscos")

# ---------------------- Atualização de Status ----------------------
st.subheader("📌 Atualização de Status das Ações")

query_acoes = "SELECT id_plano, descricao_plano FROM planos_acao WHERE status IN ('Aprovado', 'Em Execução') ORDER BY prazo_execucao ASC"
df_acoes = run_select(query_acoes)

if df_acoes.empty:
    st.warning("⚠️ Nenhuma ação em andamento para monitoramento.")
else:
    acao_selecionada = st.selectbox(
        "Selecione uma Ação para Atualizar", df_acoes["descricao_plano"]
    )
    id_acao = df_acoes[df_acoes["descricao_plano"] == acao_selecionada]["id_plano"].values[0]

    novo_status = st.selectbox(
        "Novo Status", ["Iniciado", "Em Andamento", "Concluído", "Cancelado"]
    )
    observacoes = st.text_area("Observações sobre a Ação")
    data_acompanhamento = st.date_input(
        "Data do Acompanhamento", min_value=pd.to_datetime("today").date()
    )

    if st.button("💾 Atualizar Status"):
        query = """
        UPDATE planos_acao 
        SET status = %s, observacoes = %s, data_acompanhamento = %s 
        WHERE id_plano = %s
        """
        run_query(query, (novo_status, observacoes, data_acompanhamento, id_acao))
        st.success("✅ Status atualizado com sucesso!")

# ---------------------- Exibição do Monitoramento ----------------------
st.subheader("📋 Histórico de Monitoramento")

query_monitoramento = """
    SELECT descricao_plano, status, observacoes, prazo_execucao, data_acompanhamento 
    FROM planos_acao
    WHERE status IN ('Iniciado', 'Em Andamento', 'Concluído', 'Cancelado')
    ORDER BY data_acompanhamento DESC
"""
df_monitoramento = run_select(query_monitoramento)

if not df_monitoramento.empty:
    st.dataframe(df_monitoramento, use_container_width=True)
else:
    st.info("Nenhum acompanhamento registrado até o momento.")

st.markdown("---")
st.write(
    "📊 Utilize esta tela para monitorar a execução das ações de mitigação e acompanhar o progresso dos planos de controle."
)

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para acessar outras funcionalidades.")
