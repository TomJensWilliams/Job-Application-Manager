import re
from web.websites.tools.misc_tools import *
from web.websites.tools.pyautogui_tools import *
from web.websites import glassdoor
from web.websites import indeed
from web.websites import linkedin
from web.websites import monster
from web.websites import ziprecruiter

def get_website_functions(website):
    if website == "glassdoor":
        return glassdoor
    elif website == "indeed":
        return indeed
    elif website == "linkedin":
        return linkedin
    elif website == "monster":
        return monster
    elif website == "ziprecruiter":
        return ziprecruiter

def retrieve_job_ids(website, url_list, /, *, browser_wait=2, inspect_wait=5, print_statements=False):
    open_google_chrome()
    wait_seconds(browser_wait)
    html_content = get_all_html(url_list, inspect_wait)
    close_window()
    return get_website_functions(website).job_ids_from_html(html_content, print_statements=print_statements)

def process_job_ids(website, new_ids, job_fields, /, *, broswer_wait=2, inspect_wait=5, print_statements=False):
    open_google_chrome()
    wait_seconds(broswer_wait)
    website_functions = get_website_functions(website)
    base_url = website_functions.job_base_url()
    html_content = open_tabs_and_windows(new_ids, base_url, inspect_wait)
    return website_functions.prepare_job_data(new_ids, job_fields, html_content)

def process_search_parameters(table, parameters, /, *, print_statements=False):
    pass

def get_base_url(table):
    pass