#!/usr/bin/python3

import sys
import os

import seed

def main():
    # Step 1: Connect to MySQL (no DB selected)
    connection = seed.connect_db()
    if not connection:
        print("Failed to connect to MySQL server.", file=sys.stderr)
        sys.exit(1)

    # Step 2: Create database if needed
    seed.create_database(connection)
    connection.close()
    print("connection successful")

    # Step 3: Connect to ALX_prodev DB
    connection = seed.connect_to_prodev()
    if not connection:
        print("Failed to connect to ALX_prodev database.", file=sys.stderr)
        sys.exit(1)

    # Step 4: Create table if needed
    seed.create_table(connection)

    # Step 5: Insert data from CSV
    csv_path = 'user_data.csv'
    if not os.path.isfile(csv_path):
        print(f"CSV file {csv_path} not found.", file=sys.stderr)
        connection.close()
        sys.exit(1)
    seed.insert_data(connection, csv_path)

    # Step 6: Validate schema and print sample data
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s;",
            (seed.DB_NAME,)
        )
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present ")

        cursor.execute(f"SELECT * FROM {seed.TABLE_NAME} LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
