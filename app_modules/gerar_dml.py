import pandas as pd

# Caminho do arquivo Excel (ajuste se necessário)
# arquivo = r'C:\Users\cnegr\Downloads\riscos_com_processos_organizacionais_valida (2).xlsx'

arquivo = r"C:\Users\cnegr\Downloads\riscos_com_processos_organizacionais_valida (2).xlsx"

df = pd.read_excel(arquivo)

# Exibe os nomes das colunas para confirmar a leitura
print("Colunas da planilha:", df.columns)

# Função para escapar aspas simples em strings SQL


def escape_str(val):
    if isinstance(val, str):
        return val.replace("'", "''")
    return val


# 0. Inserir um registro padrão em tb_empresas, pois a planilha não fornece essa informação.
print("-- INSERT default company into tb_empresas")
print(
    "INSERT INTO tb_empresas (nome_empresa, cnpj, setor_atuacao) VALUES ('Empresa Default', '00000000000100', 'Default');"
)

# 1. Inserir registros únicos na tabela tb_processos (coluna "Processo")
print("\n-- INSERTS para tb_processos")
processos = df["Processo"].drop_duplicates()
for proc in processos:
    proc_esc = escape_str(proc)
    print(f"INSERT INTO tb_processos (nome_processo) VALUES ('{proc_esc}');")

# 2. Inserir registros únicos na tabela tb_subprocessos (combinação de "Processo" e "SubProcesso")
print("\n-- INSERTS para tb_subprocessos")
subprocessos = df[["Processo", "SubProcesso"]].drop_duplicates()
for index, row in subprocessos.iterrows():
    processo = escape_str(row["Processo"])
    subprocesso = escape_str(row["SubProcesso"])
    print(
        f"INSERT INTO tb_subprocessos (id_processo, nome_subprocesso) VALUES ((SELECT id_processo FROM tb_processos WHERE nome_processo = '{processo}'), '{subprocesso}');"
    )

# 3. Inserir registros únicos na tabela tb_categorias (coluna "categoria")
print("\n-- INSERTS para tb_categorias")
categorias = df["categoria"].drop_duplicates()
for cat in categorias:
    cat_esc = escape_str(cat)
    print(f"INSERT INTO tb_categorias (nome_categoria) VALUES ('{cat_esc}');")

# 4. Inserir registros na tabela tb_subcategorias
# Para cada categoria, insere uma subcategoria com o mesmo nome (padrão)
print("\n-- INSERTS para tb_subcategorias (subcategoria padrão igual à categoria)")
for cat in categorias:
    cat_esc = escape_str(cat)
    print(
        f"INSERT INTO tb_subcategorias (id_categoria, nome_subcategoria) VALUES ((SELECT id_categoria FROM tb_categorias WHERE nome_categoria = '{cat_esc}'), '{cat_esc}');"
    )

# 5. Inserir os registros de riscos na tabela tb_riscos
print("\n-- INSERTS para tb_riscos")
for index, row in df.iterrows():
    processo = escape_str(row["Processo"])
    subprocesso = escape_str(row["SubProcesso"])
    categoria = escape_str(row["categoria"])
    nome_risco = escape_str(row["nome_risco"])
    descricao = escape_str(row["descricao"])
    causa = escape_str(row["causa"])
    consequencia = escape_str(row["consequencia"])
    impacto = row["impacto_estimado"]
    probabilidade = row["probabilidade"]
    status = escape_str(row["status"])
    criticidade = escape_str(row["criticidade"])

    # Tratamento da data de identificação
    data_id = row["data_identificacao"]
    if pd.isnull(data_id):
        data_id_str = "CURRENT_DATE"
    else:
        try:
            # Tenta converter para datetime e formatar
            data_dt = pd.to_datetime(data_id)
            data_id_str = f"'{data_dt.strftime('%Y-%m-%d')}'"
        except Exception:
            # Se não for possível converter, usa o valor da string diretamente
            data_id_str = f"'{data_id}'"

    insert_risco = (
        "INSERT INTO tb_riscos (id_empresa, id_subprocesso, id_subcategoria, nome_risco, descricao, causa, consequencia, impacto_estimado, probabilidade, status, data_identificacao, criticidade) VALUES ("
        f"(SELECT id_empresa FROM tb_empresas WHERE nome_empresa = 'Empresa Default'), "
        f"(SELECT id_subprocesso FROM tb_subprocessos WHERE nome_subprocesso = '{subprocesso}'), "
        f"(SELECT id_subcategoria FROM tb_subcategorias WHERE nome_subcategoria = '{categoria}'), "
        f"'{nome_risco}', "
        f"'{descricao}', "
        f"'{causa}', "
        f"'{consequencia}', "
        f"{impacto}, "
        f"{probabilidade}, "
        f"'{status}', "
        f"{data_id_str}, "
        f"'{criticidade}');"
    )
    print(insert_risco)
