# carrega.py

import re
from pathlib import Path

import pandas as pd

# 1) Carrega o CSV exportado do Google Sheets (separador TAB)
csv_path = r'D:\projetoGestaoRiscos\data\stg_Analise_riscos4.csv'
df = pd.read_csv(csv_path, sep='\t')

# 2) Limpa os nomes de coluna para snake_case (PostgreSQL-friendly)
orig_cols = df.columns.tolist()
clean_cols = []
for col in orig_cols:
    c = col.strip().lower()
    c = re.sub(r'[^\w]', '_', c)
    c = re.sub(r'__+', '_', c)
    c = c.strip('_')
    clean_cols.append(c)
df.columns = clean_cols

# 3) Mapeia tipos pandas → PostgreSQL
dtype_map = {
    'int64': 'integer',
    'float64': 'double precision',
    'object': 'text',
    'bool': 'boolean',
    'datetime64[ns]': 'timestamp without time zone',
}

# 4) Gera o DDL
table_name = 'public.stg_analise_riscos_raw'
cols_ddl = []
for col, dtype in zip(df.columns, df.dtypes.astype(str)):
    pg_type = dtype_map.get(dtype, 'text')
    cols_ddl.append("    {col} {typ}".format(col=col, typ=pg_type))

ddl = """-- AUTO-GENERATED DDL
DROP TABLE IF EXISTS {table};

CREATE TABLE {table} (
{columns}
);

ALTER TABLE {table} OWNER TO postgres;
""".format(
    table=table_name,
    columns=",\n".join(cols_ddl)
)

# Salva DDL
ddl_path = Path(
    r'D:\projetoGestaoRiscos\data\create_stg_analise_riscos_raw.sql')
ddl_path.write_text(ddl, encoding='utf-8')
print("DDL salva em", ddl_path)

# 5) Gera INSERTs
insert_lines = []
cols_list = ", ".join(df.columns)
for _, row in df.iterrows():
    vals = []
    for col in df.columns:
        v = row[col]
        if pd.isna(v):
            vals.append('NULL')
        else:
            s = str(v).replace("'", "''")
            vals.append("'{0}'".format(s))
    insert_lines.append(
        "INSERT INTO {table} ({cols}) VALUES ({vals});".format(
            table=table_name,
            cols=cols_list,
            vals=", ".join(vals)
        )
    )

# Salva INSERTs
ins_path = Path(r'D:\projetoGestaoRiscos\data\insert_riscos.sql')
ins_path.write_text("\n".join(insert_lines), encoding='utf-8')
print("Script de INSERTs salvo em", ins_path)
