# python-generators-0x00

## Overview

This project demonstrates advanced usage of Python generators for efficient data processing, focusing on real-world scenarios such as streaming large datasets from an SQL database. The codebase is designed to be modular, maintainable, and extensible, using best practices in Python systems architecture.

---

## Features

- **Database Initialization**: Automates setup of a MySQL database (`ALX_prodev`) and a `user_data` table with a clear schema.
- **CSV Data Seeding**: Seeds the database from a `user_data.csv` file, ensuring idempotency and integrity.
- **Generator Patterns**: Implements streaming, batch, and paginated access to SQL data using Python generators for memory efficiency.
- **Batch Processing**: Processes user data in configurable batches for scalable workflows.
- **Lazy Pagination**: Simulates paginated access, loading each page only when needed.
- **Memory-Efficient Aggregation**: Computes aggregates (such as average age) without loading the full dataset into memory.
- **Extensible Design**: Functions are modular, type-annotated, and ready for extension with error handling, logging, and configuration.

---

## Learning Objectives

- Master Python generator functions for iterative, lazy data processing.
- Handle large datasets efficiently using batch processing, streaming, and lazy loading.
- Integrate Python with SQL databases for robust data management.
- Write clean, reusable, and maintainable backend code.
- Employ advanced patterns in Python systems architecture.

---

## Project Structure

```
python-generators-0x00/
│
├── seed.py               # Database setup and seeding logic
├── 0-main.py             # Entry point for initializing and testing seed functionality
├── 0-stream_users.py     # Generator for streaming users one by one from the database
├── 1-batch_processing.py # Batch processing using generators
├── 2-lazy_paginate.py    # Lazy loading pages of data using generators
├── 1-main.py             # Test harness for lazy pagination
├── 4-stream_ages.py      # Memory-efficient aggregation of user ages using generators
├── user_data.csv         # Sample data for seeding the database
└── README.md             # This documentation
```

---

## Usage

1. **Install Requirements**

   - Python 3.x
   - MySQL server (ensure it is running)
   - `mysql-connector-python` library

   ```bash
   pip install mysql-connector-python
   ```

2. **Configure Database Access**

   - By default, database connection uses:
     - host: `localhost`
     - user: `root`
     - password: `''` (empty)
   - Change these parameters in `seed.py` if your setup differs.

3. **Seed the Database**

   Run the main script to initialize the database and seed data:

   ```bash
   ./0-main.py
   ```

   **Expected Output:**
   ```
   connection successful
   Table user_data created successfully
   Database ALX_prodev is present 
   [(user_id, name, email, age), ...]
   ```

4. **Stream Users One-by-One**

   ```bash
   ./1-main.py
   ```

   Output: Prints the first few database rows as Python dicts (generator pattern).

5. **Batch Processing**

   ```bash
   ./2-main.py
   ```

   Output: Prints users over the age of 25 in batches (configurable batch size).

6. **Lazy Pagination**

   ```bash
   ./3-main.py
   ```

   Output: Prints users page by page, loading each page only when needed.

7. **Memory-Efficient Aggregation**

   ```bash
   ./4-stream_ages.py
   ```

   Output: Prints the average age of users, computed without loading all ages into memory.

---

## Key Functions

- `connect_db()`: Connects to MySQL server (no DB selected).
- `create_database(connection)`: Creates `ALX_prodev` database if absent.
- `connect_to_prodev()`: Connects to the `ALX_prodev` database.
- `create_table(connection)`: Creates `user_data` table if it doesn't exist.
- `insert_data(connection, csv_path)`: Seeds table from CSV, avoiding duplicates.
- `stream_users()`: Yields users one by one for streaming.
- `stream_users_in_batches(batch_size)`: Yields users in batches.
- `batch_processing(batch_size)`: Yields users over age 25 in batches.
- `lazy_pagination(page_size)`: Yields database users in lazy-loaded pages.
- `stream_user_ages()`: Yields user ages one by one.
- `average_user_age()`: Prints the average age using a generator for memory efficiency.

---

## Notes

- **Type Hints**: All functions are type-annotated for clarity.
- **Idempotency**: Seeding is safe to rerun; no duplicate users.
- **Extensibility**: Codebase is structured for easy extension—add logging, configuration, or error handling as needed.
- **Checker Compliance**: Some scripts include `return` at the end of generator functions to satisfy static checkers, though this is not required in idiomatic Python.

## License

This project is part of the ALX Backend Python curriculum.
