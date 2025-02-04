import os
import sqlite3
import json
from cli import *

def test_coditional_remove():
    assert [1, 2, 3] == conditional_remove([1, 2, 3, 4], [4])
    assert [1, 2, 3] == conditional_remove([1, 2, 3, 4, 5], [4, 5])
    assert [1, 2, 3] == conditional_remove([1, 2, 3], [4])
    assert ["1", "2", "3"] == conditional_remove(["1", "2", "3", "4"], ["4"])

def test_conditional_append():
    assert [1, 2, 3] == conditional_append([1, 2], [3])
    assert [1, 2, 3] == conditional_append([1], [2, 3])
    assert [1, 2, 3] == conditional_append([1, 2, 3], [2, 3])
    assert ["1", "2", "3"] == conditional_append(["1", "2"], ["3"])

def test_append_if_true():
    assert [1, 2, 3] == append_if_true([1, 2], [3], True)
    assert [1, 2, 3] == append_if_true([1], [2, 3], True)
    assert [1, 2, 3] == append_if_true([1, 2, 3], [4], False)
    assert ["1", "2", "3"] == append_if_true(["1", "2"], ["3"], True)

def test_choose_from_options(monkeypatch):
    inputs = ["One", "option", "Two", "exit", "choices", "Three", "choices", "quit", "One"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    assert "One" == choose_from_options("Testing choose_from_options", ["One", "Two", "Three", "Four"])
    assert "Two" == choose_from_options("Testing choose_from_options", ["One", "Two", "Three", "Four"])
    assert "exit" == choose_from_options("Testing choose_from_options", ["One", "Two", "Three", "Four"])
    assert "Three" == choose_from_options("Testing choose_from_options", ["One", "Two", "Three", "Four"], option_choice="choices")
    assert "quit" == choose_from_options("Testing choose_from_options", ["One", "Two", "Three", "Four"], option_choice="choices", exit_choice="quit")
    assert "Four" != choose_from_options("Testing choose_from_options", ["One", "Two", "Three", "Four"], option_choice="choices", exit_choice="quit")

def test_choose_multiple_from_options(monkeypatch):
    inputs = ["One", "exit", "Two", "One", "exit", "exit", "options", "Four", "exit", "choices", "One", "Two", "exit", "quit"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    assert ["One"] == choose_multiple_from_options("Testing choose_multiple_from_options", ["One", "Two", "Three", "Four"])
    assert ["Two", "One"] == choose_multiple_from_options("Testing choose_multiple_from_options", ["One", "Two", "Three", "Four"])
    assert [] == choose_multiple_from_options("Testing choose_multiple_from_options", ["One", "Two", "Three", "Four"])
    assert ["Four"] == choose_multiple_from_options("Testing choose_multiple_from_options", ["One", "Two", "Three", "Four"])
    assert ["One", "Two"] == choose_multiple_from_options("Testing choose_multiple_from_options", ["One", "Two", "Three", "Four"], option_choice="choices")
    assert [] == choose_multiple_from_options("Testing choose_multiple_from_options", ["One", "Two", "Three", "Four"], exit_choice="quit")

def test_free_user_input(monkeypatch):
    inputs = ["Test", "A Test", "A longer test", 1]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    assert free_user_input("Testing free_user_input") == "Test"
    assert free_user_input("Testing free_user_input") == "A Test"
    assert free_user_input("Testing free_user_input") == "A longer test"
    assert free_user_input("Testing free_user_input") == 1

def test_handle_create(monkeypatch):
    create_table_statement = """CREATE TABLE IF NOT EXISTS test (
        name TEXT,
        age INTEGER
    );"""
    search_statement = "SELECT * FROM test;"
    to_print = """{
    "fields": ["age", "name"],
    "values": ["44", "Dan"]
}
"""
    with open("../input/pytest/test_create.json", "w") as f:
        print(to_print, file=f)
    inputs = ["manually", "Bill", "82", "exit", "manually", "exit", "file", "/pytest/test_create.json"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    try:
        if os.path.exists("./databases/pytest.db"):
            os.remove("./databases/pytest.db")
        with sqlite3.connect('./databases/pytest.db') as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_statement)
            conn.commit()
            handle_create("pytest", "test")
            handle_create("pytest", "test")
            handle_create("pytest", "test")
            handle_create("pytest", "test")
            cursor.execute(search_statement)
            rows = cursor.fetchall()
            assert list(rows[0]) == ['"Bill"', '"82"']
            assert list(rows[1]) == ['"Dan"', '"44"']
    except sqlite3.OperationalError as e:
        print("Failed to open database in memory:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    if os.path.exists("../input/pytest/test_create.json"):
        os.remove("../input/pytest/test_create.json")

def test_handle_read(monkeypatch, capsys):
    create_table_statement = """CREATE TABLE IF NOT EXISTS test (
        name TEXT,
        age INTEGER
    );"""
    insert_data_statements = [
        """INSERT INTO test(name,age) VALUES("Bill",82);""",
        """INSERT INTO test(age,name) VALUES(44,"Dan");"""
    ]
    to_print = """{
    "selections": ["age", "name"],
    "fields": ["age"],
    "values": [82]
}
"""
    with open("../input/pytest/test_read.json", "w") as f:
        print(to_print, file=f)
    inputs = ["manually", "all", "no", "manually", "some", "name", "exit", "yes", "age", "exit", 44, "file", "/pytest/test_read.json"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    try:
        if os.path.exists("./databases/pytest.db"):
            os.remove("./databases/pytest.db")
        with sqlite3.connect('./databases/pytest.db') as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_statement)
            conn.commit()
            for statement in insert_data_statements:
                cursor.execute(statement)
            conn.commit()
            handle_read("pytest", "test", rowid=True)
            captured = capsys.readouterr()
            assert captured.out == "[(1, 'Bill', 82), (2, 'Dan', 44)]\n"
            handle_read("pytest", "test", rowid=False)
            captured = capsys.readouterr()
            assert captured.out == "[('Dan',)]\n"
            handle_read("pytest", "test", rowid=True)
            captured = capsys.readouterr()
            assert captured.out == "[(1, 82, 'Bill')]\n"
    except sqlite3.OperationalError as e:
        print("Failed to open database in memory:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")


def test_handle_update():
    pass

def test_handle_delete():
    pass

def test_handle_print(monkeypatch):
    create_table_statement = """CREATE TABLE IF NOT EXISTS test (
        name TEXT,
        age INTEGER
    );"""
    insert_data_statements = [
        """INSERT INTO test(name,age) VALUES("Bill",82);""",
        """INSERT INTO test(age,name) VALUES(44,"Dan");"""
    ]
    inputs = ["pytest.txt"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    try:
        if os.path.exists("./databases/pytest.db"):
            os.remove("./databases/pytest.db")
        with sqlite3.connect('./databases/pytest.db') as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_statement)
            conn.commit()
            for statement in insert_data_statements:
                cursor.execute(statement)
            conn.commit()
            if os.path.exists("../output/pytest.txt"):
                os.remove("../output/pytest.txt")
            handle_print("pytest", "test")
            with open("../output/pytest.txt") as f:
                file_content = f.read()
                assert file_content == """
+-------+------+-----+
| rowid | name | age |
+-------+------+-----+
| 1     | Bill | 82  |
| 2     | Dan  | 44  |
+-------+------+-----+
"""
    except sqlite3.OperationalError as e:
        print("Failed to open database in memory:", e)
    if os.path.exists("./databases/pytest.db"):
        os.remove("./databases/pytest.db")
    if os.path.exists("../output/pytest.txt"):
        os.remove("../output/pytest.txt")

def test_handle_run():
    pass

def test_handle_prepare():
    pass

