import logging

import plotly.graph_objs as go
import streamlit as st

from database_utils import run_select

# Configura logger simples
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# --- 1) Isolar todas as queries ---
QUERIES = {
    # Métricas
    "Processos": """
        SELECT COUNT(DISTINCT p.id_processo) AS total
        FROM public.tb_processos p
        JOIN public.tb_subprocessos sp ON sp.id_processo = p.id_processo
        JOIN public.tb_riscos r ON r.id_subprocesso = sp.id_subprocesso;
    """,
    "Subprocessos": """
        SELECT COUNT(DISTINCT sp.id_subprocesso) AS total
        FROM public.tb_riscos r
        JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso;
    """,
    "Riscos": "SELECT COUNT(*) AS total FROM public.tb_riscos;",
    "Ações": "SELECT COUNT(*) AS total FROM public.tb_plano_tratamento;",
    "No Prazo": """
        SELECT COUNT(*) AS total
        FROM public.tb_plano_tratamento pt
        WHERE pt.data_real_termino <= pt.data_prazo_limite;
    """,
    "Atrasadas": """
        SELECT COUNT(*) AS total
        FROM public.tb_plano_tratamento pt
        WHERE (pt.data_real_termino > pt.data_prazo_limite)
           OR (pt.data_real_termino IS NULL AND pt.data_prazo_limite < CURRENT_DATE);
    """,
    "Concluídas": """
        SELECT COUNT(*) AS total
        FROM public.tb_plano_tratamento pt
        WHERE pt.data_real_termino IS NOT NULL;
    """,
    "Canceladas": """
        SELECT COUNT(*) AS total
        FROM public.tb_plano_tratamento pt
        WHERE pt.id_status = 4;
    """,

    # Gráficos de barras
    "Por Processo": """
        SELECT p.nome_processo, COUNT(*) AS total
        FROM public.tb_riscos r
        JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
        JOIN public.tb_processos p ON sp.id_processo = p.id_processo
        GROUP BY p.nome_processo
        ORDER BY total DESC;
    """,
    "Por Subprocesso": """
        SELECT sp.nome_subprocesso, COUNT(*) AS total
        FROM public.tb_riscos r
        JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
        GROUP BY sp.nome_subprocesso
        ORDER BY total DESC;
    """,
    "Por Categoria": """
        SELECT cat.nome_categoria, COUNT(*) AS total
        FROM public.tb_riscos r
        JOIN public.tb_categorias cat ON r.id_categoria = cat.id_categoria
        GROUP BY cat.nome_categoria
        ORDER BY total DESC;
    """,
    "Por Área": """
        SELECT ar.nome_area, COUNT(*) AS total
        FROM public.tb_plano_tratamento pl
        JOIN public.tb_area_responsavel ar ON pl.id_area_responsavel = ar.id_area
        GROUP BY ar.nome_area
        ORDER BY total DESC;
    """,

    # Tabela de detalhamento
    "Detalhamento": """
        SELECT p.nome_processo,
               sp.nome_subprocesso,
               r.nome_risco,
               r.criticidade
        FROM public.tb_riscos r
        JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
        JOIN public.tb_processos p ON sp.id_processo = p.id_processo
        ORDER BY p.nome_processo, sp.nome_subprocesso;
    """,

    # Heatmap
    "Heatmap": """
        WITH raw AS (
          SELECT
            id_risco_selecionado,
            probabilidade,
            impacto_final,
            criticidade,
            data_avaliacao,
            ROW_NUMBER() OVER (
              PARTITION BY id_risco_selecionado
              ORDER BY
                CASE criticidade
                  WHEN 'Risco Alto'  THEN 3
                  WHEN 'Risco Médio' THEN 2
                  ELSE 1
                END DESC,
                data_avaliacao DESC
            ) AS rn
          FROM public.tb_risco_avaliacoes
          WHERE criticidade IN ('Risco Baixo','Risco Médio','Risco Alto')
        ), sel AS (
          SELECT id_risco_selecionado, probabilidade, impacto_final, criticidade
          FROM raw
          WHERE rn = 1
        )
        SELECT
          probabilidade,
          impacto_final,
          COUNT(*)         AS qtd_riscos,
          MAX(criticidade) AS criticidade
        FROM sel
        GROUP BY probabilidade, impacto_final
        ORDER BY probabilidade, impacto_final;
    """,
}

# --- 2) Funções com cache ---


@st.cache_data(ttl=300)
def fetch_metric(sql: str) -> int:
    df = run_select(sql)
    return int(df.iloc[0, 0])


@st.cache_data(ttl=300)
def fetch_df(sql: str):
    return run_select(sql)


