import streamlit as st

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Gestão de Riscos", layout="wide")
st.title("📊 Sistema de Gestão de Riscos")

# ---------------------- Barra de Navegação Vertical ----------------------
st.sidebar.header("Navegação por Fases")

if st.sidebar.button("🏠 Tela Inicial - Painel de Riscos"):
    from app_painel_riscos import main as painel_riscos
    painel_riscos()

if st.sidebar.button("🔍 Fase 2 - Identificação de Riscos"):
    from app_riscos import main as riscos
    riscos()

if st.sidebar.button("📊 Fase 3 - Avaliação de Riscos"):
    from app_avaliacao_riscos import main as avaliacao_riscos
    avaliacao_riscos()

if st.sidebar.button("🛡️ Fase 4 - Resposta ao Risco"):
    from app_resposta_risco import main as resposta_risco
    resposta_risco()

if st.sidebar.button("📑 Fase 5 - Plano de Controle"):
    from app_plano_controle import main as plano_controle
    plano_controle()

if st.sidebar.button("✅ Fase 6 - Validação do Plano"):
    from app_validacao_plano import main as validacao_plano
    validacao_plano()

if st.sidebar.button("📡 Fase 7 - Monitoramento"):
    from app_monitoramento import main as monitoramento
    monitoramento()

if st.sidebar.button("👤 Gerenciamento de Usuários"):
    from app_usuarios import main as usuarios
    usuarios()

# ---------------------- Rodapé ----------------------
st.markdown("""
---
📌 **Sistema de Gestão de Riscos** - Desenvolvido para análise e mitigação de riscos empresariais
""")

if __name__ == "__main__":
    st.write("Selecione uma fase no menu lateral para começar.")
