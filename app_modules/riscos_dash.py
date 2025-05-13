import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from database_utils import run_select


def main():
    # --- Top Metrics ---
    st.markdown("### 📊 Indicadores Gerais", unsafe_allow_html=True)

    metrics = [
        ("Processos", """
            SELECT COUNT(DISTINCT p.id_processo) AS total
            FROM public.tb_processos p
            JOIN public.tb_subprocessos sp ON sp.id_processo = p.id_processo
            JOIN public.tb_riscos r ON r.id_subprocesso = sp.id_subprocesso;
        """),
        ("Subprocessos", """
            SELECT COUNT(DISTINCT sp.id_subprocesso) AS total
            FROM public.tb_riscos r
            JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso;
        """),
        ("Riscos", "SELECT COUNT(*) AS total FROM public.tb_riscos;"),
        ("Ações", "SELECT COUNT(*) AS total FROM public.tb_plano_tratamento;"),
        ("No Prazo", """
            SELECT COUNT(*) AS total
            FROM public.tb_plano_tratamento pt
            WHERE pt.data_real_termino <= pt.data_prazo_limite;
        """),
        ("Atrasadas", """
            SELECT COUNT(*) AS total
            FROM public.tb_plano_tratamento pt
            WHERE (pt.data_real_termino > pt.data_prazo_limite)
               OR (pt.data_real_termino IS NULL AND pt.data_prazo_limite < CURRENT_DATE);
        """),
        ("Concluídas", """
            SELECT COUNT(*) AS total
            FROM public.tb_plano_tratamento pt
            WHERE pt.data_real_termino IS NOT NULL;
        """),
        ("Canceladas", """
            SELECT COUNT(*) AS total
            FROM public.tb_plano_tratamento pt
            WHERE pt.id_status = 4;
        """),
    ]

    cols = st.columns(len(metrics))
    for (label, sql), col in zip(metrics, cols):
        try:
            val = run_select(sql).iloc[0, 0]
            col.metric(label, f"{val:,}")
        except:
            col.metric(label, "—")

    st.markdown("---")

    # --- Barras de Quantidade ---
    st.subheader("Distribuição de Riscos")
    p1, p2 = st.columns(2)
    df1 = run_select("""
        SELECT p.nome_processo, COUNT(*) AS total
        FROM public.tb_riscos r
        JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
        JOIN public.tb_processos p ON sp.id_processo = p.id_processo
        GROUP BY p.nome_processo
        ORDER BY total DESC;
    """)
    fig1 = go.Figure(go.Bar(x=df1['nome_processo'], y=df1['total']))
    fig1.update_layout(title_text="Por Processo", margin=dict(t=40))
    p1.plotly_chart(fig1, use_container_width=True)

    df2 = run_select("""
        SELECT sp.nome_subprocesso, COUNT(*) AS total
        FROM public.tb_riscos r
        JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
        GROUP BY sp.nome_subprocesso
        ORDER BY total DESC;
    """)
    fig2 = go.Figure(go.Bar(x=df2['nome_subprocesso'], y=df2['total']))
    fig2.update_layout(title_text="Por Subprocesso", margin=dict(t=40))
    p2.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- Barras Categoria & Área ---
    st.subheader("🌐 Riscos por Categoria e Área")
    c1, c2 = st.columns(2)
    df_cat = run_select("""
        SELECT cat.nome_categoria, COUNT(*) AS total
        FROM public.tb_riscos r
        JOIN public.tb_categorias cat ON r.id_categoria = cat.id_categoria
        GROUP BY cat.nome_categoria
        ORDER BY total DESC;
    """)
    fig_cat = go.Figure(go.Bar(x=df_cat['nome_categoria'], y=df_cat['total']))
    fig_cat.update_layout(title="Categoria", margin=dict(t=40))
    c1.plotly_chart(fig_cat, use_container_width=True)

    df_area = run_select("""
        SELECT ar.nome_area, COUNT(*) AS total
        FROM public.tb_plano_tratamento pl
        JOIN public.tb_area_responsavel ar ON pl.id_area_responsavel = ar.id_area
        GROUP BY ar.nome_area
        ORDER BY total DESC;
    """)
    fig_area = go.Figure(go.Bar(x=df_area['nome_area'], y=df_area['total']))
    fig_area.update_layout(title="Área Responsável", margin=dict(t=40))
    c2.plotly_chart(fig_area, use_container_width=True)

    st.markdown("---")

    # --- Donuts de % ---
    st.subheader("📊 Distribuições (%)")
    d1, d2 = st.columns(2)
    with d1:
        fig_d1 = go.Figure(go.Pie(
            labels=df_cat['nome_categoria'],
            values=df_cat['total'],
            hole=0.5
        ))
        fig_d1.update_layout(title="Por Categoria (%)", margin=dict(t=40))
        st.plotly_chart(fig_d1, use_container_width=True)
    with d2:
        fig_d2 = go.Figure(go.Pie(
            labels=df_area['nome_area'],
            values=df_area['total'],
            hole=0.5
        ))
        fig_d2.update_layout(title="Por Área (%)", margin=dict(t=40))
        st.plotly_chart(fig_d2, use_container_width=True)

    st.markdown("---")

    # --- Tabela & Heatmap ---
    t1, t2 = st.columns([2, 1])
    with t1:
        st.subheader("📋 Detalhamento de Riscos")
        df_tab = run_select("""
            SELECT p.nome_processo,
                   sp.nome_subprocesso,
                   r.nome_risco,
                   r.criticidade
            FROM public.tb_riscos r
            JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
            JOIN public.tb_processos p ON sp.id_processo = p.id_processo
            ORDER BY p.nome_processo, sp.nome_subprocesso;
        """)
        st.dataframe(df_tab, use_container_width=True, height=400)

    with t2:
        # ------------------ Heatmap de Avaliações ------------------
        st.subheader("Matriz de Risco: Probabilidade × Impacto (Avaliações)")

        # 1) Busca diretamente as avaliações
        q_heat = """
            SELECT 
            probabilidade,
            impacto_final,
            criticidade
            FROM public.tb_risco_avaliacoes
            WHERE probabilidade IS NOT NULL
            AND criticidade IN ('Pequeno','Moderado','Alto');
            """
        heat_df = run_select(q_heat)

        # 2) Mapeia criticidade para valor [0,1,2]
        crit_map = {'Pequeno': 0, 'Moderado': 1, 'Alto': 2}
        heat_df['crit_val'] = heat_df['criticidade'].map(crit_map)

        # 3) Para cada par (p,i) contamos:
        #    - o número de avaliações (para o texto da célula)
        #    - a pior criticidade (para a cor)
        count_df = (
            heat_df
            .groupby(['probabilidade', 'impacto_final'])
            .agg(
                qtd=('criticidade', 'size'),
                crit_max=('crit_val', 'max')
            )
            .reset_index()
        )

        # 4) Monta a matriz 5×5
        z_count = [[0]*5 for _ in range(5)]
        z_crit = [[0]*5 for _ in range(5)]
        for _, row in count_df.iterrows():
            p = int(row['probabilidade'])-1
            i = int(row['impacto_final'])-1
            # invertendo y para impacto=1 na base e 5 no topo
            linha = 4 - i
            z_count[linha][p] = int(row['qtd'])
            z_crit[linha][p] = int(row['crit_max'])

        # 5) Definição do colorscale discreto
        colorscale = [
            [0.0, 'green'],  [0.33, 'green'],
            [0.34, 'orange'], [0.66, 'orange'],
            [0.67, 'red'],   [1.0, 'red']
        ]

        fig_heat = go.Figure(
            go.Heatmap(
                z=z_crit,
                x=[1, 2, 3, 4, 5],
                y=[5, 4, 3, 2, 1],
                zmin=0, zmax=2,
                colorscale=colorscale,
                colorbar=dict(
                    title="Criticidade",
                    tickmode="array",
                    tickvals=[0, 1, 2],
                    ticktext=["Pequeno", "Moderado", "Alto"]
                ),
                text=z_count,
                texttemplate="%{text}",
                hovertemplate=(
                    "Probabilidade %{x}<br>"
                    "Impacto %{y}<br>"
                    "Avaliações %{text}<br>"
                    "Criticidade %{colorbar.title}<extra></extra>"
                )
            )
        )
        fig_heat.update_layout(
            title="Matriz de Avaliações (Prob × Impacto)",
            xaxis_title="Probabilidade",
            yaxis_title="Impacto"
        )
        st.plotly_chart(fig_heat, use_container_width=True)


if __name__ == "__main__":
    main()
