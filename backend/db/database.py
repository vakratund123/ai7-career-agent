import sqlite3
import os
import logging
from contextlib import contextmanager
from backend.core.config import DB_PATH, BACKEND_DIR

logger = logging.getLogger("ai7.database")

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=20.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for high concurrency
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

@contextmanager
def get_db():
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database transaction error: {e}")
        raise e
    finally:
        conn.close()

def init_db():
    schema_path = BACKEND_DIR / "db" / "schema.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_db() as conn:
        conn.executescript(schema_sql)
    logger.info(f"Database initialized successfully with WAL mode at {DB_PATH}")

if __name__ == "__main__":
    init_db()
    print("Database schema successfully applied.")
