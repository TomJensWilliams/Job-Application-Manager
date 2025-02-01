import re
from web.tools.misc_tools import *
from web.tools.pyautogui_tools import *

def search(urls_list, browser_wait = 2, inspect_wait = 5):
    open_google_chrome()
    wait_seconds(browser_wait)
    html_content = get_all_html()
    close_window()
    for html in html_content:
        jk_occurances = list_regex_coordinates(r'data-jk="[^"]*"', html)
        header_occurances = list_regex_coordinates(r'class="jobSection-header-text"', html)
        header_start = header_occurances[0][0] if len(header_occurances) > 0 else len(html)
        jk_list = []
        for jk in jk_occurances:
            if jk[0] < header_start:
                jk_list.append(re.search(r'"([^"]*)"', html[jk[0]:jk[1]]).group(1))
            else:
                break
    return jk_list

def process_jobs(jks):
    output = []
    open_google_chrome()
    wait_seconds(2)
    html_content = open_tabs_and_windows(jks, "https://www.indeed.com/viewjob?jk={}\n\n")
    for index in range(0, len(jks)):
        job_applied = ""
        job_title = re_search(r'<h2 data-testid="simpler-jobTitle" class="[^"]*">([^<]*)</h2>', html_content[index])
        job_company = re_search(r'<a target="_blank" href="[^"]*" class="jobsearch-JobInfoHeader-companyNameLink [^"]*" elementtiming="significant-render">([^<]*)<svg xmlns=',html_content[index])
        job_location = re_search(r'<div data-testid="jobsearch-JobInfoHeader-companyLocation" class="[^"]*"><div class="[^"]*">([^<]*)</div></div>', html_content[index])
        job_address = ""
        job_number = ""
        job_email = ""
        job_website = ""
        job_date = str(current_time())
        job_note = ""
        output.append([jks[index], job_applied, job_title, job_company, job_location, job_address, job_number, job_email, job_website, job_date, job_note])
    return output

def prepare_search_dictionary(key, values):
    pass