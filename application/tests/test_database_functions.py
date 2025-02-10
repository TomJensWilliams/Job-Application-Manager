import os
import sys
from application.databases.database_functions import *

"""
    Assert 1: Tests to make sure test database does not already exist.
    Assert 2: Tests to see that test database has been corrected.
"""
def test_create_database():
    delete_file_if_found("./databases/pytest.db")
    #
    assert not file_exists("./databases/pytest.db")
    create_database("pytest")
    assert file_exists("./databases/pytest.db")
    #
    delete_file_if_found("./databases/pytest.db")

"""
    Assert 1: Test to make sure test database does not already exist.
    Assert 2: Test that new database has been set up with one record.
    Assert 3: Ensure that sqlite exceptions are caught as failed assertions.
    Assert 4: Test to see if backup directory and database file were created.
    Assert 5: Test to see that another backup directory was created.
    Assert 6: Test to see that backup was created with expected name.
    Assert 7: For each backup database, check to see contents are as expected.
    Assert 8: Ensure that sqlite exceptions are caught as failed assertions.
"""
def test_backup_database():
    delete_file_if_found("./databases/pytest.db")
    delete_file_if_found("../backup/pytest/pytest.db")
    delete_empty_directory_if_found("../backup/pytest")
    #
    assert not file_exists("../backup/pytest/pytest.db")
    try: 
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test(name TEXT, age INTEGER);")
            cursor.execute("INSERT INTO test(name,age) VALUES('Bill',42)")
            conn.commit()
            assert cursor.execute("SELECT * FROM test").fetchall() == [('Bill', 42)]
    except sqlite3.OperationalError as e:
        print("Unable to backup database:", e)
        assert 0 == 1
    chosen_backup_name = backup_database("pytest", backup_name="pytest")
    assert file_exists(f"../backup/{chosen_backup_name}/pytest.db")
    directory_count = count_directories("../backup")
    assigned_backup_name = backup_database("pytest")
    assert count_directories("../backup") == directory_count + 1
    assert file_exists(f"../backup/{assigned_backup_name}/pytest.db")
    backup_databases = [chosen_backup_name, assigned_backup_name]
    for database in backup_databases:
        try:
            with sqlite3.connect(f"../backup/{database}/pytest.db") as conn:
                cursor = conn.cursor()
                assert cursor.execute("SELECT * FROM test").fetchall() == [('Bill', 42)]
        except sqlite3.OperationalError as e:
            print("Unable to backup database:", e)
            assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")
    delete_file_if_found(f"../backup/{chosen_backup_name}/pytest.db")
    delete_empty_directory_if_found(f"../backup/{chosen_backup_name}")
    delete_file_if_found(f"../backup/{assigned_backup_name}/pytest.db")
    delete_empty_directory_if_found(f"../backup/{assigned_backup_name}")

"""
    Assert 1: Test to make sure test database does not exist
    Assert 2: Ensure that sqlite exceptions are caught as failed assertions.
    Assert 3: Test to make sure newly created database was
              deleted following it being backed up.
    Assert 4: Test to make sure test file exists after restore.
    Assert 5: Test to see that restored database's contents are as expected.
    Assert 6: Ensure that sqlite exceptions are caught as failed assertions.
"""
def test_restore_database():
    delete_file_if_found("./databases/pytest")
    #
    assert not file_exists("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test(name TEXT, age INTEGER);")
            cursor.execute("INSERT INTO test(name,age) VALUES('Dan',84)")
            conn.commit()
    except sqlite3.Error as e:
        print("Unable to restore database:", e)
        assert 0 == 1
    backup_name = backup_database("pytest")
    delete_file_if_found("./databases/pytest.db")
    assert not file_exists("./databases/pytest.db")
    restore_database("pytest", backup_name)
    assert file_exists("./databases/pytest.db")
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            assert cursor.execute("SELECT * FROM test").fetchall() == [('Dan', 84)]
    except sqlite3.Error as e:
        print("Unable to restore database:", e)
        assert 0 == 1


def test_create_table():
    delete_file_if_found("./databases/pytest.db")
    #
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
        assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")

def test_read_fields():
    delete_file_if_found("./databases/pytest.db")
    #
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test(name TEXT, age INTEGER);")
            assert read_fields("pytest", "test") == ["name", "age"]
            cursor.execute("ALTER TABLE test ADD sex TEXT")
            assert read_fields("pytest", "test", rowid=True) == ["rowid", "name", "age", "sex"]
    except sqlite3.OperationalError as e:
        print("Unable to read fields:", e)
        assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")

def test_read_fields_datatypes():
    delete_file_if_found("./databases/pytest.db")
    #
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test(name TEXT, age INTEGER);")
            assert read_fields_datatypes("pytest", "test") == ["TEXT", "INTEGER"]
            cursor.execute("ALTER TABLE test ADD sex TEXT")
            assert read_fields_datatypes("pytest", "test") == ["TEXT", "INTEGER", "TEXT"]
    except sqlite3.OperationalError as e:
        print("Unable to read fields datatypes:", e)
        assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")

