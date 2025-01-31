import re
from web.tools.misc_tools import *
from web.tools.pyautogui_tools import *

def search(urls_list, browser_wait = 2, inspect_wait = 5):
    open_google_chrome()
    wait_seconds(browser_wait)
    html_content = get_all_html()
    close_window()
    for html in html_content:
        job_id_occurences = list_regex_coordinates(r'data-job-id="[^"]*"', html)
        expand_your_search = list_regex_coordinates(r'Expand your search', html)
        expand_start = expand_your_search[0][0] if len(expand_your_search) > 0 else len(html)
        job_id_list = []
        for job_id in job_id_occurences:
            if job_id[0] < expand_start:
                job_id_list.append(r'"([^"]*)"', html[job_id[0]: job_id[1]]).group(1)
            else:
                break
    return job_id_list

def process_jobs(jks):
    output = []
    open_google_chrome()
    wait_seconds(2)
    html_content = open_tabs_and_windows(jks, "https://www.linkedin.com/jobs/view/{}/\n\n")
    for index in range(0, len(jks)):
        job_applied = ""
        job_title = re_search(r'<h1 class="[^"]*">([^<]*)</h1>', html_content[index])
        job_company = re_search(r'<a class="[^"]*" target="[^"]*" href="[^"]*" data-test-app-aware-link="[^"]*"><!---->([^<]*)<!----></a>',html_content[index])
        job_location = re_search(r'<div class="t-black--light mt2" dir="ltr"><span class="tvm__text tvm__text--low-emphasis"><!---->([^<]*)<!----></span>', html_content[index])
        job_address = ""
        job_number = ""
        job_email = ""
        job_website = ""
        job_date = str(current_time())
        job_note = ""
        output.append([jks[index], job_applied, job_title, job_company, job_location, job_address, job_number, job_email, job_website, job_date, job_note])
    return output