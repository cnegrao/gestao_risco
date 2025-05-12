import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from database_utils import run_select


def main():

    # ------------------ Header ------------------
    st.title("🛡️ Dashboard de Gestão de Riscos")
    st.markdown(
        "## Visão geral dos principais indicadores de risco e tratamento")
    st.markdown("---")

    # ------------------ Cards de Métricas ------------------
    # Queries
    q_processos = """
    SELECT COUNT(DISTINCT p.id_processo) AS total
    FROM public.tb_processos p
    JOIN public.tb_subprocessos sp ON sp.id_processo = p.id_processo
    JOIN public.tb_riscos r ON r.id_subprocesso = sp.id_subprocesso;
    """
    q_subprocessos = """
    SELECT COUNT(DISTINCT sp.id_subprocesso) AS total
    FROM public.tb_riscos r
    JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso;
    """
    q_riscos = "SELECT COUNT(*) AS total FROM public.tb_riscos;"
    q_acoes = "SELECT COUNT(*) AS total FROM public.tb_plano_tratamento;"
    q_acoes_prazo = """
    SELECT COUNT(*) AS total
    FROM public.tb_plano_tratamento pt
    WHERE pt.data_real_termino <= pt.data_prazo_limite;
    """
    q_acoes_atrasadas = """
    SELECT COUNT(*) AS total
    FROM public.tb_plano_tratamento pt
    WHERE (pt.data_real_termino > pt.data_prazo_limite)
    OR (pt.data_real_termino IS NULL AND pt.data_prazo_limite < CURRENT_DATE);
    """
    q_acoes_concluidas = """
    SELECT COUNT(*) AS total
    FROM public.tb_plano_tratamento pt
    WHERE pt.data_real_termino IS NOT NULL;
    """
    q_acoes_canceladas = """
    SELECT COUNT(*) AS total
    FROM public.tb_plano_tratamento pt
    WHERE pt.id_status = 4;
    """

    # Executa selects
    m_processos = run_select(q_processos).iloc[0, 0]
    m_subprocessos = run_select(q_subprocessos).iloc[0, 0]
    m_riscos = run_select(q_riscos).iloc[0, 0]
    m_acoes = run_select(q_acoes).iloc[0, 0]
    m_prazo = run_select(q_acoes_prazo).iloc[0, 0]
    m_atrasadas = run_select(q_acoes_atrasadas).iloc[0, 0]
    m_concluidas = run_select(q_acoes_concluidas).iloc[0, 0]
    m_canceladas = run_select(q_acoes_canceladas).iloc[0, 0]

    # Layout dos cards em duas linhas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Processos", m_processos)
    with col2:
        st.metric("Subprocessos", m_subprocessos)
    with col3:
        st.metric("Riscos", m_riscos)
    with col4:
        st.metric("Ações", m_acoes)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Ações no Prazo", m_prazo)
    with col6:
        st.metric("Ações Atrasadas", m_atrasadas)
    with col7:
        st.metric("Ações Concluídas", m_concluidas)
    with col8:
        st.metric("Ações Canceladas", m_canceladas)

    st.markdown("---")

    # ------------------ Gráficos de Barras ------------------
    st.subheader("Distribuição de Riscos")

    # Barras por Área
    bar_area_q = """
    SELECT ar.nome_area, COUNT(*) AS total
    FROM public.tb_riscos r
    JOIN public.tb_plano_tratamento pl ON r.id_risco = pl.id_risco
    JOIN public.tb_area_responsavel ar on pl.id_area_responsavel = ar.id_area
    GROUP BY ar.nome_area
    """
    bar_area_df = run_select(bar_area_q)
    fig_bar_area = go.Figure(
        go.Bar(x=bar_area_df['nome_area'], y=bar_area_df['total'])
    )
    fig_bar_area.update_layout(
        title_text='Riscos por Área Responsável',
        xaxis_title='Área',
        yaxis_title='Quantidade'
    )

    # Barras por Categoria
    bar_cat_q = """
    SELECT cat.nome_categoria, COUNT(*) AS total
    FROM public.tb_riscos r
    join public.tb_categorias cat on r.id_categoria = cat.id_categoria
    GROUP BY cat.nome_categoria
    ORDER BY total DESC;
    """
    bar_cat_df = run_select(bar_cat_q)
    fig_bar_cat = go.Figure(
        go.Bar(x=bar_cat_df['nome_categoria'], y=bar_cat_df['total'])
    )
    fig_bar_cat.update_layout(
        title_text='Riscos por Categoria',
        xaxis_title='nome_categoria',
        yaxis_title='Quantidade'
    )

    colb1, colb2 = st.columns(2)
    with colb1:
        st.plotly_chart(fig_bar_area, use_container_width=True)
    with colb2:
        st.plotly_chart(fig_bar_cat, use_container_width=True)

    st.markdown("---")

    # ------------------ Gráficos de Rosca ------------------
    st.subheader("Distribuições (%)")

    colr1, colr2 = st.columns(2)
    with colr1:
        fig_donut_area = go.Figure(
            go.Pie(labels=bar_area_df['nome_area'],
                   values=bar_area_df['total'], hole=0.5)
        )
        fig_donut_area.update_layout(title_text='Riscos por Área (%)')
        st.plotly_chart(fig_donut_area, use_container_width=True)

    with colr2:
        fig_donut_cat = go.Figure(
            go.Pie(labels=bar_cat_df['nome_categoria'],
                   values=bar_cat_df['total'], hole=0.5)
        )
        fig_donut_cat.update_layout(title_text='Riscos por Categoria (%)')
        st.plotly_chart(fig_donut_cat, use_container_width=True)

    st.markdown("---")

    # ------------------ Tabela Descritiva ------------------
    st.subheader("Detalhamento de Riscos")
    q_table = """
    SELECT 
    p.nome_processo,
    sp.nome_subprocesso,
    r.nome_risco,
    r.criticidade
    FROM public.tb_riscos r
    JOIN public.tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso
    JOIN public.tb_processos p ON sp.id_processo = p.id_processo
    ORDER BY p.nome_processo, sp.nome_subprocesso;
    """
    table_df = run_select(q_table)
    st.dataframe(table_df, use_container_width=True)

    st.markdown("---")

    # ------------------ Heatmap Probabilidade x Impacto ------------------
    st.subheader("Matriz de Risco: Probabilidade × Impacto")
    q_heat = """
    SELECT 
    r.probabilidade,
    GREATEST(r.impacto_financeiro, r.impacto_imagem, r.impacto_conformidade) AS impacto_final
    FROM public.tb_riscos r
    WHERE r.probabilidade IS NOT NULL;
    """
    heat_df = run_select(q_heat)

    # Monta a matriz 5×5
    z = [[0]*5 for _ in range(5)]
    for _, row in heat_df.iterrows():
        p = int(row['probabilidade']) - 1
        i = int(row['impacto_final']) - 1
        if 0 <= p < 5 and 0 <= i < 5:
            z[4-i][p] += 1

    fig_heat = go.Figure(
        go.Heatmap(
            z=z,
            x=[1, 2, 3, 4, 5],
            y=[5, 4, 3, 2, 1],
            colorscale='Reds',
            text=z,
            texttemplate='%{text}',
            hovertemplate='Prob=%{x} Impacto=%{y}<br>Qtd=%{z}'
        )
    )
    fig_heat.update_layout(
        title_text='Matriz de Riscos',
        xaxis_title='Probabilidade',
        yaxis_title='Impacto'
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# só para debug em linha de comando
if __name__ == '__main__':
    main()
