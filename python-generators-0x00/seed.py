import csv
import uuid
import mysql.connector
from mysql.connector import Error
from typing import Optional

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_db() -> Optional[mysql.connector.MySQLConnection]:
    """Connect to the MySQL server (not a specific DB)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # TODO: parameterize or load from env
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection) -> None:
    """Create ALX_prodev database if not exists."""
    cursor = connection.cursor()
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
    finally:
        cursor.close()

def connect_to_prodev() -> Optional[mysql.connector.MySQLConnection]:
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # TODO: parameterize or load from env
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to {DB_NAME}: {e}")
        return None

def create_table(connection) -> None:
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        print("Table user_data created successfully")
    finally:
        cursor.close()

def insert_data(connection, csv_path: str) -> None:
    """Insert CSV data into the user_data table, avoiding duplicates."""
    cursor = connection.cursor()
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['user_id']
                name = row['name']
                email = row['email']
                age = row['age']
                # Idempotent insert: ignore if exists
                cursor.execute(
                    f"""INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)""",
                    (user_id, name, email, age)
                )
        connection.commit()
    finally:
        cursor.close()
