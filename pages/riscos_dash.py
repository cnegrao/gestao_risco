import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurações iniciais
st.set_page_config(page_title="Dashboard Analítico de Riscos", layout="wide")


@st.cache_data
def load_data(path):
    # Carrega a planilha com cabeçalho na linha 6
    df = pd.read_excel(path, header=5)
    # Renomeia colunas para facilitar uso
    df = df.rename(columns={
        'Controles existentes: existência e relevância': 'controle_m',
        'Controles existentes: funcionamento': 'controle_n',
        'Probabilidade ** pegar 5 no  zap': 'probabilidade',
        'Nível do impacto': 'nivel_impacto',
        'Nível do Risco': 'nivel_risco',
        'Classificação do Risco': 'classificacao'
    })
    # Converte tipos
    df['probabilidade'] = df['probabilidade'].astype(int)
    df['nivel_impacto'] = pd.to_numeric(df['nivel_impacto'], errors='coerce')
    df['nivel_risco'] = pd.to_numeric(df['nivel_risco'], errors='coerce')
    df['classificacao'] = df['classificacao'].astype(str)
    return df


# Carrega os dados
data_path = '/mnt/data/Riscos  senac v. 12-02-2025 (2).xlsx'
df = load_data(data_path)

# Cabeçalhos de KPI
total_riscos = df.shape[0]
media_nivel = round(df['nivel_risco'].mean(), 2)
riscos_criticos = df[df['classificacao'] == 'Crítico'].shape[0]

# Mostra KPIs
k1, k2, k3 = st.columns(3)
k1.metric("Total de Riscos", total_riscos)
k2.metric("Média do Nível de Risco", media_nivel)
k3.metric("Riscos Críticos", riscos_criticos)

st.markdown("---")

# Distribuição de Classificação
st.subheader("Distribuição de Classificação de Risco")
fig1, ax1 = plt.subplots()
df['classificacao'].value_counts().plot(kind='bar', ax=ax1)
ax1.set_xlabel('Classificação')
ax1.set_ylabel('Quantidade')
st.pyplot(fig1)

# Heatmap Probabilidade vs Impacto
st.subheader("Matriz de Distribuição (Probabilidade x Impacto)")
pivot = df.pivot_table(
    index='probabilidade',
    columns='nivel_impacto',
    values='nivel_risco',
    aggfunc='count',
    fill_value=0
)
fig2, ax2 = plt.subplots()
cax = ax2.imshow(pivot, aspect='auto', origin='lower')
fig2.colorbar(cax, ax=ax2)
ax2.set_xlabel('Nível de Impacto')
ax2.set_ylabel('Probabilidade')
ax2.set_xticks(np.arange(len(pivot.columns)))
ax2.set_xticklabels(pivot.columns)
ax2.set_yticks(np.arange(len(pivot.index)))
ax2.set_yticklabels(pivot.index)
st.pyplot(fig2)

# Controles Existentes
st.subheader("Distribuição por Controles Existentes")
c1, c2 = st.columns(2)
fig3, ax3 = plt.subplots()
df['controle_m'].value_counts().plot(kind='barh', ax=ax3)
ax3.set_xlabel('Quantidade')
ax3.set_title('Controle Existência e Relevância')
c1.pyplot(fig3)

fig4, ax4 = plt.subplots()
df['controle_n'].value_counts().plot(kind='barh', ax=ax4)
ax4.set_xlabel('Quantidade')
ax4.set_title('Controle Funcionamento')
c2.pyplot(fig4)

st.markdown("---")

# Tabela detalhada
st.subheader("Detalhamento de Riscos")
cols = ['ID Risco ', 'Riscos', 'Categoria ', 'probabilidade',
        'nivel_impacto', 'nivel_risco', 'classificacao', 'controle_m', 'controle_n']
st.dataframe(df[cols], use_container_width=True)
