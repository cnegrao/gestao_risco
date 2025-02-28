import streamlit as st
from database_utils import run_select
import pandas as pd

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Atualização de Planos de Ação", layout="wide")
st.title("🔄 Atualização de Planos de Ação")

# ---------------------- Seleção do Plano ----------------------
st.subheader("Selecione um Plano de Ação para Atualizar")
query_planos = """
    SELECT id_plano, descricao_plano, responsavel, status FROM planos_acao
    ORDER BY prazo_execucao ASC
"""
df_planos = run_select(query_planos)

if df_planos.empty:
    st.warning("⚠️ Nenhum plano encontrado.")
else:
    plano_selecionado = st.selectbox(
        "Escolha um Plano", df_planos["descricao_plano"])
    id_plano = df_planos[df_planos["descricao_plano"]
                         == plano_selecionado]["id_plano"].values[0]
    novo_status = st.selectbox(
        "Novo Status", ["Pendente", "Em Execução", "Concluído"])
    observacoes = st.text_area("Observações (Opcional)")

    # Botão para atualizar o plano
    if st.button("✅ Atualizar Plano"):
        query_update = f"""
        UPDATE planos_acao
        SET status = '{novo_status}', observacoes = '{observacoes}'
        WHERE id_plano = {id_plano}
        """
        try:
            run_select(query_update)
            st.success("✅ Plano atualizado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao atualizar plano: {e}")
