import sqlite3
from pathlib import Path

# Đường dẫn thư mục dự án
BASE_DIR = Path(__file__).resolve().parent.parent

# File database
DB_PATH = BASE_DIR / "data" / "notes.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def execute(query, params=()):
    """
    Thực thi INSERT/UPDATE/DELETE.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

    finally:
        conn.close()


def fetch_one(query, params=()):
    """
    Lấy một bản ghi.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    finally:
        conn.close()


def fetch_all(query, params=()):
    """
    Lấy nhiều bản ghi.
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    finally:
        conn.close()