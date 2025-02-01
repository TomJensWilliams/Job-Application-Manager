from interface_functions import *

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

parameters = [
    {
        "search_title": ["Help Desk", "Desktop Support"],
        "search_location": ["Post Falls, ID", "Liberty, Lake"],
        "date_posted": ["Last 3 days"],
        "distance": ["Within 50 miles"]
    },
]

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Run functions below:

# print_table("dictionaries", "indeed", "test")

process_create_search("indeed", parameters)