import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create tables for user credentials and results
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS results (
    username TEXT,
    glucose REAL,
    bmi REAL,
    prediction TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("Database initialized successfully.")
