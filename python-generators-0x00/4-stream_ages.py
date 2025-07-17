import mysql.connector

def stream_user_ages():
    """
    Generator that yields each user's age from the user_data table, one at a time.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Use secure password management in production
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:
            yield age
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def average_user_age():
    """
    Consumes the stream_user_ages generator and computes the average age.
    Prints result in the specified format.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    average_user_age()
