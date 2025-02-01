import sqlite3

# Databases

def create_database(database, print_statements=False):
    try:
        with sqlite3.connect(f"./databases/{database}.db"):
            if print_statements: print(f"{database} database opened successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

# Tables

def create_table(database, table, fields, datatypes, print_statements = False):
    statement = f"CREATE TABLE IF NOT EXISTS {table} (\n"
    for index in range(0, len(fields)):
        statement += f"\t{fields[index]} {datatypes[index]}{',' if index != len(fields) - 1 else ''}\n"
    statement += ");"
    try:
        with sqlite3.connect(f"./databases/{database}.db")as conn:
            cursor = conn.cursor()
            if print_statements: print(statement)
            cursor.execute(statement)
            conn.commit()
            if print_statements: print(f"{table} table created successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to create table:", e)

# Records

def create_record(database, table, fields, values, print_statement=False):
    statement = f""

    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statement: print(statement)
            cursor.execute(statement)
            conn.commit()
            if print_statement: print(f"Created record successfully.")
    except sqlite3.Error as e:
        print("Failed to create record:", e)

def read_records(database, table, fields, values, print_statement=False):
    statement = f"SELECT * FROM {table} WHERE"
    for index in range(0, len(fields)):
        statement += f"{' AND ' if index != 0 else ' '}{fields[index]} = {values[index]}"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statement: print(statement)
            cursor.execute(statement)
            rows = cursor.fetchall()
            if print_statement: print(f"Read records successfully.")
            return rows
    except sqlite3.Error as e:
        print("Failed to read records:", e)

def read_all_records(database, table, print_statements=False):
    statement = f"SELECT * FROM {table}"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statements: print(statement)
            cursor.execute(statement)
            rows = cursor.fetchall()
            if print_statements: print(f"Read all records successfully.")
            return rows
    except sqlite3.Error as e:
        print("Failed to read all records:", e)

def update_records():
    pass

def update_all_records():
    pass

def delete_records(database, table, fields, values, print_statements=False):
    statement = f"DELETE FROM {table} WHERE"
    for index in range(0, len(fields)):
        statement += f"{' AND ' if index != 0 else ' '}{fields[index]} = {values[index]}"
    statement += ";"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statements: print(statement)
            cursor.execute(statement)
            conn.commit()
            if print_statements: print(f"Deleted records successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to delete record:", e)

def delete_all_records(database, table, print_statements=False):
    statement = f"DELETE FROM {table};"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statements: print(statement)
            cursor.execute(statement)
            conn.commit()
            if print_statements: print(f"Deleted all records successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to delete records:", e)