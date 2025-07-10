#!/usr/bin/env python3
import sqlite3

# Setup database // For testing purposes
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER CHECK(age >= 0) DEFAULT 0
        )
    ''')
    cursor.executemany('''
        INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)
    ''', [
        ('Alice', 'alice@example.com', 25),
        ('Bob', 'bob@example.com', 30),
        ('Carol', 'carol@example.com', 11),
        ('Dave', 'dave@example.com', 45)
    ])
    conn.commit()
    conn.close()

setup_database()

class DatabaseConnection:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        print("[OPEN] Connecting to DB...")
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[CLOSE] Closing DB connection.")
        if self.conn:
            self.conn.close()

with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)

