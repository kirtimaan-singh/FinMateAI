import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('finmate.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT, income REAL, risk_appetite TEXT
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO profile (id, name, income, risk_appetite) VALUES (1, "User", 50000, "Moderate")')
    conn.commit()
    return conn

conn = init_db()

def get_profile():
    return pd.read_sql_query("SELECT * FROM profile WHERE id=1", conn).iloc[0]

def update_profile(name, income, risk):
    cursor = conn.cursor()
    cursor.execute("UPDATE profile SET name=?, income=?, risk_appetite=? WHERE id=1", (name, income, risk))
    conn.commit()
