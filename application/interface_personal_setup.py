import json
from interface_functions import *

print_statements = False

# EXPLINATION OF THE PURPOSE OF THIS FILE

#############
# Glassdoor #
#############

##########
# Indeed #
##########

search_title = {
    "Help Desk": "?q=Help+Desk",
    "Desktop Support": "?q=Desktop+Support",
    "IT Field Technician": "?q=it+field+technician"
}
search_location = {
    "Coeur d'Alene, ID": "&l=Coeur+d%27Alene%2C+ID",
    "Post Falls, ID": "&l=Post+Falls%2C+ID",
    "Liberty Lake, WA": "&l=Liberty+Lake%2C+WA",
    "Spokane, WA": "&l=Spokane%2C+WA"
}
indeed_dictionary_titles = ["search_title", "search_location"]
indeed_dictionaries = [search_title, search_location]
for index in range(0, len(indeed_dictionary_titles)):
    create_record("dictionaries", "indeed", ["parameter", "dictionary"], [indeed_dictionary_titles[index], indeed_dictionaries[index]], print_statements=print_statements)

first_search = {
    "search_title": ["Help Desk", "Desktop Support", "IT Field Technician"],
    "search_location": ["Coeur d'Alene, ID", "Post Falls, ID", "Liberty Lake, WA", "Spokane, WA"],
    "date_posted": ["Last 14 days"],
    "distance": ["Within 50 miles"]
}
prepare_search("indeed", first_search, print_statements=print_statements)

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