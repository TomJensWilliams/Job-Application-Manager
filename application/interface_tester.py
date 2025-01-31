from interface_functions import *

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

def test_run_search():
    job_parameters = [
        {
            "job_title": "Help Desk",
            "job_location": "Liberty Lake, WA",
            "date_posted": "3",
            "search_radius": "50"
        }
    ]
    run_search("indeed", job_parameters)

def test_create_search():
    job_parameters = {
        "job_title": "Help Desk",
        "job_location": "Liberty Lake, WA",
        "date_posted": "3",
        "search_radius": "50"
    }
    create_search("indeed", job_parameters)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Run functions below: