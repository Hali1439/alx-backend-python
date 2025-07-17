import mysql.connector
from mysql.connector import Error
from typing import Iterator, List, Dict, Any

def stream_users_in_batches(batch_size: int) -> Iterator[List[Dict[str, Any]]]:
    """
    Generator that yields batches of users from the user_data table.
    Each batch is a list of dicts, each dict represents a user.
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
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def batch_processing(batch_size: int):
    """
    Processes batches of users, filtering users over the age of 25.
    Prints each user as a dict.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
        return
