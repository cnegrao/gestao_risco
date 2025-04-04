import pandas as pd
# Certifique-se de que esse módulo está no diretório raiz
from database_utils import run_query, run_select


def adapt_params(params):
    """Converte parâmetros numéricos do NumPy para tipos nativos do Python."""
    return tuple((p.item() if hasattr(p, "item") else p) for p in (params or ()))


def get_count(table):
    """Retorna a quantidade de registros da tabela especificada."""
    result = run_select(f"SELECT COUNT(*) as count FROM {table};", None)
    # Supondo que run_select retorne um DataFrame
    return int(result.iloc[0]['count'])


# Leitura da planilha (ajuste o caminho conforme necessário)
df = pd.read_excel("riscos_com_processos_organizacionais_valida.xlsx")
print("Colunas da planilha:", df.columns.tolist())

# -------------------------------------------------------------------
# 1. Criação do registro de empresa padrão
default_company_id = 1
default_company_name = "Empresa Padrão"
run_query(
    """
    INSERT INTO tb_empresas (id_empresa, nome_empresa)
    VALUES (%s, %s)
    ON CONFLICT (id_empresa) DO NOTHING;
    """,
    adapt_params((default_company_id, default_company_name))
)
print("tb_empresas:", get_count("tb_empresas"))

# -------------------------------------------------------------------
# 2. Popula tb_processos (coluna "Processo")
process_map = {}
for proc in df['Processo'].unique():
    run_query(
        """
        INSERT INTO tb_processos (nome_processo)
        VALUES (%s)
        ON CONFLICT (nome_processo) DO NOTHING;
        """,
        adapt_params((proc,))
    )
    result = run_select(
        "SELECT id_processo FROM tb_processos WHERE nome_processo = %s;", adapt_params((proc,)))
    process_map[proc] = result.iloc[0]['id_processo']
print("tb_processos:", get_count("tb_processos"))

# -------------------------------------------------------------------
# 3. Popula tb_subprocessos (colunas "SubProcesso" e "Processo")
subproc_map = {}
unique_subproc = df[['SubProcesso', 'Processo']].drop_duplicates()
for _, row in unique_subproc.iterrows():
    subproc = row['SubProcesso']
    proc = row['Processo']
    id_processo = process_map[proc]
    run_query(
        """
        INSERT INTO tb_subprocessos (id_processo, nome_subprocesso)
        VALUES (%s, %s)
        ON CONFLICT (id_processo, nome_subprocesso) DO NOTHING;
        """,
        adapt_params((id_processo, subproc))
    )
    result = run_select(
        """
        SELECT id_subprocesso FROM tb_subprocessos
        WHERE id_processo = %s AND nome_subprocesso = %s;
        """,
        adapt_params((id_processo, subproc))
    )
    subproc_map[(subproc, proc)] = result.iloc[0]['id_subprocesso']
print("tb_subprocessos:", get_count("tb_subprocessos"))

# -------------------------------------------------------------------
# 4. Popula tb_categorias (coluna "categoria")
cat_map = {}
for cat in df['categoria'].unique():
    run_query(
        """
        INSERT INTO tb_categorias (nome_categoria)
        VALUES (%s)
        ON CONFLICT (nome_categoria) DO NOTHING;
        """,
        adapt_params((cat,))
    )
    result = run_select(
        "SELECT id_categoria FROM tb_categorias WHERE nome_categoria = %s;", adapt_params((cat,)))
    cat_map[cat] = result.iloc[0]['id_categoria']
print("tb_categorias:", get_count("tb_categorias"))

# -------------------------------------------------------------------
# 5. Popula tb_riscos
# Geramos id_risco com base no índice (começando em 1)
for idx, row in df.iterrows():
    id_risco = int(idx + 1)
    id_empresa = default_company_id
    nome_risco = row['nome_risco']
    descricao = row['descricao']
    impacto_estimado = row['impacto_estimado']
    probabilidade = row['probabilidade']
    status = row['status']
    data_identificacao = row['data_identificacao']
    criticidade = row['criticidade']
    # Obter id_processo usando a coluna "Processo"
    id_processo = process_map.get(row['Processo'])
    # Obter id_subprocesso usando (SubProcesso, Processo)
    id_subprocesso = subproc_map.get((row['SubProcesso'], row['Processo']))
    # Obter id_categoria usando a coluna "categoria"
    id_categoria = cat_map.get(row['categoria'])

    run_query(
        """
        INSERT INTO tb_riscos 
            (id_risco, id_empresa, nome_risco, descricao, impacto_estimado, probabilidade, status, data_identificacao, criticidade, id_processo, id_subprocesso, id_categoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id_risco) DO NOTHING;
        """,
        adapt_params((id_risco, id_empresa, nome_risco, descricao, impacto_estimado, probabilidade,
                     status, data_identificacao, criticidade, id_processo, id_subprocesso, id_categoria))
    )
print("tb_riscos:", get_count("tb_riscos"))

# -------------------------------------------------------------------
# 6. Popula tb_causas (coluna "causa")
cause_map = {}
for causa in df['causa'].unique():
    run_query(
        """
        INSERT INTO tb_causas (descricao_causa)
        VALUES (%s)
        ON CONFLICT (descricao_causa) DO NOTHING;
        """,
        adapt_params((causa,))
    )
    result = run_select(
        "SELECT id_causa FROM tb_causas WHERE descricao_causa = %s;", adapt_params((causa,)))
    cause_map[causa] = result.iloc[0]['id_causa']
print("tb_causas:", get_count("tb_causas"))

# -------------------------------------------------------------------
# 7. Popula tb_consequencias (coluna "consequencia")
cons_map = {}
for cons in df['consequencia'].unique():
    run_query(
        """
        INSERT INTO tb_consequencias (descricao_consequencia)
        VALUES (%s)
        ON CONFLICT (descricao_consequencia) DO NOTHING;
        """,
        adapt_params((cons,))
    )
    result = run_select(
        "SELECT id_consequencia FROM tb_consequencias WHERE descricao_consequencia = %s;", adapt_params((cons,)))
    cons_map[cons] = result.iloc[0]['id_consequencia']
print("tb_consequencias:", get_count("tb_consequencias"))

# -------------------------------------------------------------------
# 8. Popula as tabelas de associação tb_risco_causa e tb_risco_consequencia
for idx, row in df.iterrows():
    id_risco = int(idx + 1)
    causa = row['causa']
    consequencia = row['consequencia']
    id_causa = cause_map.get(causa)
    id_consequencia = cons_map.get(consequencia)

    run_query(
        """
        INSERT INTO tb_risco_causa (id_risco, id_causa)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
        """,
        adapt_params((id_risco, id_causa))
    )

    run_query(
        """
        INSERT INTO tb_risco_consequencia (id_risco, id_consequencia)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
        """,
        adapt_params((id_risco, id_consequencia))
    )
print("tb_risco_causa:", get_count("tb_risco_causa"))
print("tb_risco_consequencia:", get_count("tb_risco_consequencia"))
