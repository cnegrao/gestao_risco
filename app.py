import streamlit as st
from pathlib import Path
import os

# ─── 1) Configuração de Página ───────────────────────────────────────────────
st.set_page_config(
    page_title="SAFEBIS – Sistema de Gestão de Riscos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── 2) Injeta o CSS de assets/style.css ────────────────────────────────────
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Não encontrei assets/style.css")

# ─── 3) Logo na Sidebar ─────────────────────────────────────────────────────
logo_path = Path(__file__).parent / "imagens" / "logo.jpeg"
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)
else:
    st.sidebar.markdown(
        "<div class='sidebar-logo-placeholder'></div>",
        unsafe_allow_html=True
    )

# ─── 4) Navegação ────────────────────────────────────────────────────────────
st.sidebar.markdown("## Navegação por Fases")
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

# ─── 5) Top Bar ───────────────────────────────────────────────────────────────
st.markdown(
    '<div class="top-bar">'
    '  <h2>SAFEBIS – Sistema de Gestão de Riscos</h2>'
    '</div>',
    unsafe_allow_html=True
)

# ─── 6) Rotas ─────────────────────────────────────────────────────────────────
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

# ─── 7) Rodapé ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <footer class="footer">
      &copy; 2025 SAFEBIS — Todos os direitos reservados
    </footer>
    """,
    unsafe_allow_html=True
)
