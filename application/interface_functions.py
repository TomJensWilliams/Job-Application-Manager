import os
import sys
if "/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager/application" in sys.path:
    sys.path[sys.path.index("/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager/application")] = "/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager"
import datetime
import copy
import json
import re
import shutil
import traceback
from application.web import website_functions
from application.databases import database_functions

# Databases

def create_database(database, /, *, print_statements=False):
    database_functions.create_database(database, print_statements=print_statements)

def backup_database(database, /, *, backup_name=None, print_statements=False):
    return database_functions.backup_database(database, backup_name=backup_name, print_statements=print_statements)

def backup_databases(databases, /, *, backup_name=None, print_statements=False):
    if backup_name == None:
        backup_name = datetime.datetime.now()
    if os.path.isdir(f"../backup/{backup_name}.db"):
        raise BaseException("Attempting to create backup with a name that already exists.")
    os.mkdir(f"../backup/{backup_name}")
    for database in databases:
        shutil.copy(f"./databases/{database}.db", f"../backup/{backup_name}")
    if print_statements: print(f"{database} databases backed up successfully in {backup_name}.")
    return backup_name

def restore_database(database, backup_name, /, *, print_statements=False):
    database_functions.restore_database(database, backup_name, print_statements=print_statements)

def restore_databases(databases, backup_name, /, *, print_statements=False):
    for database in databases:
        if os.path.isfile(f"./databases/{database}.db"):
            if not os.path.isdir(f"../failsafe"):
                os.mkdir("../failsafe")
            shutil.copy(f"./databases/{database}.db", f"../failsafe")
            os.remove(f"./databases/{database}.db")
    for database in databases:
        try:
            shutil.copy(f"../backup/{backup_name}/{database}.db", "./databases")
            if print_statements: print(f"{database} database restored successfully from {backup_name}")
        except Exception:
            for database in databases:
                if os.path.isfile(f"./databases/{database}.db"):
                    os.remove(f"./databases/{database}.db")
                if os.path.isdir("../failsafe"):
                    shutil.copy(f"../failsafe/{database}.db", "./databases")
        finally:
            if os.path.isdir("../failsafe"):
                shutil.rmtree("../failsafe")

# Tables

def create_table(database, table, fields, datatypes, /, *, print_statements=False):
    database_functions.create_table(database, table, fields, datatypes, print_statements=print_statements)

# Fields

def read_fields(database, table, /, *, rowid=False, print_statements=False):
    return database_functions.read_fields(database, table, rowid=rowid, print_statements=print_statements)

def read_fields_datatypes(database, table, /, *, print_statements=False):
    return database_functions.read_fields_datatypes(database, table, print_statements=print_statements)

# Records

def create_record(database, table, fields, values, /, *, print_statements=False):
    database_functions.create_record(database, table, fields, values, print_statements=print_statements)

def read_records(database, table, /, *, rowid=False, selections=None, fields=None, values=None, print_statements=False):
    return database_functions.read_records(database, table, rowid=rowid, selections=selections, fields=fields, values=values, print_statements=print_statements)
    
def update_records(database, table, update_fields, update_values, /, *, match_fields=None, match_values=None, print_statements=True):
    database_functions.update_records(database, table, update_fields, update_values, match_fields=match_fields, match_values=match_values, print_statements=print_statements)

def delete_records(database, table, /, *, fields=None, values=None, print_statements=False):
    database_functions.delete_records(database, table, fields=fields, values=values, print_statements=print_statements)

# Additional Functionality

def print_table(database, table, filename, /, *, print_statements=False):
    header_content = read_fields(database, table, rowid=True, print_statements=print_statements)
    rows_content = read_records(database, table, rowid=True, selections=None, fields=None, values=None, print_statements=print_statements)
    max_characters_in_index = [len(element) for element in header_content]
    for row in rows_content:
        for index in range(0, len(row)):
            max_characters_in_index[index] = max_characters_in_index[index] if max_characters_in_index[index] > len(str(row[index])) else len(str(row[index]))
    dividing_line = f"""\n+{''.join([f"-{'-'* (max_characters_in_index[index])}-+" for index in range(0, len(header_content))])}"""
    text_to_output = f"""{dividing_line}\n|{''.join([f" {header_content[index] + (' ' * (max_characters_in_index[index] - len(header_content[index])))} |" for index in range(0, len(header_content))])}{dividing_line}"""
    for row in rows_content:
        text_to_output += f"""\n|{''.join([f" {str(row[index]) + (' ' * (max_characters_in_index[index] - len(str(row[index]))))} |" for index in range(0, len(row))])}"""
    text_to_output += dividing_line
    with open(f"../output/{filename}", 'w') as f:
        print(text_to_output, file=f)

