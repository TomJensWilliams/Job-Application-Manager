import copy
import json
from web import website_functions
from databases import database_functions


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %% Database Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

# Databases

def create_database(database, /, *, print_statements=False):
    database_functions.create_database(database, print_statements=print_statements)

# Tables

def create_table(database, table, fields, datatypes, /, *, print_statements=False):
    database_functions.create_table(database, table, fields, datatypes, print_statements=print_statements)

# Fields

def read_fields(database, table, /, *, rowid=False, print_statements=False):
    return database_functions.read_fields(database, table, rowid=rowid, print_statements=print_statements)

# Records

def create_record(database, table, fields, values, /, *, print_statements=False):
    database_functions.create_record(database, table, fields, values, print_statements=print_statements)

def read_records(database, table, /, *, rowid=False, selections=None, fields=None, values=None, print_statements=False):
    return database_functions.read_records(database, table, rowid=rowid, selections=selections, fields=fields, values=values, print_statements=print_statements)
    
def update_records(database, table, update_fields, update_values, /, *, match_fields=None, match_values=None, print_statements=False):
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
            if len(str(row[index])) > max_characters_in_index[index]:
                max_characters_in_index[index] = len(str(row[index]))
    dividing_line = "\n+"
    for index in range(0, len(header_content)):
        dividing_line += f"-{'-' * (max_characters_in_index[index])}-+"
    text_to_output = f"{dividing_line}\n|"
    for index in range(0, len(header_content)):
        text_to_output += f" {header_content[index] + (' ' * (max_characters_in_index[index] - len(header_content[index])))} |"
    text_to_output += dividing_line
    for row in rows_content:
        text_to_output += "\n|"
        for index in range(0, len(row)):
            text_to_output += f" {str(row[index]) + (' ' * (max_characters_in_index[index] - len(str(row[index]))))} |"
    text_to_output += dividing_line
    with open(f"../output/{filename}", 'w') as f:
        print(text_to_output, file=f)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# % Web Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

# DELETE OR CONNECT TO CLI?

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# % Composite Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

def run_search(table, search_id, /, *, print_statements=False):
    url_list = database_functions.read_records("searches", table, rowid=False, selections=["urls"], fields=["rowid"], values=[search_id], print_statements=print_statements)
    found_ids = website_functions.retrieve_job_ids(table, url_list, print_statements=print_statements)
    old_ids = database_functions.read_records("searches", table, rowid=False, selections=["job_id"], fields=None, values=None, print_statements=print_statements)
    new_ids = []
    for id in found_ids:
        if not id in old_ids:
            new_ids.append(id)
    job_fields = database_functions.read_fields("jobs", table, rowid=False, print_statements=print_statements)
    all_jobs_data = website_functions.process_job_ids(table, new_ids, job_fields, print_statements=print_statements)
    for job_data in all_jobs_data:
        create_record("jobs", table, job_fields, job_data, print_statements=print_statements)
    """
    url_list = read_records(database, website, selections="urls", fields="rowid", values=search_id, print_statements=print_statement)
    if website == "glassdoor":
        found_ids = glassdoor.search(url_list)
    elif website == "indeed":
        found_ids = indeed.search(url_list)
    elif website == "linkedin":
        found_ids = linkedin.search(url_list)
    elif website == "monster":
        found_ids = monster.search(url_list)
    elif website == "ziprecruiter":
        found_ids = ziprecruiter.search(url_list)
    old_ids = read_records(database, website, selections="job_id", fields=None, values=None, print_statements=print_statement)
    new_ids = []
    for id in found_ids:
        if id not in old_ids:
            new_ids.append(id)
    for id in new_ids:
        if website == "glassdoor":
            all_jobs_data = glassdoor.process_jobs(new_ids)
        elif website == "indeed":
            all_jobs_data = indeed.process_jobs(new_ids)
        elif website == "linkedin":
            all_jobs_data = linkedin.process_jobs(new_ids)
        elif website == "monster":
            all_jobs_data = monster.process_jobs(new_ids)
        elif website == "ziprecruiter":
            all_jobs_data = ziprecruiter.process_jobs(new_ids)
    for job_data in all_jobs_data:
        create_record("jobs", website, job_data)
    """

