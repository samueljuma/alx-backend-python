#!/usr/bin/env python3
import time
import sqlite3
import functools

# Global cache - a simple dictionary to store query results
query_cache = {}

# DB connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]
        
        print(f"[CACHE MISS] Executing and caching result for query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Cached fetch
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — caches result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call — uses cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
