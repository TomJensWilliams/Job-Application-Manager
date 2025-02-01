from web import glassdoor
from web import indeed
from web import linkedin
from web import monster
from web import ziprecruiter
from databases import jobs_db
from databases import searches_db
from databases import dictionaries_db


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %% Database Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

def create_database(database):
    if database == "dictionaries":
        dictionaries_db.create_database()
    elif database == "jobs":
        jobs_db.create_database()
    elif database == "searches":
        searches_db.create_database()

def create_table(database, table, fields, datatypes):
    if database == "dictionaries":
        dictionaries_db.create_table(table, fields, datatypes)
    elif database == "jobs":
        jobs_db.create_table(table, fields, datatypes)
    elif database == "searches":
        searches_db.create_table(table, fields, datatypes)

def create_tables(database, table_list, fields_list, datatypes_list):
    if database == "dictionaries":
        dictionaries_db.create_tables(table_list, fields_list, datatypes_list)
    elif database == "jobs":
        jobs_db.create_tables(table_list, fields_list, datatypes_list)
    elif database == "searches":
        searches_db.create_tables(table_list, fields_list, datatypes_list)

def read_fields(database, table):
    if database == "dictionaries":
        return dictionaries_db.read_fields(table)
    elif database == "jobs":
        return jobs_db.read_fields(table)
    elif database == "searches":
        return searches_db.read_fields(table)

def create_record(database, table, fields, values):
    if database == "dictionaries":
        dictionaries_db.create_dictionary(table, fields, values)
    elif database == "jobs":
        jobs_db.create_job(table, fields, values)
    elif database == "searches":
        searches_db.create_search(table, fields, values)

def create_records(database, table, fields_list, values_list):
    if database == "dictionaries":
        dictionaries_db.create_dictionaries(table, fields_list, values_list)
    elif database == "jobs":
        jobs_db.create_jobs(table, fields_list, values_list)
    elif database == "searches":
        searches_db.create_searches(table, fields_list, values_list)

def read_record(database, table, id):
    if database == "dictionaries":
        return dictionaries_db.read_dictionary(table, id)
    elif database == "jobs":
        return jobs_db.read_job(table, id)
    elif database == "searches":
        return searches_db.read_search(table, id)

def read_record_field(database, table, field, value):
    if database == "dictionaries":
        return dictionaries_db.read_dictionary_field(table, field, value)
    elif database == "jobs":
        return jobs_db.read_job_field(table, field, value)
    elif database == "searches":
        return searches_db.read_search_field(table, field, value)

def read_records(database, table, id_list):
    if database == "dictionaries":
        return dictionaries_db.read_dictionaries(table, id_list)
    elif database == "jobs":
        return jobs_db.read_jobs(table, id_list)
    elif database == "searches":
        return searches_db.read_searches(table, id_list)

def read_records_field(database, table, field, value_list):
    if database == "dictionaries":
        return dictionaries_db.read_dictionaries_field(table, field, value_list)
    elif database == "jobs":
        return jobs_db.read_jobs_field(table, field, value_list)
    elif database == "searches":
        return searches_db.read_searches_field(table, field, value_list)

def read_all_records(database, table):
    if database == "dictionaries":
        return dictionaries_db.read_all_dictionaries(table)
    elif database == "jobs":
        return jobs_db.read_all_jobs(table)
    elif database == "searches":
        return searches_db.read_all_searches(table)

def update_record(database, table, id, fields, values):
    if database == "dictionaries":
        dictionaries_db.update_dictionary(table, id, fields, values)
    elif database == "jobs":
        jobs_db.update_job(table, id, fields, values)
    elif database == "searches":
        searches_db.update_search(table, id, fields, values)

def update_record_field(database, table, search_field, search_value, fields, values):
    pass

def update_records(database, table, id_list, fields_list, values_list):
    pass

def update_records_field(database, table, search_field, search_value_list, fields_list, values_list):
    pass

def delete_record():
    pass

def delete_record_field():
    pass

def delete_records():
    pass

def delete_records_field():
    pass

def delete_all_records():
    pass

