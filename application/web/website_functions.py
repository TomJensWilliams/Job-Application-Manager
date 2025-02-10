import re
from application.web.websites.tools.misc_tools import *
from application.web.websites.tools.pyautogui_tools import *
from application.web.websites import glassdoor
from application.web.websites import indeed
from application.web.websites import linkedin
from application.web.websites import monster
from application.web.websites import ziprecruiter

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
    base_url = get_website_functions(website).job_base_url()
    html_content = open_urls_and_get_html(new_ids, base_url, inspect_wait)
    return get_website_functions(website).prepare_job_data(new_ids, job_fields, html_content)

def process_search_parameters(table, parameters, /, *, print_statements=False):
    return get_website_functions(table).process_search_parameters(table, parameters, print_statements=print_statements)

def get_base_url(website):
    return get_website_functions(website).search_base_url()