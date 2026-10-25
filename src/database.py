# src/database.py
import sqlite3
from contextlib import contextmanager
import os

# Caminho para o banco de dados dentro da pasta 'data'
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')

def init_db():
    """Inicializa o banco de dados e cria as tabelas necessárias."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Tabela para armazenar o histórico de versões e o payload bruto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS page_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                raw_html TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de Alertas estruturados para mudanças detectadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                change_type TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@contextmanager
def get_db_connection():
    """Gerenciador de contexto para conexões seguras com transações ACID."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()