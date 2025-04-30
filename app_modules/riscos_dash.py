import streamlit as st
import pandas as pd
import plotly.express as px
from database_utils import run_select

# OBS: st.set_page_config deve estar definido apenas em app.py


def load_data_from_db():
    query = '''
    SELECT
      r.id_risco,
      r.nome_risco AS risco,
      CAST(r.probabilidade AS numeric) AS probabilidade,
      CAST(r.impacto_financeiro AS numeric) AS impacto_financeiro,
      CAST(r.impacto_imagem AS numeric) AS impacto_imagem,
      CAST(r.impacto_conformidade AS numeric) AS impacto_conformidade,
      CAST(r.impacto_estimado AS numeric) AS impacto_final,
      CAST(r.nivel_risco AS numeric) AS nivel_risco,
      r.criticidade AS classificacao,
      c.nome_categoria AS categoria
    FROM public.tb_riscos r
    LEFT JOIN public.tb_categorias c ON r.id_categoria = c.id_categoria
    WHERE r.probabilidade IS NOT NULL
      AND r.impacto_estimado IS NOT NULL;
    '''
    df = run_select(query)
    # Converter colunas para numérico
    for col in ['probabilidade', 'impacto_financeiro', 'impacto_imagem', 'impacto_conformidade', 'impacto_final', 'nivel_risco']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Recalcula nivel_risco (probabilidade x impacto_final)
    df['nivel_risco'] = df['probabilidade'] * df['impacto_final']
    return df

# Mapeia valores numéricos para rótulos


def label_classificacao(n):
    if pd.isna(n):
        return 'Não definido'
    if n <= 5:
        return 'Pequeno'
    elif n <= 10:
        return 'Moderado'
    elif n <= 15:
        return 'Alto'
    else:
        return 'Crítico'

# Classifica fatores de impacto/propabilidade em três categorias


def label_tres_niveis(v):
    if pd.isna(v):
        return 'Não definido'
    if v <= 2:
        return 'Baixo'
    elif v <= 4:
        return 'Médio'
    else:
        return 'Alto'


def main():
    st.title("Dashboard Analítico de Riscos")
    df = load_data_from_db()

    # KPIs descritivos
    total = len(df)
    avg_nivel = df['nivel_risco'].mean(skipna=True)
    avg_prob = df['probabilidade'].mean(skipna=True)
    avg_fin = df['impacto_financeiro'].mean(skipna=True)
    avg_img = df['impacto_imagem'].mean(skipna=True)
    avg_conf = df['impacto_conformidade'].mean(skipna=True)

    nivel_label = label_classificacao(avg_nivel)
    prob_label = label_tres_niveis(avg_prob)
    fin_label = label_tres_niveis(avg_fin)
    img_label = label_tres_niveis(avg_img)
    conf_label = label_tres_niveis(avg_conf)

    st.subheader("KPIs Principais (Descritivos)")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total de Riscos", total)
    c2.metric("Nível Médio de Risco", nivel_label)
    c3.metric("Probabilidade Média", prob_label)
    c4.metric("Impacto Financeiro Médio", fin_label)
    c5.metric("Impacto de Imagem Médio", img_label)
    c6.metric("Impacto de Conformidade Médio", conf_label)

    st.markdown("---")
    # Radar (descritivo não aplicável para radar, omitido)

    st.subheader("Distribuição de Classificação")
    dist_df = df['classificacao'].value_counts().reset_index()
    dist_df.columns = ['classificacao', 'qtd']
    fig1 = px.bar(dist_df, x='classificacao', y='qtd',
                  title='Contagem por Nível de Criticidade',
                  category_orders={'classificacao': ['Pequeno', 'Moderado', 'Alto', 'Crítico']})
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
    # Scatter: Probabilidade vs Impacto Final, colorido por criticidade
    st.subheader("Dispersão: Probabilidade vs Impacto Final")
    fig2 = px.scatter(
        df, x='probabilidade', y='impacto_final', color='classificacao',
        title='Probabilidade vs Impacto',
        labels={'probabilidade': 'Probabilidade',
                'impacto_final': 'Impacto Final'}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    # Nível Médio por Categoria (descritivo)
    st.subheader("Categoria de Risco Mais Frequente")
    cat = df['categoria'].value_counts(
        normalize=True).mul(100).round(1).reset_index()
    cat.columns = ['categoria', 'percentual']
    fig3 = px.pie(cat, names='categoria', values='percentual',
                  title='Distribuição por Categoria')
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    # Top 5 Maiores Riscos (Criticidade)
    st.subheader("Top 5 Maiores Riscos")
    top5 = df.nlargest(5, 'nivel_risco')[['id_risco', 'risco', 'nivel_risco']]
    top5['criticidade'] = top5['nivel_risco'].apply(label_classificacao)
    st.table(top5.set_index('id_risco'))

    st.markdown("---")
    # Detalhamento resumido
    st.subheader("Detalhamento de Riscos")
    cols = ['id_risco', 'risco', 'categoria', 'classificacao']
    st.dataframe(df[cols], use_container_width=True)


if __name__ == '__main__':
    main()
