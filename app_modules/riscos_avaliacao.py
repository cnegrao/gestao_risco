import os
import sys

import plotly.graph_objs as go
import streamlit as st

from app_modules.riscos_controle_avaliacao import riscos_controle_avaliacao
from app_modules.riscos_estrategia_associacao import \
    riscos_estrategia_associacao
from database_utils import run_query, run_select

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
        **Objetivo:** Avaliar os riscos cadastrados preenchendo probabilidade (1-5), impactos em três dimensões, cálculo de impacto final (máximo), nível do risco e classificação.
        *Use os controles abaixo para definir e salvar sua avaliação.*
        """
    )

    # Seleção de risco
    df_riscos = run_select(
        "SELECT id_risco, nome_risco, id_empresa FROM tb_riscos ORDER BY nome_risco DESC"
    )
    if df_riscos.empty:
        st.warning("⚠️ Nenhum risco cadastrado disponível.")
        return

    escolha = st.selectbox("Selecione um risco:",
                           df_riscos["nome_risco"], key="aval_risco")
    sel_row = df_riscos[df_riscos["nome_risco"] == escolha].iloc[0]
    id_r = int(sel_row["id_risco"])
    id_empresa = int(sel_row["id_empresa"])
    st.markdown("---")

    # Exibe contexto: Estratégia & Controles
    colE, colC = st.columns(2)
    with colE:
        st.subheader("Estratégia Associada")
        estr_df = run_select(
            """
            SELECT o.descricao AS Objetivo, m.descricao AS Meta
              FROM tb_risco_meta rm
              JOIN tb_meta_estrategica m ON rm.id_meta = m.id_meta
              JOIN tb_objetivo_estrategico o ON m.id_objetivo = o.id_objetivo
             WHERE rm.id_empresa=%s AND rm.id_risco=%s;
            """,
            (id_empresa, id_r),
        )
        if estr_df.empty:
            st.info("Nenhuma estratégia associada.")
        else:
            st.table(estr_df)
    with colC:
        st.subheader("Controles Associados")
        ctrl_df = run_select(
            """
            SELECT rc.descricao_controle AS Descrição,
                   sc.descricao AS Situação,
                   ec.descricao AS Execução
              FROM tb_risco_controle rc
              JOIN tb_situacao_controle sc ON rc.id_situacao_controle=sc.id_situacao_controle
              JOIN tb_execucao_controle ec ON rc.id_execucao_controle=ec.id_execucao_controle
             WHERE rc.id_risco=%s;
            """,
            (id_r,),
        )
        if ctrl_df.empty:
            st.info("Nenhum controle associado.")
        else:
            st.table(ctrl_df)

    st.markdown("---")
    # Sliders de avaliação
    st.subheader("Defina sua Avaliação")
    prob = st.slider("Probabilidade", 1, 5, 3, key="aval_prob")
    col1, col2, col3 = st.columns(3)
    with col1:
        fin = st.slider("Impacto Financeiro", 1, 5, 3, key="aval_fin")
    with col2:
        img = st.slider("Impacto na Imagem", 1, 5, 3, key="aval_img")
    with col3:
        conf = st.slider("Impacto na Conformidade", 1, 5, 3, key="aval_conf")

    imp_final = max(fin, img, conf)
    nivel = prob * imp_final
    cls = (
        "Pequeno"
        if nivel <= 5
        else "Moderado"
        if nivel <= 10
        else "Alto"
        if nivel <= 15
        else "Crítico"
    )

    # Mapas de cor e ícones para classificação
    icon_map = {"Pequeno": "🟢", "Moderado": "🟡", "Alto": "🟠", "Crítico": "🔴"}
    color_map = {
        "Pequeno": "#00FF00",
        "Moderado": "#FFFF00",
        "Alto": "#FFA500",
        "Crítico": "#FF0000",
    }

    # Botão de salvar
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
                (prob, fin, img, conf, imp_final, nivel, cls, id_r),
            )
            st.success("✅ Avaliação salva com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao salvar avaliação: {e}")

    # Container estilizado para resultados
    st.markdown(
        f"""
    <div style="background-color:#1f2b3a;padding:20px;border-radius:8px;border:1px solid #334455;margin-bottom:20px;">
      <h3 style="margin:0 0 12px;color:#fff;">Resultado da Avaliação</h3>
      <div style="display:flex;justify-content:space-evenly;">
        <div style="text-align:center;">
          <div style="font-size:14px;color:#aaa;">Probabilidade</div>
          <div style="font-size:32px;font-weight:bold;color:{color_map.get(cls)};">{prob}</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:14px;color:#aaa;">Impacto Final</div>
          <div style="font-size:32px;font-weight:bold;color:{color_map.get(cls)};">{imp_final}</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:14px;color:#aaa;">Nível de Risco</div>
          <div style="font-size:32px;font-weight:bold;color:{color_map.get(cls)};">{nivel}</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:14px;color:#aaa;">Classificação</div>
          <div style="font-size:32px;font-weight:bold;color:{color_map.get(cls)};">{icon_map.get(cls)} {cls}</div>
        </div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    # Monta matriz de contagem filtrada por processo
    proc_df = run_select(
        "SELECT sp.id_processo FROM tb_riscos r JOIN tb_subprocessos sp ON r.id_subprocesso=sp.id_subprocesso WHERE r.id_risco=%s;",
        (id_r,),
    )
    if proc_df.empty:
        st.error("⚠️ Processo não encontrado.")
        return
    pid = int(proc_df.iloc[0, 0])
    all_df = run_select(
        "SELECT r.probabilidade, GREATEST(r.impacto_financeiro, r.impacto_imagem, r.impacto_conformidade) AS impacto_final FROM tb_riscos r JOIN tb_subprocessos sp ON r.id_subprocesso=sp.id_subprocesso WHERE sp.id_processo=%s AND r.probabilidade IS NOT NULL;",
        (pid,),
    )
    z = [[0] * 5 for _ in range(5)]
    for _, r in all_df.iterrows():
        try:
            p = int(r.probabilidade) - 1
            i = int(r.impacto_final) - 1
        except:
            continue
        if 0 <= p < 5 and 0 <= i < 5:
            z[4 - i][p] += 1
    prob_labels = [str(x) for x in range(1, 6)]
    y_labels = [str(x) for x in range(5, 0, -1)]
    fig = go.Figure(
        go.Heatmap(
            x=prob_labels,
            y=y_labels,
            z=z,
            text=z,
            texttemplate="%{text}",
            hovertemplate="Prob=%{x} Impacto=%{y}<br>Riscos=%{z}",
            colorscale="Reds",
            zmin=0,
            zmax=max(max(row) for row in z),
            showscale=True,
        )
    )
    fig.update_layout(
        title="Matriz de Riscos por Quadrante (Contagem)",
        xaxis_title="Probabilidade",
        yaxis_title="Impacto",
        yaxis=dict(autorange=False),
    )
    st.subheader("Distribuição de Riscos no Processo")
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.sidebar.title("Navegação")
    escolha = st.sidebar.radio(
        "Ir para:",
        ["Avaliação de Riscos", "Estratégia de Riscos", "Controles de Risco"],
    )
    if escolha == "Avaliação de Riscos":
        main_avaliacao()
    elif escolha == "Estratégia de Riscos":
        riscos_estrategia_associacao()
    else:
        riscos_controle_avaliacao()


if __name__ == "__main__":
    main()
