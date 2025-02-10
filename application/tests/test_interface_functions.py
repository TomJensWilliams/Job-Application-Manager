import os
import sqlite3
from application.interface_functions import *

"""

def test_create_database():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")   
    create_database("pytest")
    assert os.path.exists("./databases/pytest.db")
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_backup_databases():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    if os.path.exists("../backup/pytest/pytest.db"):
        os.remove("../backup/pytest/pytest.db")
        os.rmdir("../backup/pytest")
    create_database("pytest")
    create_table("pytest", "test", ["message"], ["TEXT"])
    create_record("pytest", "test", ["message"], ["this worked"])
    backup_directory_name = backup_databases(database_filenames=["pytest.db"], backup_directory_name="pytest")
    try:
        with sqlite3.connect(f"../backup/{backup_directory_name}/pytest.db") as conn:
            cursor = conn.cursor()
            assert cursor.execute("SELECT * FROM test").fetchall() == [('this worked',)]
    except sqlite3.Error as e:
        print("Unable to backup database:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")   
    if os.path.exists("../backup/pytest/pytest.db"):
        os.remove("../backup/pytest/pytest.db")
        os.rmdir("../backup/pytest")

def test_create_table():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            assert cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test';").fetchall() == []
            create_table("pytest", "test", ["name", "age"], ["TEXT", "INTEGER"])
            assert cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test';").fetchall() == [('test',)]
            assert [description[0] for description in cursor.execute("SELECT rowid, * FROM test LIMIT 0").description] == ["rowid", "name", "age"]
            assert [detail[2] for detail in cursor.execute("PRAGMA table_info(test)").fetchall()] == ['TEXT', 'INTEGER']
    except sqlite3.OperationalError as e:
        print("Unable to create table:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_read_fields():
    pass

def test_read_fields_datatypes():
    pass

def test_create_record():
    pass

def test_read_record():
    pass

def test_update_record():
    pass

def test_delete_record():
    pass

def test_print_table():
    pass

def test_run_search():
    pass

def test_prepare_search():
    pass

def test_create_and_update_dictionaries():
    pass

# """