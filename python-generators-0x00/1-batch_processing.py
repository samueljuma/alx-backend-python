#!/usr/bin/env python3
"""
1-batch_processing.py
Stream user rows in batches and process them with a generator‑driven workflow.
"""

import mysql.connector
from mysql.connector import Error


# ──────────────────────────────────────────────────────────────────────────────
# Database connection settings
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "samueljuma"
DATABASE = "ALX_prodev"
TABLE = "user_data"
# ──────────────────────────────────────────────────────────────────────────────


def stream_users_in_batches(batch_size):
    """
    Generator that yields lists of rows (batches) from the user_data table.

    Uses only one loop (a `while` that calls cursor.fetchmany).
    """
    try:
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
        )
        cursor = conn.cursor()  # tuple rows: (uuid, name, email, age)
        cursor.execute(f"SELECT * FROM {TABLE};")

        while True:                              # ➊ LOOP #1
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    except Error as e:
        print(f"MySQL error: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def batch_processing(batch_size):
    """
    Streams users in batches, prints only those whose age > 25.

    Contains two explicit loops:
      ➋ outer `for` over batches
      ➌ inner `for` over rows within a batch
    """
    for batch in stream_users_in_batches(batch_size):        # ➋ LOOP #2
        for row in batch:                                    # ➌ LOOP #3
            # row format: (user_id, name, email, age)
            if row[3] > 25:
                print(row)

