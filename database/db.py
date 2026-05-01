import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT,
            status TEXT,
            servicenow_id TEXT,
            jira_id TEXT,
            azure_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