def run_search(table, search_id, /, *, print_statements=False):
    failsafe_name = backup_database("searches")
    try:
        url_list = database_functions.read_records("searches", table, rowid=False, selections=["urls"], fields=["rowid"], values=[search_id], print_statements=print_statements)[0][0]
        found_ids = website_functions.retrieve_job_ids(table, url_list, print_statements=print_statements)
        found_ids = list(set(found_ids))
        old_ids = [element[0] for element in database_functions.read_records("jobs", table, rowid=False, selections=["job_id"], fields=None, values=None, print_statements=print_statements)]
        print(old_ids)
        if old_ids != None:
            new_ids = [id for id in found_ids if not id in old_ids]
        else:
            new_ids = found_ids
        job_fields = database_functions.read_fields("jobs", table, rowid=False, print_statements=print_statements)
        all_jobs_data = website_functions.process_job_ids(table, new_ids, job_fields, print_statements=print_statements)
        for job_data in all_jobs_data:
            create_record("jobs", table, job_fields, job_data, print_statements=print_statements)
    except Exception as e:
        print("Run search failed:", e)
        restore_database("searches", failsafe_name)
    finally:
        if os.path.isdir(f"../backup/{failsafe_name}"):
            shutil.rmtree(f"../backup/{failsafe_name}")


def prepare_search(table, parameters, /, *, print_statements=False):
    failsafe_name = backup_database("searches")
    try:
        create_and_update_dictionaries(table, parameters, print_statements=print_statements)
        print_table("dictionaries", table, "MID_FUNCTION_CAPTURE.txt") # REMOVE LATER!!!!!!!!!!!!!!!!!
        keyed_dictionaries = database_functions.read_records("dictionaries", table, rowid=False, selections=["parameter", "dictionary"], fields=None, values=None, print_statements=print_statements)
        base_url = website_functions.get_base_url(table)
        urls = [base_url]
        for key, values in parameters.items():
            key_index = [element[0] for element in keyed_dictionaries].index(key)
            new_urls = [url + keyed_dictionaries[key_index][1][value] for value in values for url in urls]
            urls = new_urls
        urls = [url + "\n\n" for url in urls]
        database_functions.create_record("searches", table, ["parameters", "urls"], [parameters, urls], print_statements=print_statements)
        print_table("searches", table, "AFTER_FUNCTION_CAPTURE.txt") # REMOVE LATER!!!!!!!!!!!!!
    except Exception as e:
        print("Prepare Search failed:", e)
        traceback.print_exc(file=sys.stdout)
        restore_database("searches", failsafe_name)
    finally:
        if os.path.isdir(f"../backup/{failsafe_name}"):
            shutil.rmtree(f"../backup/{failsafe_name}")

def create_and_update_dictionaries(table, parameters, /, *, print_statements=False):
    update_index = 0
    all_parameters = []
    old_key_dictionary_pairs = database_functions.read_records("dictionaries", table, rowid=False, selections=["parameter", "dictionary"], fields=None, values=None, print_statements=print_statements)
    old_keys = [pair[0] for pair in old_key_dictionary_pairs]
    print(f"# {old_keys}")
    print(f"## {list(parameters.keys())}")
    for key in list(parameters.keys()):
        print(f"###{key}: {parameters[key]}")
    for key in list(parameters.keys()):
        if not key in old_keys:
            all_parameters.insert(0,{"key": key, "values": parameters[key]})
            update_index += 1
        else:
            dictionary_update_set = {"key": key, "values": []}
            old_key_index = old_keys.index(key)
            for value in parameters[key]:
                if not value in list(old_key_dictionary_pairs[old_key_index][1].keys()):
                    dictionary_update_set["values"].append(value)
            if len(dictionary_update_set["values"]) != 0:
                all_parameters.append(dictionary_update_set)
    if len(all_parameters) == 0:
        return
    else:
        print(f"#### {all_parameters}")
        dictionary_contents = website_functions.process_search_parameters(table, all_parameters, print_statements=print_statements)
        for index in range(0, update_index):
            database_functions.create_record("dictionaries", table, dictionary_contents[index]["key"], dictionary_contents[index]["dictionary"], print_statements=print_statements)
        for index in range(update_index, len(dictionary_contents)):
            new_dictionary = old_key_dictionary_pairs[old_keys.index(dictionary_contents[index]["key"])][1]
            for key, value in dictionary_contents[index]["dictionary"].items():
                new_dictionary[key] = value
            database_functions.update_records("dictionaries", table, ["dictionary"], [new_dictionary], match_fields=["parameter"], match_values=[dictionary_contents[index]["key"]], print_statements=print_statements)