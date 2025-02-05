import json
import sys
if "/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager/application" in sys.path:
    sys.path[sys.path.index("/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager/application")] = "/home/tom/Desktop/GithubFolder/Public/Job-Application-Manager"
from application.interface_functions import *

# EXPLINATION OF THE PURPOSE OF THISE FILE

def main(*, print_statements=False):
    all_databases = ["dictionaries", "jobs", "searches"]
    all_websites = ["glassdoor", "indeed", "linkedin", "monster", "ziprecruiter"]

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

main()