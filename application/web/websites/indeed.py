import re
from web.websites.tools.misc_tools import *
from web.websites.tools.pyautogui_tools import *

def job_ids_from_html(html_content, /, *, print_statements=False):
    output = []
    for html in html_content:
        jk_occurances = list_regex_coordinates(r'data-jk="[^"]*"', html)
        header_occurances = list_regex_coordinates(r'class="jobSection-header-text"', html)
        header_start = header_occurances[0][0] if len(header_occurances) > 0 else len(html)
        for jk in jk_occurances:
            if jk[0] < header_start:
                output.append(re.search(r'"([^"]*)"', html[jk[0]:jk[1]]).group(1))
            else:
                break
    return output

def job_base_url(*, print_statements=False):
    return "https://www.indeed.com/viewjob?jk={}"

def prepare_job_data(new_ids, job_fields, html_content):
    output = []
    for index in range(0, len(new_ids)):
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
        output.append([new_ids[index], job_applied, job_title, job_company, job_location, job_address, job_number, job_email, job_website, job_date, job_note])
    return output