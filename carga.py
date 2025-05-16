import pandas as pd

# O módulo já gerencia a conexão via context manager
from database_utils import run_query, run_select


def adapt_params(params):
    """Converte parâmetros numéricos do NumPy para tipos nativos do Python."""
    return tuple((p.item() if hasattr(p, "item") else p) for p in (params or ()))


# Mapeamento dos nomes das tabelas para suas colunas de chave primária
pk_map = {
    "tb_processos": "id_processo",
    "tb_subprocessos": "id_subprocesso",
    "tb_categorias": "id_categoria",
    "tb_causas": "id_causa",
    "tb_consequencias": "id_consequencia",
}


def insert_if_not_exists(table, column, value):
    """Tenta selecionar o registro; se não existir, insere e então retorna o ID.
    Usa o mapeamento pk_map para obter o nome da coluna de chave primária.
    """
    pk_col = pk_map.get(table)
    if not pk_col:
        raise Exception(f"PK para a tabela {table} não está mapeado.")

    select_query = f"SELECT {pk_col} FROM {table} WHERE {column} = %s;"
    result = run_select(select_query, adapt_params((value,)))
    if not result.empty:
        return result.iloc[0][pk_col]
    else:
        # Executa o INSERT e depois faz o SELECT para recuperar o ID
        insert_query = f"INSERT INTO {table} ({column}) VALUES (%s);"
        run_query(insert_query, adapt_params((value,)))
        result = run_select(select_query, adapt_params((value,)))
        return result.iloc[0][pk_col]


