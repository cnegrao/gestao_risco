import importlib

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(
    page_title="Gestão de Riscos - Sistema Principal", layout="wide")
st.title("📊 Sistema de Gestão de Riscos")

# ---------------------- Menu de Navegação ----------------------
menu = st.sidebar.radio("Navegação", [
    "🏠 Painel de Riscos",
    "⚠️ Riscos",
    "🛠️ Planos de Ação",
    "📈 Indicadores",
    "🔎 Auditoria",
    "🚨 Alertas",
    "👤 Usuários",
    "📝 Cadastro de Risco",
    "🔄 Atualização de Planos",
    "📘 Documentação"
])

# ---------------------- Redirecionamento das Páginas ----------------------
pages = {
    "🏠 Painel de Riscos": "pages.app_painel_riscos",
    "⚠️ Riscos": "pages.app_riscos",
    "🛠️ Planos de Ação": "pages.app_planos",
    "📈 Indicadores": "pages.app_indicadores",
    "🔎 Auditoria": "pages.app_auditoria",
    "🚨 Alertas": "pages.app_alertas",
    "👤 Usuários": "pages.app_usuarios",
    "📝 Cadastro de Risco": "pages.app_cadastro_risco",
    "🔄 Atualização de Planos": "pages.app_atualizar_plano",
    "📘 Documentação": "pages.app_menu_documentacao"
}

if menu in pages:
    module = importlib.import_module(pages[menu])
    module.main()

# ---------------------- Rodapé ----------------------
st.markdown("""
---
📌 **Sistema de Gestão de Riscos** - Desenvolvido com ❤️ usando Streamlit
""")

if __name__ == "__main__":
    st.write("Escolha uma opção no menu lateral para começar.")
