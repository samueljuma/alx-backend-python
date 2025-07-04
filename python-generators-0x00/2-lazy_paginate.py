#!/usr/env/bin python3
"""
2-lazy_paginate.py
Implements lazy pagination of user_data using a generator.
"""

seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database using LIMIT/OFFSET.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches user data page by page.
    Only one loop is used.
    """
    offset = 0
    while True:  # ✅ SINGLE LOOP
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