def process_etl():
    # Leitura da planilha – ajuste o caminho conforme necessário
    df = pd.read_excel("riscos_com_processos_organizacionais_valida.xlsx")
    print("Colunas da planilha:", df.columns.tolist())

    # -------------------------------------------------------------------
    # 1. Criação de Empresa Padrão
    default_company_id = 1
    default_company_name = "Empresa Padrão"
    run_query(
        """
        INSERT INTO tb_empresas (id_empresa, nome_empresa)
        VALUES (%s, %s)
        ON CONFLICT (id_empresa) DO NOTHING;
        """,
        adapt_params((default_company_id, default_company_name)),
    )

    # -------------------------------------------------------------------
    # 2. Processos
    process_map = {}
    for proc in df["Processo"].unique():
        proc_id = insert_if_not_exists("tb_processos", "nome_processo", proc)
        process_map[proc] = proc_id
    print("tb_processos:", process_map)

    # -------------------------------------------------------------------
    # 3. SubProcessos
    subproc_map = {}
    unique_subproc = df[["SubProcesso", "Processo"]].drop_duplicates()
    for _, row in unique_subproc.iterrows():
        subproc = row["SubProcesso"]
        proc = row["Processo"]
        id_processo = process_map[proc]
        select_subproc = "SELECT id_subprocesso FROM tb_subprocessos WHERE id_processo = %s AND nome_subprocesso = %s;"
        result = run_select(select_subproc, adapt_params((id_processo, subproc)))
        if not result.empty:
            subproc_map[(subproc, proc)] = result.iloc[0]["id_subprocesso"]
        else:
            insert_subproc = (
                "INSERT INTO tb_subprocessos (id_processo, nome_subprocesso) VALUES (%s, %s);"
            )
            run_query(insert_subproc, adapt_params((id_processo, subproc)))
            result = run_select(select_subproc, adapt_params((id_processo, subproc)))
            subproc_map[(subproc, proc)] = result.iloc[0]["id_subprocesso"]
    print("tb_subprocessos:", subproc_map)

    # -------------------------------------------------------------------
    # 4. Categorias
    cat_map = {}
    for cat in df["categoria"].unique():
        cat_id = insert_if_not_exists("tb_categorias", "nome_categoria", cat)
        cat_map[cat] = cat_id
    print("tb_categorias:", cat_map)

    # -------------------------------------------------------------------
    # 5. Causas e Consequências (fazendo split por vírgula)
    cause_map = {}
    # Percorre cada valor único na coluna 'causa'
    for cause_str in df["causa"].dropna().unique():
        # Divide a string em itens individuais
        causes = [item.strip() for item in cause_str.split(",") if item.strip()]
        for cause in causes:
            cause_id = insert_if_not_exists("tb_causas", "descricao_causa", cause)
            cause_map[cause] = cause_id
    print("tb_causas:", cause_map)

    cons_map = {}
    for cons_str in df["consequencia"].dropna().unique():
        cons_list = [item.strip() for item in cons_str.split(",") if item.strip()]
        for cons in cons_list:
            cons_id = insert_if_not_exists("tb_consequencias", "descricao_consequencia", cons)
            cons_map[cons] = cons_id
    print("tb_consequencias:", cons_map)

    # -------------------------------------------------------------------
    # 6. Inserção de Riscos e dos Relacionamentos
    for idx, row in df.iterrows():
        id_risco = int(idx + 1)
        id_empresa = default_company_id
        nome_risco = row["nome_risco"]
        descricao = row["descricao"]
        impacto_estimado = row["impacto_estimado"]
        probabilidade = row["probabilidade"]
        status = row["status"]
        data_identificacao = row["data_identificacao"]
        criticidade = row["criticidade"]
        id_processo = process_map.get(row["Processo"])
        id_subprocesso = subproc_map.get((row["SubProcesso"], row["Processo"]))
        id_categoria = cat_map.get(row["categoria"])

        insert_risco = """
            INSERT INTO tb_riscos 
                (id_risco, id_empresa, nome_risco, descricao, impacto_estimado, probabilidade, status, data_identificacao, criticidade, id_processo, id_subprocesso, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_risco) DO NOTHING;
        """
        run_query(
            insert_risco,
            adapt_params(
                (
                    id_risco,
                    id_empresa,
                    nome_risco,
                    descricao,
                    impacto_estimado,
                    probabilidade,
                    status,
                    data_identificacao,
                    criticidade,
                    id_processo,
                    id_subprocesso,
                    id_categoria,
                )
            ),
        )

        # Processa as causas para este risco – faz split e insere cada item na tabela associativa
        if pd.notna(row["causa"]):
            causes = [item.strip() for item in row["causa"].split(",") if item.strip()]
            for cause in causes:
                id_causa = cause_map.get(cause)
                if id_causa:
                    insert_rc = "INSERT INTO tb_risco_causa (id_risco, id_causa) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
                    run_query(insert_rc, adapt_params((id_risco, id_causa)))

        # Processa as consequências para este risco
        if pd.notna(row["consequencia"]):
            consequences = [item.strip() for item in row["consequencia"].split(",") if item.strip()]
            for cons in consequences:
                id_cons = cons_map.get(cons)
                if id_cons:
                    insert_rcons = "INSERT INTO tb_risco_consequencia (id_risco, id_consequencia) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
                    run_query(insert_rcons, adapt_params((id_risco, id_cons)))
    print("Carga finalizada.")

    # -------------------------------------------------------------------
    # 7. Criação da tabela tb_risco_selecionado (caso não exista)
    create_risco_selecionado = """
    CREATE TABLE IF NOT EXISTS tb_risco_selecionado (
      id_risco_selecionado SERIAL PRIMARY KEY,
      id_empresa INT REFERENCES tb_empresas(id_empresa),
      id_risco INT REFERENCES tb_riscos(id_risco),
      data_selecao DATE NOT NULL DEFAULT CURRENT_DATE,
      usuario VARCHAR(100),
      observacoes TEXT
    );
    """
    run_query(create_risco_selecionado, None)

    # Debug: imprimir contagens de registros de cada tabela
    for table in [
        "tb_empresas",
        "tb_processos",
        "tb_subprocessos",
        "tb_categorias",
        "tb_causas",
        "tb_consequencias",
        "tb_riscos",
        "tb_risco_causa",
        "tb_risco_consequencia",
        "tb_risco_selecionado",
    ]:
        result = run_select(f"SELECT COUNT(*) as count FROM {table};", None)
        print(f"{table}: {int(result.iloc[0]['count'])}")


if __name__ == "__main__":
    process_etl()
