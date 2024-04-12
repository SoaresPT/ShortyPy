import sqlite3
from settings import DATABASE_NAME

# Function to create tables in SQLite database
def create_tables():
    # Change this to another db file if needed
    conn = sqlite3.connect(f"{DATABASE_NAME}.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shorturl TEXT NOT NULL,
            destination TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to execute SQL queries on the SQLite database
def execute_query(query, params=None):
    conn = sqlite3.connect(f"{DATABASE_NAME}.db")
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result