def main():
    st.title("🛡️ Dashboard de Gestão de Riscos")
    st.markdown(
        "## Visão geral dos principais indicadores de risco e tratamento")
    st.markdown("---")

    # --- Top Metrics ---
    labels = [
        "Processos", "Subprocessos", "Riscos",
        "Ações", "No Prazo", "Atrasadas",
        "Concluídas", "Canceladas"
    ]
    cols = st.columns(len(labels))
    for label, col in zip(labels, cols):
        try:
            val = fetch_metric(QUERIES[label])
            col.metric(label, f"{val:,}")
        except Exception as e:
            logger.error("Erro ao buscar métrica %s: %s", label, e)
            col.metric(label, "—")

    st.markdown("---")

    # --- Bar Charts ---
    st.subheader("📊 Riscos por Processo e Subprocesso")
    p1, p2 = st.columns(2)
    df1 = fetch_df(QUERIES["Por Processo"])
    fig1 = go.Figure(go.Bar(x=df1["nome_processo"], y=df1["total"]))
    fig1.update_layout(title="Por Processo", margin=dict(t=30))
    p1.plotly_chart(fig1, use_container_width=True)

    df2 = fetch_df(QUERIES["Por Subprocesso"])
    fig2 = go.Figure(go.Bar(x=df2["nome_subprocesso"], y=df2["total"]))
    fig2.update_layout(title="Por Subprocesso", margin=dict(t=30))
    p2.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- Categoria & Área ---
    st.subheader("🌐 Riscos por Categoria e Área")
    c1, c2 = st.columns(2)
    df_cat = fetch_df(QUERIES["Por Categoria"])
    fig_cat = go.Figure(go.Bar(x=df_cat["nome_categoria"], y=df_cat["total"]))
    fig_cat.update_layout(title="Por Categoria", margin=dict(t=30))
    c1.plotly_chart(fig_cat, use_container_width=True)

    df_area = fetch_df(QUERIES["Por Área"])
    fig_area = go.Figure(go.Bar(x=df_area["nome_area"], y=df_area["total"]))
    fig_area.update_layout(title="Por Área Responsável", margin=dict(t=30))
    c2.plotly_chart(fig_area, use_container_width=True)

    st.markdown("---")

    # --- Donut Charts ---
    st.subheader("🍩 Distribuições (%)")
    d1, d2 = st.columns(2)
    fig_d1 = go.Figure(go.Pie(
        labels=df_cat["nome_categoria"], values=df_cat["total"], hole=0.5))
    fig_d1.update_layout(title="Por Categoria (%)", margin=dict(t=30))
    d1.plotly_chart(fig_d1, use_container_width=True)

    fig_d2 = go.Figure(go.Pie(
        labels=df_area["nome_area"], values=df_area["total"], hole=0.5))
    fig_d2.update_layout(title="Por Área (%)", margin=dict(t=30))
    d2.plotly_chart(fig_d2, use_container_width=True)

    st.markdown("---")

    # --- Table & Heatmap ---
    t1, t2 = st.columns([2, 1])
    with t1:
        st.subheader("📝 Detalhamento de Riscos")
        df_tab = fetch_df(QUERIES["Detalhamento"])
        st.dataframe(df_tab, use_container_width=True, height=400)

    with t2:
        st.subheader("🔥 Matriz de Avaliações (Prob × Impacto)")
        agg = fetch_df(QUERIES["Heatmap"])

        # Prepara as matrizes com z_count e z_val como antes...
        z_count = [[0]*5 for _ in range(5)]
        z_val = [[0]*5 for _ in range(5)]
        color_map = {"Risco Baixo": "green",
                     "Risco Médio": "orange", "Risco Alto": "red"}
        crit_to_val = {"green": 0, "orange": 1, "red": 2}

        for _, row in agg.iterrows():
            p = int(row["probabilidade"]) - 1
            i = int(row["impacto_final"]) - 1
            r = 4 - i
            z_count[r][p] = int(row["qtd_riscos"])
            col = color_map.get(row["criticidade"], "green")
            z_val[r][p] = crit_to_val[col]

        fig = go.Figure(go.Heatmap(
            z=z_val,
            x=[1, 2, 3, 4, 5],
            y=[5, 4, 3, 2, 1],
            zmin=0, zmax=2,
            colorscale=[
                [0.0, "green"], [0.33, "green"],
                [0.34, "orange"], [0.66, "orange"],
                [0.67, "red"], [1.0, "red"],
            ],
            colorbar=dict(
                title="Criticidade",
                tickmode="array",
                tickvals=[0, 1, 2],
                ticktext=["Baixo", "Médio", "Alto"],
            ),
            text=z_count,
            texttemplate="%{text}",
            hovertemplate=(
                "Probabilidade: %{x}<br>"
                "Impacto: %{y}<br>"
                "Riscos: %{text}<extra></extra>"
            )
        ))
        fig.update_layout(
            title="Matriz de Avaliações (Prob × Impacto)",
            xaxis_title="Probabilidade",
            yaxis_title="Impacto",
            margin=dict(t=30)
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
