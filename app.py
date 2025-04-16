import streamlit as st

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Gestão de Riscos", layout="wide")
st.title("📊 Sistema de Gestão de Riscos")

# ---------------------- Navegação por Fases via Radio ----------------------
page = st.sidebar.radio(
    "Navegação por Fases",
    [
        "Tela Inicial - Painel de Riscos",
        "Fase 2 - Identificação de Riscos",
        "Fase 3 - Avaliação de Riscos",
        "Fase 4 - Resposta ao Risco",
        "Fase 5 - Plano de Controle",
        "Fase 6 - Validação do Plano",
        "Fase 7 - Monitoramento",
        "Gerenciamento de Usuários"
    ],
    index=1  # Define como padrão a Fase 2 - Identificação de Riscos
)

if page == "Tela Inicial - Painel de Riscos":
    from pages.app_painel_riscos import main as painel_riscos
    painel_riscos()

elif page == "Fase 2 - Identificação de Riscos":
    from pages.riscos_identificacao import main as riscos_identificacao
    riscos_identificacao()

elif page == "Fase 3 - Avaliação de Riscos":
    from pages.riscos_avaliacao import main as riscos_avaliacao
    riscos_avaliacao()

elif page == "Fase 4 - Resposta ao Risco":
    from pages.app_resposta_risco import main as resposta_risco
    resposta_risco()

elif page == "Fase 5 - Plano de Controle":
    from pages.app_plano_controle import main as plano_controle
    plano_controle()

elif page == "Fase 6 - Validação do Plano":
    from pages.app_validacao_plano import main as validacao_plano
    validacao_plano()

elif page == "Fase 7 - Monitoramento":
    from pages.app_monitoramento import main as monitoramento
    monitoramento()

elif page == "Gerenciamento de Usuários":
    from pages.app_usuarios import main as usuarios
    usuarios()

# ---------------------- Rodapé ----------------------
st.markdown("""
---
📌 **Sistema de Gestão de Riscos** - Desenvolvido para análise e mitigação de riscos empresariais
""")
