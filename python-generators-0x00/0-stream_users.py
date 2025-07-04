#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that yields rows one by one from the user_data table.
    Uses only one loop and no more than one query.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="samueljuma",
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
    except Error as e:
        print(f"MySQL Error: {e}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
