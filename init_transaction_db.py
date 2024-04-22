import sqlite3


def initialize_db():
    conn = sqlite3.connect('kafka/transaction_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()