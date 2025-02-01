import datetime
from interface_functions import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~ Handling Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def handle_website_input():
    return ask_until_answered("What website are you interacting with?\n(Enter \"options\" to see all options\n or enter \"exit\" to quit program)\t", ["options", "glassdoor", "indeed", "linkedin", "monster", "ziprecruiter", "exit"])
    
def handle_object_input():
    return ask_until_answered("What type of object are you interacting with?\n(Enter \"options\" to see all options)\t", ["options", "jobs", "searches"])

def handle_action_input(object):
    options = ["options", "create", "read", "update", "delete"]
    if object == "searches":
        options.append("run")
    return ask_until_answered("What action are you performing?\n(Enter \"options\" to see all options)\t", options)

def handle_create_job(website):
    job_id = ask_until_answered_open("What is the title of the job?\n", ["options", "None"])
    job_applied = ask_until_answered_open("What is the applied status for this job?\n", ["options", "None"])
    job_title = ask_until_answered_open("What is the job's title?\n", ["options", "None"])
    job_company = ask_until_answered_open("What is the company's name?\n", ["options", "None"])
    job_location = ask_until_answered_open("What is this job's location?\n", ["options", "None"])
    job_address = ask_until_answered_open("What is the job's address?", ["options", "None"])
    job_number = ask_until_answered_open("What is the company's phone number?", ["options", "None"])
    job_email = ask_until_answered_open("What is the company's email?", ["options", "None"])
    job_website = ask_until_answered_open("What is the company's website?", ["options", "None"])
    job_date = str(datetime.datetime.now())
    job_note = ask_until_answered_open("Would you like to add any note about this job?\n", ["options", "None"])
    create_job(website, [job_id, job_applied, job_title, job_company, job_location, job_address, job_number, job_email, job_website, job_date, job_note])

def handle_read_job(website):
    how_many_jobs = ask_until_answered("Would you like to view one job, multiple jobs, or all jobs?\t", ["options", "one", "multiple", "all"])
    if how_many_jobs == "one":
        job_id = ask_until_answered_open("what is the job id?\t", ["options"])
        print("\n")
        print(read_job(website, job_id))
        print("\n")
    elif how_many_jobs == "multiple":
        job_ids = []
        job_id = ask_until_answered_open("What is the next job id?\t", ["options", "None"])
        while job_id != None:
            job_ids.append(job_id)
            job_id = ask_until_answered_open("what is the next job id?\t", ["options", "None"])
        print("\n")
        for job_id in job_ids:
            print(read_job(website, job_id))
        print("\n")
    elif how_many_jobs == "all":
        for job in read_all_records(website):
            print(job)
        print("\n")

def handle_update_job(website):
    pass

def handle_delete_job(website):
    pass

def handle_create_search(website):
    pass

def handle_read_search(website):
    pass

def handle_update_search(website):
    pass

def handle_delete_search(website):
    pass

def handle_run_search(website):
    pass

def handle_create_job_glassdoor():
    pass

def ask_until_answered(question, options):
    while True:
        user_input = input(question)
        if user_input in options[:1]:
            options_string = " ".join(options[1:])
            print(f"\nThese are the current options:\n{options_string}\n")
        elif user_input in options[1:]:
            print("\n")
            return user_input
        else:
            print("\nThat was not an acceptable option.\n")

def ask_until_answered_open(question, options):
    while True:
        user_input = input(question)
        if user_input in options[:1]:
            options_string = " ".join(options[1:])
            print(f"\nThese are the current options:\n{options_string}\n")
        elif user_input in options[1:2]:
            return None
        elif user_input in options[2:]:
            # HERE INCASE I USE THIS LATER
            pass
        else:
            return user_input

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~ Main Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

while True:
    database = handle_database_input()
    website = hande_website_input()
    action = handle_action_input(database)
    quantity = handle_quantity_input(action)
    if action == "create" and quantity == "one":
        
    elif action == "create" and quantity == "multiple":

    elif action == "read" and quantity == "one":
        id = handle_id_input()
        read_record(database, website, id)
    elif action == "read" and quantity == "multiple":
        id_list = handle_id_list_input()
        read_records
    elif action == "read" and quantity == "all":
    elif action == "update" and quantity == "one":
    elif action == "update" and quantity == "multiple":
    elif action == "delete" and quantity == "one":
    elif action == "delete" and quantity == "multiple":
    elif action == "delete" and quantity == "all":
    elif action == "run" and quantity == "one":
    elif action == "run" and quantity == "multiple":
    elif action == "run" and quantity == "all":

    website = handle_website_input()
    if website == "exit":
        break
    object = handle_object_input()
    action = handle_action_input(object)
    print(f"{website} {action} {object}\n")
    if object == "jobs":
        if action == "create":
            handle_create_job(website)
        elif action == "read":
            handle_read_job(website)
        elif action == "update":
            handle_update_job(website)
        elif action == "delete":
            handle_delete_job(website)
    elif object == "searches":
        if action == "create":
            handle_create_search(website)
        elif action == "read":
            handle_read_search(website)
        elif action == "update":
            handle_update_search(website)
        elif action == "delete":
            handle_delete_search(website)
        elif action == "run":
            handle_run_search(website)
