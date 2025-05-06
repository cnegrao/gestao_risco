from app_modules.riscos_estrategia_associacao import riscos_estrategia_associacao
from app_modules.riscos_controle_avaliacao import riscos_controle_avaliacao
import sys
import os
import streamlit as st
import pandas as pd
from database_utils import run_select, run_query
import plotly.graph_objs as go

# Ajusta path para módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Importa telas adicionais


def main_avaliacao():
    st.title("Fase 3 – Avaliação de Riscos")
    st.markdown(
        """
        **Objetivo:** Avaliar os riscos cadastrados preenchendo probabilidade (1-5), impactos em três dimensões,
        cálculo de impacto final (máximo), nível do risco e classificação (Pequeno, Moderado, Alto, Crítico).
        """
    )

    # Riscos disponíveis
    df_riscos = run_select(
        "SELECT id_risco, nome_risco, id_empresa FROM tb_riscos ORDER BY data_identificacao DESC"
    )
    if df_riscos.empty:
        st.warning("⚠️ Nenhum risco cadastrado disponível para avaliação.")
        return

    # Seleção de risco
    escolha = st.selectbox("Selecione um risco:",
                           df_riscos['nome_risco'], key='aval_risco')
    row = df_riscos[df_riscos['nome_risco'] == escolha].iloc[0]
    id_r = int(row['id_risco'])
    id_empresa = int(row['id_empresa'])
    st.markdown("---")

    # Estratégia Associada
    st.subheader("Estratégia Associada")
    estr_df = run_select(
        """
        SELECT o.descricao AS Objetivo, m.descricao AS Meta
          FROM tb_risco_meta rm
          JOIN tb_meta_estrategica m ON rm.id_meta = m.id_meta
          JOIN tb_objetivo_estrategico o ON m.id_objetivo = o.id_objetivo
         WHERE rm.id_empresa=%s AND rm.id_risco=%s
         ORDER BY o.id_objetivo, m.id_meta;
        """,
        (id_empresa, id_r)
    )
    if estr_df.empty:
        st.info("Nenhuma estratégia associada a este risco.")
    else:
        st.table(estr_df)

    # Controles Associados
    st.subheader("Controles Associados")
    ctrl_df = run_select(
        """
        SELECT rc.descricao_controle AS Descrição,
               sc.descricao AS Situação,
               ec.descricao AS Execução
          FROM tb_risco_controle rc
          JOIN tb_situacao_controle sc ON rc.id_situacao_controle=sc.id_situacao_controle
          JOIN tb_execucao_controle ec ON rc.id_execucao_controle=ec.id_execucao_controle
         WHERE rc.id_risco=%s
         ORDER BY rc.data_criacao DESC;
        """,
        (id_r,)
    )
    if ctrl_df.empty:
        st.info("Nenhum controle associado a este risco.")
    else:
        st.table(ctrl_df)

    st.markdown("---")

    # Avaliação
    prob = st.slider("Probabilidade (1 a 5)", 1, 5, 3, key='aval_prob')
    col1, col2, col3 = st.columns(3)
    with col1:
        fin = st.slider("Impacto Financeiro", 1, 5, 3, key='aval_fin')
    with col2:
        img = st.slider("Impacto na Imagem", 1, 5, 3, key='aval_img')
    with col3:
        conf = st.slider("Impacto na Conformidade", 1, 5, 3, key='aval_conf')

    imp_final = max(fin, img, conf)
    nivel = prob * imp_final
    if nivel <= 5:
        cls = "Pequeno"
    elif nivel <= 10:
        cls = "Moderado"
    elif nivel <= 15:
        cls = "Alto"
    else:
        cls = "Crítico"

    st.markdown("---")
    st.write(f"**Probabilidade:** {prob}")
    st.write(
        f"**Impactos:** Financeiro={fin}, Imagem={img}, Conformidade={conf}")
    st.write(f"**Impacto Final:** {imp_final} (Fórmula: max(F,I,C))")
    st.write(f"**Nível de Risco:** {nivel} (Fórmula: {prob}×{imp_final})")
    st.write(f"**Classificação:** {cls}")

    if st.button("💾 Salvar Avaliação"):
        try:
            run_query(
                """
                UPDATE tb_riscos
                   SET probabilidade=%s,
                       impacto_financeiro=%s,
                       impacto_imagem=%s,
                       impacto_conformidade=%s,
                       impacto_estimado=%s,
                       nivel_risco=%s,
                       criticidade=%s
                 WHERE id_risco=%s;
                """,
                (prob, fin, img, conf, imp_final, nivel, cls, id_r)
            )
            st.success("✅ Avaliação salva com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao salvar avaliação: {e}")

    st.markdown("---")
    st.subheader("Avaliações Realizadas")
    df_av = run_select(
        """
        SELECT nome_risco, probabilidade, impacto_financeiro, impacto_imagem,
               impacto_conformidade, impacto_estimado, nivel_risco, criticidade, data_identificacao
          FROM tb_riscos
         WHERE probabilidade IS NOT NULL AND impacto_estimado IS NOT NULL
         ORDER BY data_identificacao DESC;
        """
    )
    if df_av is not None and not df_av.empty:
        st.dataframe(df_av, use_container_width=True)
    else:
        st.info("Nenhuma avaliação de risco registrada até o momento.")

    st.markdown("---")
    st.subheader("Matriz de Riscos 5x5")
    # Heatmap
    prob_labels = [str(i) for i in range(1, 6)]
    impact_labels = [str(i) for i in range(1, 6)]
    z = [[(j+1)*(i+1) for j in range(5)] for i in range(5)]
    z_text = [[str(val) for val in row] for row in z]
    colorscale = [
        [0, "green"], [0.2, "green"],
        [0.21, "yellow"], [0.4, "yellow"],
        [0.41, "orange"], [0.6, "orange"],
        [0.61, "red"], [1.0, "red"]
    ]
    fig = go.Figure(go.Heatmap(
        x=prob_labels,
        y=impact_labels,
        z=z,
        text=z_text,
        texttemplate="%{text}",
        hovertemplate="Probabilidade=%{x}<br>Impacto=%{y}<br>Valor=%{z}",
        colorscale=colorscale,
        zmin=1,
        zmax=25,
        showscale=True
    ))
    fig.update_layout(
        title="Matriz de Riscos 5x5",
        xaxis_title="Probabilidade",
        yaxis_title="Impacto",
        yaxis=dict(autorange="reversed")
    )
    # Anota o risco atual
    fig.add_annotation(
        x=prob_labels[prob-1],
        y=impact_labels[imp_final-1],
        text=str(id_r),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-20
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Riscos no gráfico")
    st.write(f"- **{id_r}**: {escolha}")

    st.markdown("**Legenda de Níveis**")
    st.write(
        "- 1–5: Pequeno  \\  \n"
        "- 6–10: Moderado  \\  \n"
        "- 11–15: Alto  \\  \n"
        "- 16–25: Crítico"
    )


def main():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio(
        "Ir para:",
        ["Avaliação de Riscos", "Estratégia de Riscos", "Controles de Risco"]
    )
    if page == "Avaliação de Riscos":
        main_avaliacao()
    elif page == "Estratégia de Riscos":
        riscos_estrategia_associacao()
    else:
        riscos_controle_avaliacao()


if __name__ == '__main__':
    main()