def prepare_search(table, parameters, /, *, print_statements=False):
    create_and_update_dictionaries(table, parameters, print_statements=print_statements)
    keyed_dictionaries = database_functions.read_records("dictionaries", table, rowid=False, selections=["parameter", "dictionary"], fields=None, values=None, print_statements=print_statements)
    base_url = website_functions.get_base_url(table)
    urls = [base_url]
    for key in parameters:
        current_key_index = [element[0] for element in keyed_dictionaries].index(key)
        for index in range(0, len(parameters[key])):
            old_urls = copy.copy(urls)
            old_length = len(urls)
            if index == 0:
                for url_index in range(0, old_length):
                    urls[url_index] += keyed_dictionaries[current_key_index][parameters[key][index]]
            else:
                for url_index in range(0, old_length):
                    urls.append(f"{old_urls[url_index]}{keyed_dictionaries[current_key_index][parameters[key][index]]}")
    database_functions.create_record("searches", table, ["parameters", "urls"], [parameters, urls], print_statements=print_statements)

def create_and_update_dictionaries(table, parameters, /, *, print_statements=False):
    dictionaries_to_create = []
    dictionaries_to_update = []
    old_key_dictionary_pairs = database_functions.read_records("dictionaries", table, rowid=False, selections=["parameter", "dictionary"], fields=None, values=None, print_statements=print_statements)
    old_keys = [json.loads(pair[0]) for pair in old_key_dictionary_pairs]
    for key in list(parameters.keys()):
        if not key in old_keys:
            dictionaries_to_create.append(key)
        else:
            dictionary_update_set = {"key": key, "values": []}
            old_key_index = old_keys.index(key)
            for value in parameters[key]:
                if not value in list(json.loads(old_key_dictionary_pairs[old_key_index][1]).keys()):
                    dictionary_update_set["values"].append(value)
            if len(dictionary_update_set["values"]) != 0:
                dictionaries_to_update.append(dictionary_update_set)
    if len(dictionaries_to_create) == 0 and len(dictionaries_to_update) == 0:
        return
    else:
        update_index = len(dictionaries_to_create)
        all_parameters = []
        for key in dictionaries_to_create:
            all_parameters.append({"key": key, "values": parameters[key]})
        for object in dictionaries_to_update:
            all_parameters.append(object)
        dictionary_contents = website_functions.process_search_parameters(table, all_parameters, print_statements=print_statements)
        for index in range(0, update_index):
            print(f"{index} {update_index} {len(dictionary_contents)}")
            database_functions.create_record("dictionaries", table, dictionary_contents[index]["key"], dictionary_contents[index]["dictionary"], print_statements=print_statements)
        for index in range(update_index, len(dictionary_contents)):
            new_dictionary = old_key_dictionary_pairs[old_keys.index(dictionary_contents[index]["key"])][1]
            for key, value in dictionary_contents[index]["dictionary"]:
                new_dictionary[key] = value
            database_functions.update_records("dictionaries", table, "dictionary", new_dictionary, "parameter", dictionary_contents[index]["key"], print_statements=print_statements)

    """
    all_key_dictionary_pairs = read_records("dictionaries", website, selections=["parameter", "dictionary"], print_statements=print_statements)
    all_keys = [element[0] for element in all_key_dictionary_pairs]
    keys_to_create = []
    keys_values_to_update = []
    all_update_content =[]
    for key in list(parameters.keys()):
        if not key in all_keys:
            keys_to_create.append(key)
        else:
            for index in range(0, len(parameters[key])):
                if not parameters[key][index] in all_key_dictionary_pairs[key]:
                    keys_values_to_update.append([key, parameters[key][index]])
    for index in range(0, len(keys_to_create)):
        if website == "glassdoor":
            dictionaries_content = glassdoor.prepare_search_dictionary(parameters)
        elif website == "indeed":
            dictionaries_content = indeed.prepare_search_dictionary()
        elif website == "linkedin":
            dictionaries_content = linkedin.prepare_search_dictionary()
        elif website == "monster":
            dictionaries_content = monster.prepare_search_dictionary()
        elif website == "ziprecruiter":
            dictionaries_content = ziprecruiter.prepare_search_dictionary()
        for dictionary in dictionaries_content:
            create_record("searches", website, dic, print_statements)
        # all_update_content.append("PALCEHOLDER")
    for index in range(0, len(keys_values_to_update)):
        # all_update_content.append("PLACEHOLDER")
    for index in range(0, len(all_update_content)):
        update_records("dictionaries", website, all_update_content[index][0], website, all_update_content[index][1], website, all_update_content[index][2], website, all_update_content[index][3], print_statements)
"""
