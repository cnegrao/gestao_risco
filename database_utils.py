import configparser
import contextlib
import logging
import platform
from pathlib import Path

import pandas as pd
from psycopg2.pool import ThreadedConnectionPool

try:
    import streamlit as st
except ImportError:
    st = None

# Configurações de logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).parent.resolve()
INI_PATH = BASE_DIR / "config" / "config.ini"


def load_db_config() -> dict:
    """
    Carrega configuração de DB:
     - DEV (Windows ou st ausente): config.ini
     - PROD (Streamlit Cloud): st.secrets["DATABASE"]
    Retorna dict com 'dsn'.
    """
    is_dev = platform.system().lower().startswith("win") or st is None
    if is_dev:
        parser = configparser.ConfigParser()
        parser.read(INI_PATH)
        db = parser["DATABASE"]
        return {"dsn": db["URL"]}
    else:
        cfg = st.secrets["DATABASE"]
        url = cfg.get("URL") or cfg.get("url")
        if "sslmode" not in url:
            url += "?sslmode=require"
        return {"dsn": url}


@st.cache_resource(show_spinner=False)
def get_connection_pool() -> ThreadedConnectionPool:
    cfg = load_db_config()
    logging.info("Criando pool de conexões com Supabase...")
    return ThreadedConnectionPool(minconn=1, maxconn=5, dsn=cfg["dsn"])


@contextlib.contextmanager
def db_connection():
    """Gerencia conexões reaproveitando o pool."""
    pool = get_connection_pool()
    conn = pool.getconn()
    try:
        yield conn
    except Exception:
        logging.exception("Erro na conexão ou query")
        raise
    finally:
        pool.putconn(conn)


@st.cache_data(ttl=300, show_spinner=False)
def run_select(sql_query: str, params: tuple = None) -> pd.DataFrame:
    """Executa SELECT, retorna DataFrame e faz cache por 5 minutos."""
    logging.info("Executando SELECT: %s | params: %s", sql_query, params)
    with db_connection() as conn:
        return pd.read_sql(sql_query, conn, params=params)


def run_query(sql_query: str, params: tuple = None) -> None:
    """Executa INSERT/UPDATE/DELETE e faz commit imediato."""
    logging.info("Executando QUERY: %s | params: %s", sql_query, params)
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, params or ())
        conn.commit()
