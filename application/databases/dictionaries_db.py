import sqlite3

def create_database():
    try:
        with sqlite3.connect("./databases/dictionaries.db") as conn:
            print(f"Opened SQLite database dictionaries with version {sqlite3.sqlite_version} successfully.\n")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def create_table(table, fields, datatypes):
    statement = f"CREATE TABLE IF NOT EXISTS {table}(\n"
    for index in range(0, len(fields)):
        statement += f"\t{fields[index]} {datatypes[index]}{' PRIMARY KEY' if index == 0 else ''}{',' if index != len(fields) - 1 else ''}\n"
    statement += ");"
    print(statement)
    try:
        with sqlite3.connect("./databases/dictionaries.db") as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
            print(f"{table} table create successfully.\n")
    except sqlite3.OperationalError as e:
        print("Failed to create table:", e)

def create_tables(table_list, fields_list, datatypes_list):
    for outer_index in range(0, len(table_list)):
        statement = f"CREATE TABLE IF NOT EXISTS {table_list[outer_index]}(\n"
        for index in range(0, len(fields_list[outer_index])):
            statment += f"\t{fields_list[outer_index][index]} {datatypes_list[outer_index][index]}{' PRIMARY KEY' if index == 0 else ''}{',' if index != len(fields_list[outer_index]) - 1 else ''}\n"
        statement += ");"
        print(statement)
        try:
            with sqlite3.connect("./databases/dictionaries.db") as conn:
                cursor = conn.cursor()
                cursor.execute(statement)
                conn.commit()
                print(f"{table_list[outer_index]} table create successfully.\n")
        except sqlite3.OperationalError as e:
            print("Failed to create table:", e)

def read_fields(table):
    output = []
    try:
        with sqlite3.connect("./databases/dictionaries.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE 1 = 0;")
            for element in cursor.description:
                output.append(element[0])
    except sqlite3.Error as e:
        print("Failed to read fields:", e)
    return output

def create_dictionary(table, values):
    statement = f"INSERT INTO {table}("
    for index in range(0, len(values)):
        statement = f"{',' if index != 0 else ''}{values[index]}"
    statement += ");"
    print(statement)
    try:
        with sqlite3.connect("./databases/dictionaries.db") as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
            print(f"Search with id {cursor.lastrowid} created in {table} successfully.")
            return cursor.lastrowid
    except sqlite3.Error as e:
        print("Failed to create search:", e)

def create_dictionaries(table, values_list):
    output = []
    for values in values_list:
        statement = f"INSERT INTO {table}("
        for index in range(0, len(values)):
            statement = f"{',' if index != 0 else ''}{values[index]}"
        statement += ");"
        print(statement)
        try:
            with sqlite3.connect("./databases/dictionaries.db") as conn:
                cursor = conn.cursor()
                cursor.execute(statement)
                conn.commit()
                print(f"Search with id {cursor.lastrowid} created in {table} successfully.")
                output.append(cursor.lastrowid)
        except sqlite3.Error as e:
            print("Failed to create search:", e)
    return output

def read_dictionary(table, id):
    try:
        with sqlite3.connect("./databases/dictionaries.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE id = {id};")
            row = cursor.fetchone()
            return row
    except sqlite3.OperationalError as e:
        print("Failed to read search:", e)

def read_dictionary_field(table, field, value):
    try:
        with sqlite3.connect("./databases/dictionaries.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE {field} = {value};")
            row = cursor.fetchone()
            return row
    except sqlite3.OperationalError as e:
        print("Failed to read search:", e)

def read_dictionaries(table, id_list):
    output = []
    for id in id_list:
        try:
            with sqlite3.connect("./databases/dictionaries.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE id = {id};")
                row = cursor.fetchone()
                output.append(row)
        except sqlite3.OperationalError as e:
            print("Failed to read search:", e)
    return output

def read_dictionaries_field(table, field, value_list):
    output = []
    for value in value_list:
        try:
            with sqlite3.connect("./databases/dictionaries.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE {field} = {value};")
                row = cursor.fetchone()
                output.append(row)
        except sqlite3.OperationalError as e:
            print("Failed to read search:", e)
    return output

def read_all_dictionaries(table):
    try:
        with sqlite3.connect("./databases/dictionaries.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        print("Failed to read all searches:", e)