def print_table(database, website, filename):
    header_content = read_fields(database, website)
    rows_content = read_all_records(database, website)
    max_characters_in_index = [0] * len(rows_content[0])
    for index in range(0, len(header_content)):
        if len(header_content[index]) > max_characters_in_index[index]:
            max_characters_in_index[index] = len(header_content[index])
    for row in rows_content:
        for index in range(0, len(row)):
            current_thing = row[index]
            if not isinstance(current_thing, str):
                current_thing = str(current_thing)
            if len(current_thing) > max_characters_in_index[index]:
                max_characters_in_index[index] = len(row[index])
    dividing_line = "\n+"
    for index in range(0, len(header_content)):
        dividing_line += "-" * (max_characters_in_index[index] + 2)
        dividing_line += "+"
    text_to_output = dividing_line
    text_to_output += "\n|"
    for index in range(0, len(header_content)):
        text_to_output += f" {header_content[index] + (' ' * (max_characters_in_index[index] - len(header_content[index])))} |"
    text_to_output += dividing_line
    for row in rows_content:
        text_to_output += "\n|"
        for index in range(0, len(row)):
            current_thing = row[index]
            if not isinstance(current_thing, str):
                current_thing = str(current_thing)
            text_to_output += f" {current_thing + (' ' * (max_characters_in_index[index] - len(current_thing)))} |"
    text_to_output += dividing_line
    with open(f"{filename}.txt", 'w') as f:
        print(text_to_output, file=f)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# % Web Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# % Composite Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

def run_search(website, search_id):
    url_list = read_record("searches", website, search_id)[2]
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
    old_ids = [record[0] for record in read_all_records("jobs", website)]
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

def process_create_search(website, parameters):
    process_search_parameters(website, parameters)
    website_dictionaries = {}
    dictionaries_names = []
    all_parameters_values = []
    for key, value in parameters.items():
        website_dictionaries[key] = read_record_field("dictionaries", website, "parameter", key)
        dictionaries_names.append(key)
        all_parameters_values.append(value)
    while len(all_parameters_values) > 1:
        first_list = all_parameters_values.pop(1)
        second_list = all_parameters_values.pop(1)
        combined_list = []
        for first_item in first_list:
            for second_item in second_list:
                combined_list.push(first_item + second_item)
        all_parameters_values.insert(0, combined_list)
    all_parameters_values_combined = all_parameters_values[0]
    all_urls = []
    for parameters_list in all_parameters_values_combined:
        if website == "glassdoor":
            current_url = ""
        elif website == "indeed":
            current_url = "https://www.indeed.com/jobs"
        elif website == "linkedin":
            current_url = "https://www.linkedin.com/jobs/search/"
        elif website == "monster":
            current_url = ""
        elif website == "ziprecruiter":
            current_url = ""
        for index in range(0, len(parameters_list)):
            current_url += website_dictionaries[dictionaries_names[index]][parameters_list[index]]
        all_urls.append(current_url)
    create_record("searches", website, ["parameters", "urls"], [parameters, all_urls])


def process_search_parameters(website, parameters):
    website_dictionaries = {}
    dictionaries_to_create = []
    dictionaries_to_update = []
    for key, value in parameters.items():
        website_dictionaries[key] = read_record_field("dictionaries", website, "parameter", key)
        if website_dictionaries[key] == None:
            dictionaries_to_create.append([key, value])
        elif not all(parameter in website_dictionaries[key] for parameter in parameters[key]):
            dictionaries_to_update.append([key, value])
    for dictionary in dictionaries_to_create:
        if website == "glassdoor":
            new_dictionary = glassdoor.prepare_search_dictionary(key, value)
        elif website == "indeed":
            new_dictionary = indeed.prepare_search_dictionary(key, value)
        elif website == "linkedin":
            new_dictionary = linkedin.prepare_search_dictionary(key, value)
        elif website == "monster":
            new_dictionary = monster.prepare_search_dictionary(key, value)
        elif website == "ziprecruiter":
            new_dictionary = ziprecruiter.prepare_search_dictionary(key, value)
        create_record("dictionaries", website, ["parameter", "dictionary"], [key, new_dictionary])
    for dictionary in dictionaries_to_update:
            pass