def test_create_record():
    delete_file_if_found("./databases/pytest.db")
    #
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test(name TEXT, age INTEGER, parents TEXT);")
            assert cursor.execute("SELECT * FROM test").fetchall() == []
            create_record("pytest", "test", ["age", "name", "parents"], [42, 'Bill', {"mother": "Jan", "father": "Jake"}])
            assert cursor.execute("SELECT * FROM test").fetchall() == [('Bill', 42, '{"mother": "Jan", "father": "Jake"}')]
    except sqlite3.OperationalError as e:
        print("Unable to create record:", e)
        assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")

def test_read_record():
    delete_file_if_found("./databases/pytest.db")
    #
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test(name TEXT, age INTEGER, parents TEXT);")
            assert read_records("pytest", "test") == []
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Bill",44, \'{"mother": "Jan", "father": "Jake"}\')')
            conn.commit()
            assert read_records("pytest", "test", rowid=True) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}]]
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Dan",82, \'{"mother": "Jan", "father": "Jake"}\')')
            conn.commit()
            assert read_records("pytest", "test", selections=["name"]) == [["Bill"], ["Dan"]]
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Jill",44, \'{"mother": "Jenifer", "father": "Hunter"}\')')
            conn.commit()
            assert read_records("pytest", "test", rowid=True, fields=["age"], values=[44]) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}], [3, "Jill", 44, {"mother": "Jenifer", "father": "Hunter"}]]
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Dan",63, \'{"mother": "Vivian", "father": "Todd"}\')')
            conn.commit()
            assert read_records("pytest", "test", rowid=True, selections=["age"], fields=["name"], values=["Dan"]) == [[2, 82], [4, 63]]
            assert read_records("pytest", "test", rowid=True, selections=["name"], fields=["parents"], values=[{"mother": "Jan", "father": "Jake"}]) == [[1, "Bill"], [2, "Dan"]]
            assert read_records("pytest", "test", rowid=True, selections=None, fields=["rowid"], values=[2]) == [[2, "Dan", 82, {"mother": "Jan", "father": "Jake"}]]
    except sqlite3.OperationalError as e:
        print("Unable to read records:", e)
        assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")

def test_update_record():
    delete_file_if_found("./databases/pytest.db")
    #
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test(name TEXT, age INTEGER, parents TEXT);")
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Bill",44, \'{"mother": "Jan", "father": "Jake"}\')')
            conn.commit()
            assert read_records("pytest", "test", rowid=True) == [[1, "Bill", 44, {"mother": "Jan", "father": "Jake"}]]
            update_records("pytest", "test", ["name", "age"], ["Aaron", 28], match_fields=["name", "age"], match_values=["Bill", 44])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Jan", "father": "Jake"}]]
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Jan",53, \'{"mother": "Vivian", "father": "Dan"}\')')
            conn.commit()
            update_records("pytest", "test", ["parents"], [{"mother": "Samantha", "father": "Saul"}])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Samantha", "father": "Saul"}], ["Jan", 53, {"mother": "Samantha", "father": "Saul"}]]
            update_records("pytest", "test", ["parents"], [{"mother": "Samantha", "father": "Paul"}], match_fields=["parents"], match_values=[{"mother": "Samantha", "father": "Saul"}])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Samantha", "father": "Paul"}], ["Jan", 53, {"mother": "Samantha", "father": "Paul"}]]
            update_records("pytest", "test", ["age"], [54], match_fields=["rowid"], match_values=[2])
            assert read_records("pytest", "test") == [["Aaron", 28, {"mother": "Samantha", "father": "Paul"}], ["Jan", 54, {"mother": "Samantha", "father": "Paul"}]]
    except sqlite3.OperationalError as e:
        print("Unable to update record:", e)
        assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")

def test_delete_record():
    delete_file_if_found("./databases/pytest.db")
    #
    try:
        with sqlite3.connect("./databases/pytest.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS test(name TEXT, age INTEGER, parents TEXT);")
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Bill",44,\'{"mother": "Jan", "father": "Jake"}\')')
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Dan",82,\'{"mother": "Jan", "father": "Jake"}\')')
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Jill",44,\'{"mother": "Jenifer", "father": "Hunter"}\')')
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Dan",63,\'{"mother": "Vivian", "father": "Todd"}\')')
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Trish",36,\'{"mother": "Margaret", "father": "Jim"}\')')
            cursor.execute('INSERT INTO test(name,age,parents) VALUES("Taylor",39,\'{"mother": "Margaret", "father": "Jim"}\')')
            conn.commit()
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
        assert 0 == 1
    #
    delete_file_if_found("./databases/pytest.db")

#################
# Testing Tools #
#################

def file_exists(file):
    return os.path.isfile(file)

def directory_exists(directory):
    return os.path.isdir(directory)

def directory_is_empty(directory):
    return not any(os.scandir(directory))

def delete_file_if_found(file):
    if file_exists(file):
        os.remove(file)

def delete_empty_directory_if_found(directory):
    if directory_exists(directory) and directory_is_empty(directory):
        os.rmdir(directory)

def count_files(directory):
    count = 0
    for entry in os.scandir(directory):
        if entry.is_file():
            count += 1
    return count

def count_directories(directory):
    count = 0
    for entry in os.scandir(directory):
        if entry.is_dir():
            count += 1
    return count