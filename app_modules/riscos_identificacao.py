import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from database_utils import run_select, run_query
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# ------------------------------
# Configurações de estilo Sankey
# Ajuste estas variáveis para afinar o Sankey
NODE_PAD = 30           # Espaçamento interno dos nós
NODE_THICKNESS = 16     # Altura dos nós
NODE_LINE_WIDTH = 1     # Largura da borda dos nós
LINK_OPACITY = 0.5      # Opacidade dos links
LINK_LINE_WIDTH = 1     # Largura da borda dos links
# ------------------------------


def evenly_spaced_positions(n, start=0.1, end=0.9):
    """Retorna posições y uniformemente espaçadas para n nós."""
    if n <= 1:
        return [0.5]
    return [start + i * (end - start) / (n - 1) for i in range(n)]


def main():
    # Carrega CSS customizado
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

    # Cabeçalhos
    st.markdown(
        "<h1 style='font-size:32px; margin-bottom:4px;'>Fase 2 – Identificação de Riscos</h1>"
        "<h2 style='font-size:20px; margin-top:0; color:#ccc;'>SafeBis – Sistema de Gestão de Riscos</h2>",
        unsafe_allow_html=True
    )
    st.write(
        "Digite sua consulta para buscar riscos. A busca é textual (usando ILIKE) "
        "e os dados normalizados são usados para gerar o diagrama Causa & Efeito."
    )

    # Estado de sessão
    st.session_state.setdefault("search_query", "")
    st.session_state.setdefault("df_riscos", pd.DataFrame())

    # Formulário de busca
    with st.form(key="search_form"):
        query_input = st.text_input(
            "Digite o contexto do mapeamento de riscos:",
            value=st.session_state.search_query,
            key="input_search_query"
        )
        if st.form_submit_button("🔍 Buscar Riscos"):
            term = query_input.strip()
            if term:
                st.session_state.search_query = term
                like_q = f"%{term}%"
                sql = (
                    "SELECT r.id_risco, r.nome_risco, r.descricao, r.criticidade, p.nome_processo "
                    "FROM tb_riscos r "
                    "LEFT JOIN tb_subprocessos sp ON r.id_subprocesso = sp.id_subprocesso "
                    "LEFT JOIN tb_processos p ON sp.id_processo = p.id_processo "
                    "WHERE r.nome_risco ILIKE %s OR r.descricao ILIKE %s OR p.nome_processo ILIKE %s "
                    "ORDER BY r.data_identificacao DESC"
                )
                st.session_state.df_riscos = run_select(
                    sql, (like_q, like_q, like_q))
            else:
                st.warning("Digite uma consulta para buscar riscos.")

    # Exibe resultados
    df = st.session_state.df_riscos
    if isinstance(df, pd.DataFrame) and df.empty:
        st.info("Nenhum risco encontrado para a consulta.")
        return

    st.write("Riscos encontrados:")
    df_display = df[["id_risco", "nome_risco",
                     "descricao", "criticidade", "nome_processo"]]

    gb = GridOptionsBuilder.from_dataframe(df_display)
    gb.configure_selection("multiple", use_checkbox=True,
                           groupSelectsChildren=True,
                           suppressRowClickSelection=True)
    grid_opts = gb.build()

    grid_resp = AgGrid(
        df_display,
        gridOptions=grid_opts,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="ag-theme-alpine-dark",
        height=300,
        fit_columns_on_grid_load=True
    )

    # Normaliza seleção
    raw = grid_resp.get("selected_rows")
    if raw is None or (isinstance(raw, list) and not raw) or (isinstance(raw, pd.DataFrame) and raw.empty):
        selected = []
    else:
        selected = raw.to_dict("records") if isinstance(
            raw, pd.DataFrame) else raw

    st.write("IDs dos riscos selecionados:", [r['id_risco'] for r in selected])

    # Renderiza Sankey para cada risco selecionado
    for row in selected:
        sankey_df = run_select(
            "SELECT ca.descricao_causa AS causa, cons.descricao_consequencia AS consequencia "
            "FROM tb_risco_causa rc "
            "LEFT JOIN tb_causas ca ON rc.id_causa = ca.id_causa "
            "LEFT JOIN tb_risco_consequencia rcons ON rc.id_risco = rcons.id_risco "
            "LEFT JOIN tb_consequencias cons ON rcons.id_consequencia = cons.id_consequencia "
            "WHERE rc.id_risco = %s", (row['id_risco'],)
        )
        if sankey_df.empty:
            st.info(
                f"Nenhuma causa/consequência para o risco {row['id_risco']}")
            continue

        causes = sankey_df['causa'].dropna().unique().tolist()
        effects = sankey_df['consequencia'].dropna().unique().tolist()
        labels = causes + [row['nome_risco']] + effects
        nc = len(causes)

        # Define fontes, alvos e valores
        src = list(range(nc)) + [nc]*len(effects)
        tgt = [nc]*nc + [nc+1+i for i in range(len(effects))]
        vals = [1]*(nc+len(effects))

        # Calcula posições x, y
        xs = [0.0]*nc + [0.5] + [1.0]*len(effects)
        ys = evenly_spaced_positions(
            nc) + [0.5] + evenly_spaced_positions(len(effects))

        # Cria o gráfico Sankey
        fig = go.Figure(go.Sankey(
            arrangement="snap",
            node=dict(
                label=[""]*len(labels),  # labels via annotations
                pad=NODE_PAD,
                thickness=NODE_THICKNESS,
                line=dict(color="#222", width=NODE_LINE_WIDTH),
                color=["#005f88" if i !=
                       nc else "#FF6600" for i in range(len(labels))],
                x=xs, y=ys
            ),
            link=dict(
                source=src, target=tgt, value=vals,
                color=f"rgba(0,143,210,{LINK_OPACITY})",
                line=dict(color="#222", width=LINK_LINE_WIDTH)
            )
        ))

        # Anotações de cabeçalho acima do Sankey
        for pos, text, bg in [(0, 'Causa', '#005f88'), (0.5, 'Risco', '#0091c2'), (1, 'Consequência', '#005f88')]:
            fig.add_annotation(
                x=pos, y=1.1, xref='paper', yref='paper', showarrow=False,
                text=text, font=dict(size=16, color='#fff'), bgcolor=bg, borderpad=6
            )

        # Anotações dos labels nos nós
        for i, txt in enumerate(labels):
            fig.add_annotation(
                x=xs[i], y=ys[i], xref='paper', yref='paper', showarrow=False,
                text=txt, align='left', font=dict(size=12, color='#fff'),
                bgcolor='#1a1a1a', bordercolor='#444', borderpad=4
            )

        fig.update_layout(
            title_text=f"Causa & Efeito – Risco {row['id_risco']}: {row['nome_risco']}",
            title_x=0, font=dict(size=12, color='#fff'),
            margin=dict(t=100, l=20, r=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Formulário de salvamento
    with st.form(key="save_form"):
        user = st.text_input("Usuário", value="usuario_padrao")
        obs = st.text_area("Observações (opcional)")
        if st.form_submit_button("💾 Salvar Riscos Selecionados"):
            run_query(
                "CREATE TABLE IF NOT EXISTS tb_risco_selecionado ("
                "id_risco_selecionado SERIAL PRIMARY KEY,"
                "id_empresa INT REFERENCES tb_empresas(id_empresa),"
                "id_risco INT REFERENCES tb_riscos(id_risco),"
                "data_selecao DATE NOT NULL DEFAULT CURRENT_DATE,"
                "usuario VARCHAR(100), observacoes TEXT)"
            )
            count = 0
            for r in selected:
                run_query(
                    "INSERT INTO tb_risco_selecionado (id_empresa, id_risco, usuario, observacoes) VALUES (%s,%s,%s,%s)",
                    (1, r['id_risco'], user, obs)
                )
                count += 1
            st.success(f"{count} risco(s) salvo(s) com sucesso!")


if __name__ == "__main__":
    main()
