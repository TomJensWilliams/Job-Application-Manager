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

def create_record(database, table, values):
    if database == "dictionaries":
        dictionaries_db.create_dictionary(table, values)
    elif database == "jobs":
        jobs_db.create_job(table, values)
    elif database == "searches":
        searches_db.create_search(table, values)

def create_records(database, table, values_list):
    if database == "dictionaries":
        dictionaries_db.create_dictionaries(table, values_list)
    elif database == "jobs":
        jobs_db.create_jobs(table, values_list)
    elif database == "searches":
        searches_db.create_searches(table, values_list)

def read_record(database, table, id):
    if database == "dictionaries":
        dictionaries_db.read_dictionary(table, id)
    elif database == "jobs":
        jobs_db.read_job(table, id)
    elif database == "searches":
        searches_db.read_search(table, id)

def read_record_field(database, table, field, value):
    if database == "dictionaries":
        dictionaries_db.read_dictionary_field(table, field, value)
    elif database == "jobs":
        jobs_db.read_job_field(table, field, value)
    elif database == "searches":
        searches_db.read_search_field(table, field, value)

def read_records(database, table, id_list):
    if database == "dictionaries":
        dictionaries_db.read_dictionaries(table, id_list)
    elif database == "jobs":
        jobs_db.read_jobs(table, id_list)
    elif database == "searches":
        searches_db.read_searches(table, id_list)

def read_records_field(database, table, field, value_list):
    if database == "dictionaries":
        dictionaries_db.read_dictionaries_field(table, field, value_list)
    elif database == "jobs":
        jobs_db.read_jobs_field(table, field, value_list)
    elif database == "searches":
        searches_db.read_searches_field(table, field, value_list)

def read_all_records(database, table):
    if database == "dictionaries":
        dictionaries_db.read_all_dictionaries(table)
    elif database == "jobs":
        jobs_db.read_all_jobs(table)
    elif database == "searches":
        searches_db.read_all_searches(table)

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

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# % Web Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# % Composite Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

def run_dictionary_update(website, field, input_list):
    if website == "glassdoor":
        found_value = glassdoor.find_corresponding_url_value(website, field, input_list)
    elif website == "indeed":
        found_value = indeed.find_corresponding_url_value(website, field, input_list)
    elif website == "linkedin":
        found_value = linkedin.find_corresponding_url_value(website, field, input_list)
    elif website == "monster":
        found_value = monster.find_corresponding_url_value(website, field, input_list)
    elif website == "ziprecruiter":
        found_value = ziprecruiter.find_corresponding_url_value(website, field, input_list)
    records_to_update = read_records_field("dictionaries", website, field, input_list)
    records_to_create = []
    """
    LOGIC TO CREATE records_to_create
    """
    """
    LOGIC TO UPDATE ALL OF records_to_update
    """
    for record in records_to_create:
        create_record("dictionaries", website, record)
        
    

def run_search(website, parameters):
    # BELOW LINE WILL NEED TO BE EDITED TO GET URL_LIST OUT OF RETURNED DATA
    url_list = read_record_field("searches", website, "parameters", parameters)
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
    # BELOW LINE WILL PROBABLY NEED TO BE EDITED TO EXTRACT VALUES
    old_ids = read_all_records("jobs", website)
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
