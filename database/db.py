import streamlit as st
import psycopg2


def get_connection():

    return psycopg2.connect(
        st.secrets["DATABASE_URL"]
    )

def execute(query, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            query,
            params or ()
        )
        conn.commit()

    finally:
        conn.close()
        
def fetch_one(query, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            query,
            params or ()
        )
        row = cur.fetchone()

        return row

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
