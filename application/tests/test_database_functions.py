import os
from application.databases.database_functions import *

def test_create_database():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    create_database("pytest")
    assert os.path.exists("./databases/pytest.db")
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_create_table():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test';")
            assert cursor.fetchall() == []
            create_table("pytest", "test", ["name", "age"], ["TEXT", "INTEGER"])
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test';")
            assert cursor.fetchall() == [('test',)]
            cursor.execute("SELECT rowid, * FROM test LIMIT 0")
            assert [description[0] for description in cursor.description] == ["rowid", "name", "age"]
            cursor.execute("PRAGMA table_info(test)")
            assert [detail[2] for detail in cursor.fetchall()] == ['TEXT', 'INTEGER']
    except sqlite3.OperationalError as e:
        print("Unable to create table:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_read_fields():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            create_table("pytest", "test", ["name", "age"], ["TEXT", "INTEGER"])
            assert read_fields("pytest", "test") == ["name", "age"]
            cursor.execute("ALTER TABLE test ADD sex TEXT")
            assert read_fields("pytest", "test", rowid=True) == ["rowid", "name", "age", "sex"]
    except sqlite3.OperationalError as e:
        print("Unable to read record:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_read_fields_datatypes():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            create_table("pytest", "test", ["name", "age"], ["TEXT", "INTEGER"])
            assert read_fields_datatypes("pytest", "test") == ["TEXT", "INTEGER"]
            cursor.execute("ALTER TABLE test ADD sex TEXT")
            assert read_fields_datatypes("pytest", "test") == ["TEXT", "INTEGER", "TEXT"]
    except sqlite3.OperationalError as e:
        print("Unable to read record:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_create_record():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            create_table("pytest", "test", ["name", "age"], ["TEXT", "INTEGER"])
            cursor.execute("SELECT * FROM test")
            rows = cursor.fetchall()
            assert rows == []
            create_record("pytest", "test", ["age", "name"], [42, 'Bill'])
            cursor.execute("SELECT * FROM test")
            rows = cursor.fetchall()
            assert rows == [('Bill', 42)]
    except sqlite3.OperationalError as e:
        print("Unable to read record:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_read_record():
    pass

def test_update_record():
    pass

def test_delete_record():
    pass