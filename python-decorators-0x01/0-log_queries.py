#!/usr/bin/env python3

import sqlite3
import functools
from datetime import datetime

# Setup database // For testing purposes
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.executemany('''
        INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)
    ''', [
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Carol', 'carol@example.com')
    ])
    conn.commit()
    conn.close()

setup_database()


# Decorator
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] [SQL LOG] Query to be executed: {args[0]}")
        return func(*args, **kwargs)
    return wrapper

# Use of decorator
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


users = fetch_all_users("SELECT * FROM users where name like 'A%'")
print(users)
