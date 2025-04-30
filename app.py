import streamlit as st
from PIL import Image
import os

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(
    page_title="SAFEBIS - Sistema de Gestão de Riscos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho para o logo (ajuste se necessário)
# Caminho para o logo (ajuste se necessário)
# Usuário informou que a imagem está em /imagens/logo.ppg (provavelmente logo.png)
logo_dir = os.path.join(os.path.dirname(__file__), 'imagens')
# Tenta png, jpg e ppg
for fname in ['logo.png', 'logo.jpg', 'logo.ppg']:
    logo_path = os.path.join(logo_dir, fname)
    if os.path.exists(logo_path):
        break
else:
    logo_path = None  # não encontrado
# ===================== Logo na Barra Lateral ====================
# Exibe o logo no topo da sidebar
if logo_path:
    st.sidebar.image(logo_path, width=100)
else:
    st.sidebar.markdown(
        "<div style='width:100px;height:100px;background-color:#ccc;border-radius:8px;margin-bottom:10px;'></div>",
        unsafe_allow_html=True
    )

# ===================== Navegação ====================
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
    index=1
)

# ===================== Rotas ====================
if page == "Tela Inicial - Contexto de Riscos":
    from pages.riscos_dash import main as riscos_dash
    riscos_dash()

elif page == "Fase 2 - Identificação de Riscos":
    from pages.riscos_identificacao import main as riscos_identificacao
    riscos_identificacao()

elif page == "Fase 3 - Avaliação de Riscos":
    from pages.riscos_avaliacao import main as riscos_avaliacao
    riscos_avaliacao()

elif page == "Fase 4 - Resposta ao Risco":
    from pages.app_resposta_risco import main as resposta_risco
    resposta_risco()

elif page == "Fase 5 - Plano de Tratamento de Risco":
    from pages.app_plano_controle import main as plano_controle
    plano_controle()

elif page == "Fase 7 - Dashboard de Riscos":
    from pages.app_monitoramento import main as monitoramento
    monitoramento()

elif page == "Gerenciamento de Usuários":
    from pages.app_usuarios import main as usuarios
    usuarios()

# ===================== Rodapé =====================
st.markdown("""
---
<p style='text-align:center; color:#666;'>
&copy; 2025 SAFEBIS - Todos os direitos reservados
</p>
""", unsafe_allow_html=True)
