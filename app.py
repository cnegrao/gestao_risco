import streamlit as st

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Gestão de Riscos", layout="wide")
st.title("📊 Sistema de Gestão de Riscos")

# ---------------------- Barra de Navegação Horizontal ----------------------
menu = st.columns(7)

if menu[0].button("🏠 Tela Inicial"):
    from app_painel_riscos import main as painel_riscos
    painel_riscos()

if menu[1].button("🔍 Identificação de Riscos"):
    from app_riscos import main as riscos
    riscos()

if menu[2].button("📊 Avaliação de Riscos"):
    from app_avaliacao_riscos import main as avaliacao_riscos
    avaliacao_riscos()

if menu[3].button("🛡️ Resposta ao Risco"):
    from app_resposta_risco import main as resposta_risco
    resposta_risco()

if menu[4].button("📑 Plano de Controle"):
    from app_plano_controle import main as plano_controle
    plano_controle()

if menu[5].button("✅ Validação do Plano"):
    from app_validacao_plano import main as validacao_plano
    validacao_plano()

if menu[6].button("📡 Monitoramento"):
    from app_monitoramento import main as monitoramento
    monitoramento()

# ---------------------- Rodapé ----------------------
st.markdown("""
---
📌 **Sistema de Gestão de Riscos** - Desenvolvido para análise e mitigação de riscos empresariais
""")

if __name__ == "__main__":
    st.write("Selecione uma fase no menu acima para começar.")
