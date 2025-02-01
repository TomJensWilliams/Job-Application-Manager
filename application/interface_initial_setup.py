import json
from interface_functions import *

# This will contain the lines of code which should be able to be
# run upon downloading this application, and prepare the databases
# enough that they are ready for individual use.

# Things such as searches will not be created, and dictionary
# values which are variable and user input, such as job titles and
# locations, will not be set, but dictionaries which are stable
# and chosen from a consistent list, such as date posted and
# radius, will be preemptively created in this script.

#################
# All Databases #
#################

all_databases = ["dictionaries", "jobs", "searches"]
for database in all_databases:
    create_database(database)

################
# All Websites #
################
all_websites = ["glassdoor", "indeed", "linkedin", "monster", "ziprecruiter"]
dictionaries_fields = ["id","parameter", "dictionary"]
dictionaries_datatypes = ["INTEGER PRIMARY KEY", "TEXT", "TEXT"]
jobs_fields = ["id", "applied", "title", "company", "location", "address", "number", "email", "website", "date", "note"]
jobs_datatypes = ["TEXT PRIMARY KEY", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT"]
searches_fields = ["id", "parameters", "urls"]
searches_datatypes = ["INTEGER PRIMARY KEY", "TEXT", "TEXT"]
all_fields = [dictionaries_fields, jobs_fields, searches_fields]
all_datatypes = [dictionaries_datatypes, jobs_datatypes, searches_datatypes]
for outer_index in range(0, len(all_databases)):
    for index in range(0, len(all_websites)):
        create_table(all_databases[outer_index], all_websites[index], all_fields[outer_index], all_datatypes[outer_index])

#############
# Glassdoor #
#############

##########
# Indeed #
##########

date_posted = {
    "Last 24 hours": "&fromage=1",
    "Last 3 days": "&fromage=3",
    "Last 7 days": "&fromage=7",
    "Last 14 days": "&fromage=14"
}
distance = {
    "Exact location only": "&radius=0",
    "Within 5 miles": "&radius=5",
    "Within 10 miles": "&radius=10",
    "Within 15 miles": "&radius=15",
    "Within 25 miles": "&radius=25",
    "Within 35 miles": "&radius=35",
    "Within 50 miles": "&radius=50",
    "Within 100 miles": "&radius=100"
}
indeed_dictionary_titles = ["date_posted", "distance"]
indeed_dictionaries = [date_posted, distance]
for index in range(0, len(indeed_dictionary_titles)):
    create_record("dictionaries", "indeed", ["parameter", "dictionary"], [f"'{indeed_dictionary_titles[index]}'", f"'{json.dumps(indeed_dictionaries[index])}'"])
# create_record("dictionaries", "indeed", ["parameter", "dictionary"], ['"distance"', f"'{json.dumps(distance)}'"])

############
# LinkedIn #
############

###########
# Monster #
###########

################
# Ziprecruiter #
################




#################
# Demonstration #
#################

print("##########")
for database in all_databases:
    for website in all_websites:
        print(read_fields(database, website))

print(read_all_records("dictionaries", "indeed"))
"""
new_date_posted = json.loads(read_record_field("dictionaries", "indeed", "parameter", '"date_posted"')[2])
new_distance = json.loads(read_record_field("dictionaries", "indeed", "parameter", '"distance"')[2])
print(new_date_posted["Last 7 days"])
print(new_distance["Within 50 miles"])
"""
