import sqlite3
import json

# Databases

def create_database(database, /, *, print_statements=False):
    try:
        with sqlite3.connect(f"./databases/{database}.db"):
            if print_statements: print(f"{database} database opened successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

# Tables

def create_table(database, table, fields, datatypes, /, *, print_statements = False):
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

# Fields

def read_fields(database, table, /, *, rowid=False, print_statements=False):
    statement = f"SELECT {'rowid, ' if rowid else ''}* FROM {table} LIMIT 0;"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statements: print(statement)
            cursor.execute(statement)
            field_names = [description[0] for description in cursor.description]
            if print_statements: print(f"fields read from {table} successfully.")
            return field_names
    except sqlite3.Error as e:
        print("Failed to read fields:", e)

def read_fields_datatypes(database, table, /, *, print_statements=False):
    statement = f"PRAGMA table_info({table})"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statements: print(statement)
            cursor.execute(statement)
            datatypes = [detail[2] for detail in cursor.fetchall()]
            if print_statements: print(f"datatypes read from {table} sucessfully")
            return datatypes
    except sqlite3.Error as e:
        print("Failed to read field datatypes:", e)

# Records

def create_record(database, table, fields, values, /, *, print_statements=False):
    for index in range(0, len(values)):
        if isinstance(values[index], str) or isinstance(values[index], int):
            pass
        else: 
            values[index] = json.dumps(values[index])
    statement = f"INSERT INTO {table} ("
    for index in range(0, len(fields)):
        statement += f"{',' if index != 0 else ''}{fields[index]}"
    statement += f") VALUES("
    for index in range(0, len(values)):
        statement += f"{',' if index != 0 else ''}?"
    statement += f");"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if print_statements: print(statement, tuple(values))
            cursor.execute(statement, tuple(values))
            conn.commit()
            if print_statements: print(f"Created record successfully.")
    except sqlite3.Error as e:
        print("Failed to create record:", e)

def read_records(database, table, /, *, rowid=False, selections=None, fields=None, values=None, print_statements=False):
    if values != None:
        for index in range(0, len(values)):
            try:
                values[index] = json.dumps(values[index])
            except TypeError as e:
                print("Type Error in read_records:", e)
                values[index] = None
    statement = f"SELECT {'rowid' if rowid else ''}"
    if selections == None:
        statement += f"{', ' if rowid else ''}*"
    else:
        for index in range(0, len(selections)):
            statement += f"{', ' if index != 0 or rowid else ''}{selections[index]}"
    statement += f" FROM {table}"
    if fields == None:
        pass
    else:
        statement += f" WHERE"
        for index in range(0, len(fields)):
            statement += f"{' AND ' if index != 0 else ' '}{fields[index]} = ?"
    statement += f";"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if values == None:
                if print_statements: print(statement)
                cursor.execute(statement)
            else:
                if print_statements: print(statement, tuple(values))
                cursor.execute(statement, tuple(values))
            rows = cursor.fetchall()
            output = []
            for row in rows:
                current_array = []
                for element in row:
                    if not isinstance(element, int):
                        current_array.append(json.loads(element))
                    else:
                        current_array.append(element)
            if print_statements: print(f"Read records successfully.")
            return rows
    except sqlite3.Error as e:
        print("Failed to read records:", e)

def update_records(database, table, update_fields, update_values, /, *, match_fields, match_values, print_statements=False):
    if print_statements: print(read_records(database, table))
    if update_values != None:
        for index in range(0, len(update_values)):
            try:
                update_values[index] = json.dumps(update_values[index])
            except TypeError as e:
                print("Type Error in update_records:", e)
    if match_values != None:
        for index in range(0, len(match_values)):
            try:
                match_values[index] = json.dumps(match_values[index])
            except TypeError as e:
                print("Type Error in update_records:", e)
    statement = f"UPDATE {table} SET"
    for index in range(0, len(update_fields)):
        statement += f"{',' if index != 0 else ''} {update_fields[index]} = ?"
    if match_fields == None:
        pass
    else:
        statement += f" WHERE"
        for index in range(0, len(match_fields)):
            statement += f"{' AND ' if index != 0 else ''} {match_fields[index]} = ?"
        statement += f";"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if match_values == None:
                if print_statements: print(statement, tuple(update_values))
                cursor.execute(statement, tuple(update_values))
            else:
                if print_statements: print(update_values, match_values)
                if print_statements: print(statement, tuple(update_values + match_values))
                cursor.execute(statement, tuple(update_values + match_values))
            conn.commit()
            if print_statements: print("Updated records successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to update records:", e)

def delete_records(database, table, fields=None, values=None, print_statements=False):
    if values != None:
        for index in range(0, len(values)):
            try:
                values[index] = json.dumps(values[index])
            except TypeError as e:
                print("Type Error in read_records:", e)
                values[index] = None
    statement = f"DELETE FROM {table}"
    if fields == None:
        pass
    else:
        statement += f" WHERE"
        for index in range(0, len(fields)):
            statement += f"{' AND ' if index != 0 else ' '}{fields[index]} = ?"
    statement += ";"
    try:
        with sqlite3.connect(f"./databases/{database}.db") as conn:
            cursor = conn.cursor()
            if values == None:
                if print_statements: print(statement)
                cursor.execute(statement)
            else: 
                if print_statements: print(statement, tuple(values))
                cursor.execute(statement, tuple(values))
            conn.commit()
            if print_statements: print(f"Deleted records successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to delete record:", e)