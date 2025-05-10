import configparser
import contextlib
import platform
from pathlib import Path

import pandas as pd
import psycopg2

# Import apenas em produção (Streamlit Cloud)
try:
    import streamlit as st
except ImportError:
    st = None

BASE_DIR = Path(__file__).parent.resolve()
INI_PATH = BASE_DIR / "config" / "config.ini"


def load_db_config():
    """
    - Windows (DEV): lê config.ini
    - Linux / Streamlit (PROD): usa st.secrets["DATABASE"]
    """
    is_windows = platform.system().lower().startswith("win")
    if is_windows or st is None:
        # Desenvolvimento local
        parser = configparser.ConfigParser()
        parser.read(INI_PATH)
        db = parser["DATABASE"]
        return {
            "dbname":   db.get("DATABASE"),
            "user":     db.get("USER"),
            "password": db.get("PASSWORD"),
            "host":     db.get("HOST"),
            "port":     db.get("PORT", "5432"),
        }
    else:
        # Produção no Streamlit Cloud
        cfg = st.secrets["DATABASE"]
        # Se tiver URL (DSN) completo:
        if "url" in cfg:
            return {"dsn": cfg["url"]}
        # Senão, espera as chaves separadas:
        return {
            "dbname":   cfg.get("database") or cfg.get("DATABASE"),
            "user":     cfg.get("user") or cfg.get("USER"),
            "password": cfg.get("password") or cfg.get("PASSWORD"),
            "host":     cfg.get("host") or cfg.get("HOST"),
            "port":     cfg.get("port") or cfg.get("PORT", 5432),
        }


@contextlib.contextmanager
def db_connection():
    """
    Abre/fecha conexão:
     - kwargs em DEV (Windows)
     - dsn em PROD (Streamlit)
    """
    cfg = load_db_config()

    if "dsn" in cfg:
        conn = psycopg2.connect(cfg["dsn"])
    else:
        conn = psycopg2.connect(**cfg)
    try:
        yield conn
    finally:
        conn.close()


def run_select(sql_query: str, params: tuple = None) -> pd.DataFrame:
    """
    Executa SELECT e retorna DataFrame.
    """
    with db_connection() as conn:
        return pd.read_sql(sql_query, conn, params=params)


def run_query(sql_query: str, params: tuple = None) -> None:
    """
    Executa INSERT/UPDATE/DELETE e efetiva commit.
    """
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, params or ())
            conn.commit()
