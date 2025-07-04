
import csv
import uuid
import mysql.connector
from mysql.connector import Error

# --------------------------------------------------------------------------- #
# Connection parameters
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "samueljuma"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

# ---------- Core helpers --------------------------------------------------- #
def _get_connection(**kwargs):
    """Low‑level connector wrapper with common parameters."""
    return mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        **kwargs,
    )

# --- Connect to db -------------------------------------------------- #
def connect_db():
    """
    Connects to the MySQL *server* (no default schema).
    Returns a connection or None on failure.
    """
    try:
        return _get_connection()
    except Error as e:
        print(f"[connect_db] MySQL error: {e}")
        return None

# -- create database -------------------------------------------------- #
def create_database(connection):
    """Creates database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    connection.commit()
    cursor.close()


# -- connect to ALX_prodev schema ------------------------------------- #
def connect_to_prodev():
    """
    Connects straight to the ALX_prodev schema.
    Returns a connection or None on failure.
    """
    try:
        return _get_connection(database=DB_NAME)
    except Error as e:
        print(f"[connect_to_prodev] MySQL error: {e}")
        return None

# -- create user_data table ------------------------------------------ #
def create_table(connection):
    """Creates the user_data table if absent (UUID PK, indexed)."""
    cursor = connection.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY,
            name    VARCHAR(255) NOT NULL,
            email   VARCHAR(255) NOT NULL,
            age     DECIMAL(3)   NOT NULL,
            INDEX idx_user_id (user_id)
        ) ENGINE=InnoDB;
        """
    )
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


# -- insert data from CSV --------------------------------------------- #
def insert_data(connection, csv_path):
    """
    Reads `csv_path` and inserts every row into user_data,
    generating a fresh UUID for each record.
    Duplicate emails are allowed.
    """
    cursor = connection.cursor()
    insert_sql = (
        f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    )

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute(
                insert_sql,
                (
                    str(uuid.uuid4()),
                    row["name"],
                    row["email"],
                    row["age"],
                ),
            )

    connection.commit()
    cursor.close()


# ---------- Generator for streaming rows ----------------------------------- #
def stream_users(connection):
    """
    Lazy generator that yields one row (as a dict) at a time from user_data.

    Usage:
        with connect_to_prodev() as conn:
            for row in seed.stream_users(conn):
                process(row)
    """
    cursor = connection.cursor(dictionary=True)  # dict rows for convenience
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    try:
        for record in cursor:
            yield record
    finally:
        cursor.close()
