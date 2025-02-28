import streamlit as st
from database_utils import run_select
import pandas as pd

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Cadastro de Riscos", layout="wide")
st.title("📝 Cadastro de Novos Riscos")

# Função principal


def main():
    # ---------------------- Formulário de Cadastro ----------------------
    st.subheader("Preencha os dados do novo risco")

    nome_risco = st.text_input("Nome do Risco")
    descricao = st.text_area("Descrição")
    categoria = st.selectbox(
        "Categoria", ["Operacional", "Financeiro", "Tecnológico", "Legal", "Estratégico"])
    impacto = st.number_input("Impacto Estimado (R$)",
                              min_value=0.0, format="%.2f")
    probabilidade = st.slider("Probabilidade de Ocorrência", 0.0, 1.0, 0.5)
    status = st.selectbox(
        "Status", ["Aberto", "Em Análise", "Mitigado", "Encerrado"])

    # ---------------------- Listagem de Riscos Cadastrados ----------------------
    st.subheader("📋 Riscos Cadastrados")
    query_listagem = """
        SELECT id_risco, nome_risco, categoria, impacto_estimado, probabilidade, status, data_identificacao
        FROM riscos
        ORDER BY data_identificacao DESC
    """
    df_riscos = run_select(query_listagem)

    if df_riscos.empty:
        st.warning("⚠️ Nenhum risco cadastrado ainda.")
    else:
        st.dataframe(df_riscos, use_container_width=True)

    # ---------------------- Botão para salvar o risco ----------------------
    if st.button("💾 Salvar Risco"):
        if nome_risco and descricao:
            query = f"""
            INSERT INTO riscos (nome_risco, descricao, categoria, impacto_estimado, probabilidade, status, data_identificacao)
            VALUES ('{nome_risco}', '{descricao}', '{categoria}', {impacto}, {probabilidade}, '{status}', CURRENT_DATE)
            """
            try:
                run_select(query)
                st.success("✅ Risco cadastrado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar risco: {e}")
        else:
            st.warning("⚠️ Preencha todos os campos obrigatórios.")


if __name__ == "__main__":
    main()
