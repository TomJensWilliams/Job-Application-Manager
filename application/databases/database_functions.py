import os
import sys
if "/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager/application" in sys.path:
    sys.path[sys.path.index("/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager/application")] = "/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager"
import sqlite3
import json
import datetime
import shutil

# Databases

def create_database(database, /, *, print_statements=False):
    if os.path.isfile(f"./databases/{database}.db"):
        print("Attempted to create database which already exists.")
        return
    try:
        with sqlite3.connect(f"./databases/{database}.db"):
            if print_statements: print(f"{database} database opened successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def backup_database(database, /, *, backup_name=None, print_statements=False):
    if backup_name == None:
        backup_name = datetime.datetime.now()
    if os.path.isdir(f"../backup/{backup_name}.db"):
        raise BaseException("Attempting to create backup with a name that already exists.")
    os.mkdir(f"../backup/{backup_name}")
    shutil.copy(f"./databases/{database}.db", f"../backup/{backup_name}")
    if print_statements: print(f"{database} database backed up successfully in {backup_name}.")
    return backup_name

def restore_database(database, backup_name, /, *, print_statements=False):
    if os.path.isfile(f"./databases/{database}.db"):
        os.mkdir("../failsafe")
        shutil.copy(f"./databases/{database}.db", f"../failsafe")
        os.remove(f"./databases/{database}.db")
    try:
        shutil.copy(f"../backup/{backup_name}/{database}.db", "./databases")
        if print_statements: print(f"{database} database restored successfully from {backup_name}")
    except Exception:
        if os.path.isfile(f"./databases/{database}.db"):
            os.remove(f"./databases/{database}.db")
        if os.path.isdir("../failsafe"):
            shutil.copy(f"../failsafe/{database}.db", "./databases")
    finally:
        if os.path.isdir("../failsafe"):
            shutil.rmtree("../failsafe")

# Tables

def create_table(database, table, fields, datatypes, /, *, print_statements = False):
    statement = f"CREATE TABLE {table} (\n"
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
            if isinstance(values[index], str) or isinstance(values[index], int):
                pass
            else: 
                values[index] = json.dumps(values[index])
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
                current_list = []
                for element in row:
                    if isinstance(element, int):
                        current_list.append(element)
                    else:
                        try:
                            current_list.append(json.loads(element))
                        except json.decoder.JSONDecodeError as e:
                            current_list.append(element)
                output.append(current_list)
            if print_statements: print(f"Read records successfully.")
            return output
    except sqlite3.Error as e:
        print("Failed to read records:", e)

def update_records(database, table, update_fields, update_values, /, *, match_fields=None, match_values=None, print_statements=False):
    if update_values != None:
        for index in range(0, len(update_values)):
            if isinstance(update_values[index], str) or isinstance(update_values[index], int):
                pass
            else: 
                update_values[index] = json.dumps(update_values[index])
    if match_values != None:
        for index in range(0, len(match_values)):
            if isinstance(match_values[index], str) or isinstance(match_values[index], int):
                pass
            else: 
                match_values[index] = json.dumps(match_values[index])
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
                if print_statements: print(statement, tuple(update_values + match_values))
                cursor.execute(statement, tuple(update_values + match_values))
            conn.commit()
            if print_statements: print("Updated records successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to update records:", e)

def delete_records(database, table, /, *, fields=None, values=None, print_statements=False):
    if values != None:
        for index in range(0, len(values)):
            if isinstance(values[index], str) or isinstance(values[index], int):
                pass
            else: 
                values[index] = json.dumps(values[index])
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