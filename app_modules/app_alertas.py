import smtplib
from email.mime.text import MIMEText

import streamlit as st
from database_utils import run_select

# ---------------------- Configuração Inicial ----------------------
st.set_page_config(page_title="Gestão de Riscos - Alertas", layout="wide")

# Função principal


def main():
    st.title("🚨 Alertas e Notificações de Riscos")

    # ---------------------- Consulta de Alertas ----------------------
    st.subheader("🔍 Riscos Críticos e Alertas")

    query_alertas = """
        SELECT id_risco, nome_risco, descricao, impacto_estimado, probabilidade, status, data_identificacao 
        FROM riscos 
        WHERE status IN ('Aberto', 'Em Análise') AND impacto_estimado > 50000 AND probabilidade > 0.7
        ORDER BY data_identificacao DESC
    """
    df_alertas = run_select(query_alertas)

    if df_alertas.empty:
        st.success("✅ Nenhum alerta crítico no momento.")
    else:
        st.warning("⚠️ Existem riscos críticos que requerem atenção!")
        st.dataframe(df_alertas, use_container_width=True)

    # ---------------------- Configuração de Notificações ----------------------
    st.subheader("📢 Configuração de Notificações")

    email_alerta = st.text_input("📧 Email para receber alertas")
    tipo_alerta = st.selectbox("Tipo de Alerta", ["Todos", "Críticos", "Encerrados"])
    frequencia_alerta = st.selectbox("Frequência de Notificação", ["Imediato", "Diário", "Semanal"])

    # Função para envio de email
    def enviar_email(destinatario, assunto, mensagem):
        remetente = "seu_email@example.com"  # Configurar email de envio
        senha = "sua_senha"  # Configurar senha do email

        msg = MIMEText(mensagem)
        msg["Subject"] = assunto
        msg["From"] = remetente
        msg["To"] = destinatario

        try:
            with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
                server.login(remetente, senha)
                server.sendmail(remetente, destinatario, msg.as_string())
            st.success("📧 Email de alerta enviado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao enviar email: {e}")

    if st.button("💾 Salvar Configuração"):
        st.success("✅ Configuração salva! Você receberá alertas no email informado.")

        # Simulação de envio de alerta por email
        if email_alerta:
            assunto = f"[Alerta de Risco] Notificação de Risco {tipo_alerta}"
            mensagem = f"Existem riscos {tipo_alerta.lower()} identificados no sistema. Frequência de notificação: {frequencia_alerta}. Acesse o painel para mais detalhes."
            enviar_email(email_alerta, assunto, mensagem)


if __name__ == "__main__":
    main()
