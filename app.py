from pathlib import Path
import streamlit as st

# 1️⃣ CONFIGURAÇÃO DE PÁGINA (sempre em primeiríssima linha após imports)
st.set_page_config(
    page_title="SafeBis – Sistema de Gestão de Riscos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2️⃣ INJEÇÃO DO CSS
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Não encontrei assets/style.css")

# 3️⃣ LOGO NA SIDEBAR
logo_path = Path(__file__).parent / "imagens" / "logo.jpeg"
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)
else:
    st.sidebar.markdown(
        "<div class='sidebar-logo-placeholder'></div>",
        unsafe_allow_html=True
    )

# 4️⃣ TÍTULO DA SIDEBAR
st.sidebar.markdown("# Navegação por Fases")

# 5️⃣ RÁDIO DE NAVEGAÇÃO
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

# 6️⃣ BARRA SUPERIOR FIXA
st.markdown(
    '<div class="top-bar">'
    '<h2>SafeBis – Sistema de Gestão de Riscos</h2>'
    '</div>',
    unsafe_allow_html=True
)

# 7️⃣ CHAMADA DAS PÁGINAS
if page == "Tela Inicial - Contexto de Riscos":
    from app_modules.riscos_dash import main as riscos_dash
    riscos_dash()
elif page == "Fase 2 - Identificação de Riscos":
    from app_modules.riscos_identificacao import main as riscos_identificacao
    riscos_identificacao()
# ... siga para as demais fases

# 8️⃣ RODAPÉ
st.markdown("""<footer>© 2025 SafeBis – Todos os direitos reservados</footer>""",
            unsafe_allow_html=True)
