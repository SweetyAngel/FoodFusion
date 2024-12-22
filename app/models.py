import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS products
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL);''')
    conn.commit()
    conn.close()
