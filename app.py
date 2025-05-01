# app.py
import streamlit as st
from pathlib import Path

# 1️⃣ Página config — DEVE vir antes de QUALQUER coisa do Streamlit
st.set_page_config(
    page_title="SAFEBIS - Sistema de Gestão de Riscos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2️⃣ Injeção do CSS (assets/style.css)
css_file = Path(__file__).parent / "assets" / "style.css"
if css_file.exists():
    css = css_file.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
else:
    st.error("🛑 assets/style.css não encontrado!")

# 3️⃣ Sidebar: logo + menu
with st.sidebar:
    logo = Path(__file__).parent / "imagens" / "logo.png"
    if not logo.exists():
        logo = Path(__file__).parent / "imagens" / "logo.jpg"
    if logo.exists():
        st.image(str(logo), use_column_width=True)
    st.markdown("## Navegação por Fases")
    page = st.radio(
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

# 4️⃣ Top-Bar full width
st.markdown(
    """
    <div class="top-bar">
      <h2>SAFEBIS – Sistema de Gestão de Riscos</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# 5️⃣ Container do conteúdo principal (empurrado pra baixo)
main = st.container()
main.markdown('<div class="main-content">', unsafe_allow_html=True)

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

main.markdown("</div>", unsafe_allow_html=True)

# 6️⃣ Rodapé
st.markdown(
    """
    <footer>
      &copy; 2025 SAFEBIS – Todos os direitos reservados
    </footer>
    """,
    unsafe_allow_html=True
)
