import streamlit as st

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Documentação do Sistema", layout="wide")
st.title("📘 Documentação do Sistema de Gestão de Riscos")

# ---------------------- Modelo 5W2H ----------------------

st.markdown("""
## 📌 Visão Geral
Este sistema foi desenvolvido para auxiliar na **gestão de riscos empresariais**, permitindo o **monitoramento, mitigação e auditoria** de riscos organizacionais. 

Cada módulo segue o **modelo 5W2H**, detalhando os principais aspectos do sistema.

---
## 🏠 **Painel de Riscos**
- **What (O que?)**: Exibe gráficos interativos e estatísticas sobre os riscos cadastrados no sistema.
- **Why (Por quê?)**: Para fornecer uma visão analítica dos riscos e priorizar ações.
- **Where (Onde?)**: Tela inicial do sistema.
- **When (Quando?)**: Sempre que o usuário desejar uma visão geral dos riscos.
- **Who (Quem?)**: Gestores de risco e equipe de compliance.
- **How (Como?)**: Apresenta gráficos dinâmicos e relatórios interativos.
- **How Much (Quanto?)**: Gratuito para usuários do sistema.

---
## ⚠️ **Riscos**
- **What (O que?)**: Lista os riscos cadastrados, permitindo filtros por categoria e status.
- **Why (Por quê?)**: Para visualizar e gerenciar os riscos de forma eficiente.
- **Where (Onde?)**: Módulo de riscos no menu do sistema.
- **When (Quando?)**: Sempre que for necessária a consulta ou atualização de um risco.
- **Who (Quem?)**: Analistas de risco e gestores.
- **How (Como?)**: Através de filtros, listagens e exportação de dados.
- **How Much (Quanto?)**: Sem custo adicional.

---
## 🛠️ **Planos de Ação**
- **What (O que?)**: Gerencia planos de mitigação de riscos, permitindo acompanhar status e progresso.
- **Why (Por quê?)**: Para reduzir a probabilidade e impacto dos riscos.
- **Where (Onde?)**: Módulo de planos de ação.
- **When (Quando?)**: Sempre que for necessário definir ou atualizar uma ação.
- **Who (Quem?)**: Equipe responsável pela mitigação de riscos.
- **How (Como?)**: Permite cadastrar, acompanhar e exportar ações.
- **How Much (Quanto?)**: Incluso no sistema.

---
## 📈 **Indicadores**
- **What (O que?)**: Apresenta métricas e KPIs sobre a gestão de riscos.
- **Why (Por quê?)**: Para medir a eficácia das ações implementadas.
- **Where (Onde?)**: Tela de Indicadores no menu.
- **When (Quando?)**: Sempre que for necessário acompanhar métricas de desempenho.
- **Who (Quem?)**: Tomadores de decisão e analistas.
- **How (Como?)**: Mostra gráficos e KPIs baseados nos dados.
- **How Much (Quanto?)**: Incluso no sistema.

---
## 🔎 **Auditoria**
- **What (O que?)**: Registro detalhado de logs e ações realizadas no sistema.
- **Why (Por quê?)**: Para garantir conformidade e rastreabilidade de ações.
- **Where (Onde?)**: Módulo de Auditoria.
- **When (Quando?)**: Sempre que for necessário consultar atividades do sistema.
- **Who (Quem?)**: Equipes de governança e segurança.
- **How (Como?)**: Listagem detalhada de logs filtráveis.
- **How Much (Quanto?)**: Sem custos adicionais.

---
## 🚨 **Alertas**
- **What (O que?)**: Monitora riscos críticos e permite configurar notificações por e-mail.
- **Why (Por quê?)**: Para garantir que riscos urgentes sejam rapidamente identificados e tratados.
- **Where (Onde?)**: Módulo de Alertas no menu.
- **When (Quando?)**: Sempre que houver riscos de alta criticidade.
- **Who (Quem?)**: Gestores e equipes de resposta a crises.
- **How (Como?)**: Através da listagem de riscos críticos e envio automático de alertas.
- **How Much (Quanto?)**: Custo variável conforme necessidade de notificações externas.

---

Se precisar de mais detalhes, estamos prontos para ajudar! 🚀
""")

if __name__ == "__main__":
    st.write("Para acessar cada módulo, utilize o menu lateral do Streamlit.")
