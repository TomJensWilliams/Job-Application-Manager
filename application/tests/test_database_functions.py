import os
import sys
print(sys.path)
from application.databases.database_functions import *

"""
Hierarchy of Test Interdependancy:
- test_create_database
- create_table
    - test_read_fields
    - test_read_fields_datatypes
    - test_create_record
        - test_read_records
            - test_update_records
"""

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
        print("Unable to read fields:", e)
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
        print("Unable to read fields datatypes:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_create_record():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            create_table("pytest", "test", ["name", "age", "parents"], ["TEXT", "INTEGER", "TEXT"])
            assert cursor.execute("SELECT * FROM test").fetchall() == []
            create_record("pytest", "test", ["age", "name", "parents"], [42, 'Bill', {"mother": "Jan", "father": "Jake"}])
            assert cursor.execute("SELECT * FROM test").fetchall() == [('Bill', 42, '{"mother": "Jan", "father": "Jake"}')]
    except sqlite3.OperationalError as e:
        print("Unable to create record:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_read_record():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            create_table("pytest", "test", ["name", "age", "parents"], ["TEXT", "INTEGER", "TEXT"])
            assert read_records("pytest", "test") == []
            create_record("pytest", "test", ["name", "age", "parents"], ["Bill", 44, {"mother": "Jan", "father": "Jake"}])
            assert read_records("pytest", "test", rowid=True) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}]]
            create_record("pytest", "test", ["name", "age", "parents"], ["Dan", 82, {"mother": "Jan", "father": "Jake"}])
            assert read_records("pytest", "test", selections=["name"]) == [["Bill"], ["Dan"]]
            create_record("pytest", "test", ["name", "age", "parents"], ["Jill", 44, {"mother": "Jenifer", "father": "Hunter"}])
            assert read_records("pytest", "test", rowid=True, fields=["age"], values=[44]) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}], [3, "Jill", 44, {"mother": "Jenifer", "father": "Hunter"}]]
            create_record("pytest", "test", ["name", "age", "parents"], ["Dan", 63, {"mother": "Vivian", "father": "Todd"}])
            assert read_records("pytest", "test", rowid=True, selections=["age"], fields=["name"], values=["Dan"]) == [[2, 82], [4, 63]]
            assert read_records("pytest", "test", rowid=True, selections=["name"], fields=["parents"], values=[{"mother": "Jan", "father": "Jake"}]) == [[1, "Bill"], [2, "Dan"]]
            assert read_records("pytest", "test", rowid=True, selections=None, fields=["rowid"], values=[2]) == [[2, "Dan", 82, {"mother": "Jan", "father": "Jake"}]]
    except sqlite3.OperationalError as e:
        print("Unable to read records:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_update_record():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            create_table("pytest", "test", ["name", "age", "parents"], ["TEXT", "INTEGER", "TEXT"])
            create_record("pytest", "test", ["name", "age", "parents"], ["Bill", 44, {"mother": "Jan", "father": "Jake"}])
            assert read_records("pytest", "test", rowid=True) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}]]
            update_records("pytest", "test", ["name", "age"], ["Aaron", 28], match_fields=["name", "age"], match_values=["Bill", 44])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Jan", "father": "Jake"}]]
            create_record("pytest", "test", ["name", "age", "parents"], ["Jan", 53, {"mother": "Vivian", "father": "Dan"}])
            update_records("pytest", "test", ["parents"], [{"mother": "Samantha", "father": "Saul"}])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Samantha", "father": "Saul"}], ["Jan", 53, {"mother": "Samantha", "father": "Saul"}]]
            update_records("pytest", "test", ["parents"], [{"mother": "Samantha", "father": "Paul"}], match_fields=["parents"], match_values=[{"mother": "Samantha", "father": "Saul"}])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Samantha", "father": "Paul"}], ["Jan", 53, {"mother": "Samantha", "father": "Paul"}]]
            update_records("pytest", "test", ["age"], [54], match_fields=["rowid"], match_values=[2])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Samantha", "father": "Paul"}], ["Jan", 54, {"mother": "Samantha", "father": "Paul"}]]
    except sqlite3.OperationalError as e:
        print("Unable to update record:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")

def test_delete_record():
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            create_table("pytest", "test", ["name", "age", "parents"], ["TEXT", "INTEGER", "TEXT"])
            create_record("pytest", "test", ["name", "age", "parents"], ["Bill", 44, {"mother": "Jan", "father": "Jake"}])
            create_record("pytest", "test", ["name", "age", "parents"], ["Dan", 82, {"mother": "Jan", "father": "Jake"}])
            create_record("pytest", "test", ["name", "age", "parents"], ["Jill", 44, {"mother": "Jenifer", "father": "Hunter"}])
            create_record("pytest", "test", ["name", "age", "parents"], ["Dan", 63, {"mother": "Vivian", "father": "Todd"}])
            create_record("pytest", "test", ["name", "age", "parents"], ["Trish", 36, {"mother": "Margaret", "father": "Jim"}])
            create_record("pytest", "test", ["name", "age", "parents"], ["Taylor", 39, {"mother": "Margaret", "father": "Jim"}])
            assert read_records("pytest", "test", rowid=True) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}], [2, "Dan", 82, {"mother": "Jan", "father": "Jake"}], [3, "Jill", 44, {"mother": "Jenifer", "father": "Hunter"}], [4, "Dan", 63, {"mother": "Vivian", "father": "Todd"}], [5, "Trish", 36, {"mother": "Margaret", "father": "Jim"}], [6, "Taylor", 39, {"mother": "Margaret", "father": "Jim"}]]
            delete_records("pytest", "test", fields=["name"], values=["Jill"])
            assert read_records("pytest", "test", rowid=True) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}], [2, "Dan", 82, {"mother": "Jan", "father": "Jake"}], [4, "Dan", 63, {"mother": "Vivian", "father": "Todd"}], [5, "Trish", 36, {"mother": "Margaret", "father": "Jim"}], [6, "Taylor", 39, {"mother": "Margaret", "father": "Jim"}]]
            delete_records("pytest", "test", fields=["parents"], values=[{"mother": "Jan", "father": "Jake"}])
            assert read_records("pytest", "test", rowid=True) == [[4, "Dan", 63, {"mother": "Vivian", "father": "Todd"}], [5, "Trish", 36, {"mother": "Margaret", "father": "Jim"}], [6, "Taylor", 39, {"mother": "Margaret", "father": "Jim"}]]
            delete_records("pytest", "test", fields=["rowid"], values=[5])
            assert read_records("pytest", "test", rowid=True) == [[4, "Dan", 63, {"mother": "Vivian", "father": "Todd"}], [6, "Taylor", 39, {"mother": "Margaret", "father": "Jim"}]]
            delete_records("pytest", "test")
            assert read_records("pytest", "test", rowid=True) == []
    except sqlite3.OperationalError as e:
        print("Unable to read records:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")