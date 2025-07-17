import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator that yields one row at a time from the user_data table in ALX_prodev.
    Each row is yielded as a dict with keys: user_id, name, email, age.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Parameterize or secure in production
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        for row in cursor:
            yield row
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
