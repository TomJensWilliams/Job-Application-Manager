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
dictionaries_fields = ["id", "parameter", "dictionary"]
dictionaries_datatypes = ["INTEGER", "TEXT", "TEXT"]
jobs_fields = ["id", "applied", "title", "company", "location", "address", "number", "email", "website", "date", "note"]
jobs_datatypes = ["TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT"]
searches_fields = ["id", "parameters", "urls"]
searches_datatypes = ["INTEGER", "TEXT", "TEXT"]
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