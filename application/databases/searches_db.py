import sqlite3

def create_database():
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            print(f"Opened SQLite database searches with version {sqlite3.sqlite_version} successfully.\n")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def create_table(table, fields, datatypes):
    statement = f"CREATE TABLE IF NOT EXISTS {table}(\n"
    for index in range(0, len(fields)):
        statement += f"\t{fields[index]} {datatypes[index]}{',' if index != len(fields) - 1 else ''}\n"
    statement += ");"
    print(statement)
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
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
            statment += f"\t{fields_list[outer_index][index]} {datatypes_list[outer_index][index]}{',' if index != len(fields_list[outer_index]) - 1 else ''}\n"
        statement += ");"
        print(statement)
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(statement)
                conn.commit()
                print(f"{table_list[outer_index]} table create successfully.\n")
        except sqlite3.OperationalError as e:
            print("Failed to create table:", e)

def read_fields(table):
    output = []
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE 1 = 0;")
            for element in cursor.description:
                output.append(element[0])
    except sqlite3.Error as e:
        print("Failed to read fields:", e)
    return output

def create_search(table, fields,  values):
    statement = f"INSERT INTO {table}("
    for index in range(0, len(fields)):
        statement += f"{',' if index != 0 else ''}{fields[index]}"
    statement += ") VALUES("
    for index in range(0, len(values)):
        statement += f"{',' if index != 0 else ''}{values[index]}"
    statement += ");"
    print(statement)
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
            print(f"Search with id {cursor.lastrowid} created in {table} successfully.")
            return cursor.lastrowid
    except sqlite3.Error as e:
        print("Failed to create search:", e)

def create_searches(table, fields_list, values_list):
    output = []
    for outer_index in range(0, len(fields_list)):
        statement = f"INSERT INTO {table}("
        for index in range(0, len(fields_list[outer_index])):
            statement += f"{',' if index != 0 else ''}{fields_list[outer_index][index]}"
        statement += ") VALUES("
        for index in range(0, len(values_list[outer_index])):
            statement += f"{',' if index != 0 else ''}{values_list[outer_index][index]}"
        statement += ");"
        print(statement)
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(statement)
                conn.commit()
                print(f"Search with id {cursor.lastrowid} created in {table} successfully.")
                output.append(cursor.lastrowid)
        except sqlite3.Error as e:
            print("Failed to create search:", e)
    return output

def read_search(table, id):
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE id = {id};")
            row = cursor.fetchone()
            return row
    except sqlite3.OperationalError as e:
        print("Failed to read search:", e)

def read_search_field(table, field, value):
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE {field} = {value};")
            row = cursor.fetchone()
            return row
    except sqlite3.OperationalError as e:
        print("Failed to read search:", e)

def read_searches(table, id_list):
    output = []
    for id in id_list:
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE id = {id};")
                row = cursor.fetchone()
                output.append(row)
        except sqlite3.OperationalError as e:
            print("Failed to read search:", e)
    return output

def read_searches_field(table, field, value_list):
    output = []
    for value in value_list:
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE {field} = {value};")
                row = cursor.fetchone()
                output.append(row)
        except sqlite3.OperationalError as e:
            print("Failed to read search:", e)
    return output

def read_all_searches(table):
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        print("Failed to read all searches:", e)

def update_search(table, id, fields, values):
    statement = f"UPDATE {table} SET"
    for index in range(0, len(fields)):
        statement += f"{',' if index != 0 else ''} {fields[index]} = {values[index]}"
    statement += f"WHERE id = {id};"
    print(statement)
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to update search:", e)

def update_search_field(table, search_field, search_value, fields, values):
    statement = f"UPDATE {table} SET"
    for index in range(0, len(fields)):
        statement += f"{',' if index != 0 else ''} {fields[index]} = {values[index]}"
    statement += f"WHERE {search_field} = {search_value}"
    print(statement)
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to update search:", e)

def update_searches(table, id_list, fields_list, values_list):
    for outer_index in range(0, id_list):
        statement = f"UPDATE {table} SET"
        for index in range(0, len(fields_list[outer_index])):
            statement += f"{',' if index != 0 else ''} {fields_list[outer_index][index]} = {values_list[outer_index][index]}"
        statement += f"WHERE id = {id_list[outer_index]};"
        print(statement)
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(statement)
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Failed to update search:", e)

def update_searches_field(table, search_field_list, search_value_list, fields_list, values_list):
    for outer_index in range(0, search_field_list):
        statement = f"UPDATE {table} SET"
        for index in range(0, len(fields_list[outer_index])):
            statement += f"{',' if index != 0 else ''} {fields_list[outer_index][index]} = {values_list[outer_index][index]}"
        statement += f"WHERE {search_field_list[outer_index]} = {search_value_list[outer_index]}"
        print(statement)
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(statement)
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Failed to update search:", e)

# def update_all_searches(table, ): I don't think this needs to exits, unless there were differnt update values for each entry, which is what update_searches is for

def delete_search(table, id):
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id = {id};")
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to delete search:", e)

def delete_search_parameters(table, field, value):
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE {field} = {value};")
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to delete search:", e)

def delete_searches(table, id_list):
    for id in id_list:
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table} WHERE id = {id};")
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Failed to delete search:", e)

def delete_searches_parameters(table, field_list, value_list):
    for index in range(0, len(field_list)):
        try:
            with sqlite3.connect("./databases/searches.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table} WHERE {field_list[index]} = {value_list[index]};")
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Failed to delete search:", e)

def delete_all_searches(table):
    try:
        with sqlite3.connect("./databases/searches.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table};")
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to delete search:", e)