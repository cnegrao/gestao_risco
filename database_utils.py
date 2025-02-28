import psycopg2
import contextlib
import configparser
import pandas as pd


@contextlib.contextmanager
def db_connection():
    """Cria e gerencia a conexão com o banco de dados PostgreSQL."""
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    dbname = config["DATABASE"]["DATABASE"]
    user = config["DATABASE"]["USER"]
    password = config["DATABASE"]["PASSWORD"]
    host = config["DATABASE"]["HOST"]
    port = config["DATABASE"].get("PORT", "5432")

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    try:
        yield conn
    finally:
        conn.close()


def run_select(sql_query, params=None):
    """Executa um SELECT e retorna os dados como um DataFrame."""
    with db_connection() as conn:
        return pd.read_sql(sql_query, conn, params=params)


def run_query(sql_query, params=None):
    """Executa uma query de INSERT, UPDATE ou DELETE."""
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, params or ())
            conn.commit()
