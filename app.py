import streamlit as st
import os

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(
    page_title="SAFEBIS - Sistema de Gestão de Riscos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- Logo na Sidebar ----------------------
# Exibe o logo acima da navegação na sidebar
logo_dir = os.path.join(os.path.dirname(__file__), 'imagens')
for fname in ['logo.png', 'logo.jpeg', 'logo.ppg']:
    potential = os.path.join(logo_dir, fname)
    if os.path.exists(potential):
        logo_path = potential
        break
else:
    logo_path = None

if logo_path:
    # Atualizado para usar use_container_width em vez de use_column_width
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.markdown(
        "<div style='width:100%;height:150px;background-color:#ccc;border-radius:8px; margin-bottom:10px;'></div>",
        unsafe_allow_html=True
    )

# ---------------------- Navegação por Fases ----------------------
st.sidebar.markdown("# Navegação por Fases")
page = st.sidebar.radio(
    "",
    [
        "Tela Inicial - Contexto de Riscos",
        "Fase 2 - Identificação de Riscos",
        "Fase 3 - Avaliação de Riscos",
        "Fase 4 - Resposta ao Risco",
        "Fase 5 - Plano de Tratamento de Risco",
        "Fase 7 - Dashboard de Riscos",
        "Gerenciamento de Usuários"
    ],
    index=0
)

# ---------------------- Top Bar ----------------------
# Barra horizontal azul com título, acima do conteúdo principal
st.markdown(
    "<div style='width:100%; background-color:#003366; padding:12px 20px;'>"
    "<h2 style='color:white; margin:0;'>SAFEBIS - Sistema de Gestão de Riscos</h2>"
    "</div>",
    unsafe_allow_html=True
)

# ---------------------- Rotas ----------------------
if page == "Tela Inicial - Contexto de Riscos":
    from app_modules.riscos_dash import main as riscos_dash
    riscos_dash()
elif page == "Fase 2 - Identificação de Riscos":
    from app_modules.riscos_identificacao import main as riscos_identificacao
    riscos_identificacao()
elif page == "Fase 3 - Avaliação de Riscos":
    from app_modules.riscos_avaliacao import main as riscos_avaliacao
    riscos_avaliacao()
elif page == "Fase 4 - Resposta ao Risco":
    from app_modules.app_resposta_risco import main as resposta_risco
    resposta_risco()
elif page == "Fase 5 - Plano de Tratamento de Risco":
    from app_modules.app_plano_controle import main as plano_controle
    plano_controle()
elif page == "Fase 7 - Dashboard de Riscos":
    from app_modules.app_monitoramento import main as monitoramento
    monitoramento()
elif page == "Gerenciamento de Usuários":
    from app_modules.app_usuarios import main as usuarios
    usuarios()

# ---------------------- Rodapé ----------------------
st.markdown(
    """
    ---
    <p style='text-align:center; color:#666;'>
    &copy; 2025 SAFEBIS - Todos os direitos reservados
    </p>
    """,
    unsafe_allow_html=True
)
