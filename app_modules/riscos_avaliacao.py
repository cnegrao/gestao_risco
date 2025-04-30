import sys
import os
import streamlit as st
import pandas as pd
from database_utils import run_select, run_query

# Para exibir a matriz de riscos em formato de heatmap (plotly)
import plotly.graph_objs as go

# ---------------------------------------------
# Ajuste para encontrar database_utils.py (caso esteja na raiz do projeto)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# ---------------------------------------------

# st.set_page_config(page_title="Fase 3 - Avaliação de Riscos", layout="wide")


def main():
    st.title("Fase 3 – Avaliação de Riscos")
    st.markdown("""
    **Objetivo:** Avaliar os riscos cadastrados na fase anterior, preenchendo:
    - Probabilidade (1 a 5)
    - Impactos em três dimensões (Financeiro, Imagem e Conformidade)
    - Cálculo do impacto final (máximo dos três)
    - Nível do Risco = probabilidade × impacto_final (1..25)
    - Classificação do Risco (Pequeno, Moderado, Alto, Crítico)

    As informações serão gravadas nas colunas recém-adicionadas em **tb_riscos**.
    """)

    # Consulta os riscos cadastrados
    query_riscos = "SELECT id_risco, nome_risco FROM tb_riscos ORDER BY data_identificacao DESC"
    df_riscos = run_select(query_riscos)

    if df_riscos.empty:
        st.warning("⚠️ Nenhum risco cadastrado disponível para avaliação.")
        return

    # Selecionar o risco para avaliação
    risco_selecionado = st.selectbox(
        "Selecione um Risco para Avaliação", df_riscos["nome_risco"])
    id_risco = df_riscos.loc[df_riscos["nome_risco"]
                             == risco_selecionado, "id_risco"].iloc[0]

    st.subheader("Passo 1: Probabilidade de Ocorrência")
    probabilidade = st.slider("Probabilidade (1 a 5)",
                              min_value=1, max_value=5, value=3)

    st.subheader("Passo 2: Avaliação dos Impactos (1 a 5 cada)")
    col1, col2, col3 = st.columns(3)
    with col1:
        impacto_financeiro = st.slider("Impacto Financeiro", 1, 5, 3)
    with col2:
        impacto_imagem = st.slider("Impacto na Imagem", 1, 5, 3)
    with col3:
        impacto_conformidade = st.slider("Impacto na Conformidade", 1, 5, 3)

    # Calcula o impacto final como o máximo entre as três dimensões
    impacto_final = max(impacto_financeiro, impacto_imagem,
                        impacto_conformidade)
    nivel_risco = probabilidade * impacto_final

    # Determina a classificação
    if 1 <= nivel_risco <= 5:
        classificacao = "Pequeno"
    elif 6 <= nivel_risco <= 10:
        classificacao = "Moderado"
    elif 11 <= nivel_risco <= 15:
        classificacao = "Alto"
    else:
        classificacao = "Crítico"

    st.markdown("---")
    st.write(f"**Probabilidade:** {probabilidade}")
    st.write(
        f"**Impacto Financeiro:** {impacto_financeiro}, **Imagem:** {impacto_imagem}, **Conformidade:** {impacto_conformidade}")
    st.write(f"**Impacto Final (máximo):** {impacto_final}")
    st.write(f"**Nível de Risco:** {nivel_risco}")
    st.write(f"**Classificação do Risco:** {classificacao}")

    # Botão para salvar no banco
    if st.button("💾 Salvar Avaliação"):
        try:
            update_query = """
            UPDATE tb_riscos
               SET probabilidade = %s,
                   impacto_financeiro = %s,
                   impacto_imagem = %s,
                   impacto_conformidade = %s,
                   impacto_estimado = %s,
                   nivel_risco = %s,
                   criticidade = %s
             WHERE id_risco = %s;
            """
            params = (
                str(probabilidade),
                str(impacto_financeiro),
                str(impacto_imagem),
                str(impacto_conformidade),
                str(impacto_final),
                nivel_risco,
                classificacao,
                id_risco
            )
            run_query(update_query, params)
            st.success("✅ Avaliação salva com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao salvar avaliação: {e}")

    st.markdown("---")
    st.subheader("Avaliações Realizadas")
    query_avaliacoes = """
        SELECT nome_risco,
               probabilidade,
               impacto_financeiro,
               impacto_imagem,
               impacto_conformidade,
               impacto_estimado,
               nivel_risco,
               criticidade,
               data_identificacao
          FROM tb_riscos
         WHERE probabilidade IS NOT NULL AND impacto_estimado IS NOT NULL
         ORDER BY data_identificacao DESC;
    """
    df_avaliacoes = run_select(query_avaliacoes)
    if df_avaliacoes is not None and not df_avaliacoes.empty:
        st.dataframe(df_avaliacoes, use_container_width=True)
    else:
        st.info("Nenhuma avaliação de risco registrada até o momento.")

    st.markdown("---")

    # Opção para exibir a matriz de riscos 5x5 (probabilidade x impacto)
    st.subheader("Matriz de Riscos 5x5")

    st.write("Esta matriz exibe no eixo X o impacto (1..5) e no eixo Y a probabilidade (1..5). "
             "O produto (probabilidade × impacto) varia de 1 a 25. "
             "Cores diferentes indicam a classificação (Pequeno, Moderado, Alto, Crítico).")

    # Cria a matriz 5x5 (probabilidade: linhas, impacto: colunas)
    # Cada célula tem valor = p*i
    z_vals = []
    text_vals = []
    for p in range(1, 6):
        row_z = []
        row_text = []
        for i in range(1, 6):
            val = p * i
            # Classificação textual
            if val <= 5:
                clas = "Pequeno"
            elif val <= 10:
                clas = "Moderado"
            elif val <= 15:
                clas = "Alto"
            else:
                clas = "Crítico"
            row_z.append(val)
            row_text.append(clas)
        z_vals.append(row_z)
        text_vals.append(row_text)

    # Plotly: Heatmap com 5x5
    # Eixo x: Impacto 1..5
    # Eixo y: Probabilidade 1..5
    # "orientation" - se quisermos prob 1 no topo ou no bottom
    impact_labels = [str(i) for i in range(1, 6)]
    prob_labels = [str(i) for i in range(1, 6)]

    # Cores customizadas (pequeno => verde, moderado => amarelo, alto => orange, crítico => red)
    # Precisamos normalizar 1..25 => range 0..1
    # e.g: 1 => 0.0, 5 => 0.16, 10 => 0.36, 15 => 0.56, 25 => 1.0
    custom_colorscale = [
        [0.0, "green"],     # val = 1
        [0.2, "green"],
        [0.21, "yellow"],   # val ~5
        [0.4, "yellow"],
        [0.41, "orange"],   # val ~10
        [0.6, "orange"],
        [0.61, "red"],      # val ~15
        [1.0, "red"]        # val ~25
    ]

    fig = go.Figure(data=go.Heatmap(
        x=impact_labels,
        # Reverte y para exibir prob=1 em cima e prob=5 em baixo, se desejado
        y=prob_labels[::-1],
        z=z_vals[::-1],       # Aplica a mesma reversão nas linhas
        text=[row for row in text_vals[::-1]],
        hovertemplate="Probabilidade=%{y}<br>Impacto=%{x}<br>Nível=%{z}<br>Classificação=%{text}",
        colorscale=custom_colorscale,
        zmin=1,
        zmax=25,
        showscale=True,
        texttemplate="%{text}",
        textfont={"size": 14},
    ))

    # Rótulos e layout
    fig.update_layout(
        title="Matriz de Riscos 5x5 (Probabilidade × Impacto)",
        xaxis=dict(title="Impacto (1 = Baixo, 5 = Muito Alto)"),
        yaxis=dict(title="Probabilidade (1 = Baixa, 5 = Muito Alta)",
                   autorange="reversed")
    )

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
