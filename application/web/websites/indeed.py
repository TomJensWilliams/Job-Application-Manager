import re
from application.web.websites.tools.misc_tools import *
from application.web.websites.tools.pyautogui_tools import *

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

def process_search_parameters(table, parameters, print_statements=False):
    parameters_sets = []
    all_keys = [parameter["key"] for parameter in parameters]
    for parameter_title in [element for element in ["search_title", "search_location"] if element not in all_keys]:
        parameters.append({"key": parameter_title, "values": ["placeholder"]})
    # if not "search_title" in all_keys:
    #     parameters.append({"key": "search_title", "values": ["placeholder"]})
    # elif not "search_location" in all_keys:
    #     parameters.append({"key": "search_location", "values": ["placeholder"]})

    largest_index = max([len(parameter) for parameter in parameters])
    # largest_index = 0
    # for parameter in parameters:
    #     if len(parameter["values"]) > largest_index:
    #         largest_index = len(parameter["values"])
    for index in range(0, largest_index):
        current_parameters = {}
        for parameter in parameters:
            if index < len(parameter["values"]):
                print(parameter)
                # current_parameters[parameter["key"]] = parameter["values"][index]
                current_parameters[parameter["key"]] = parameter["values"][index]
            else:
                print(parameter)
                # current_parameters[parameter["key"]] = parameter["values"][len(parameter["values"]) - 1]
                current_parameters[parameter["key"]] = parameter["values"][len(parameter["values"]) - 1]
        parameters_sets.append(current_parameters)
    open_google_chrome()
    wait_seconds(2)
    open_url("https://www.indeed.com#\b\n\n", 0.1)
    wait_seconds(3)
    urls = []
    searches = []
    first_time = True
    for parameters_set in parameters_sets:
        if not first_time:
            move_mouse_to(((magnifying_glass_element[0] + pin_element[0]) / 2), (magnifying_glass_element[1] + (magnifying_glass_element[3] / 2)), 0.5)
            wait_seconds(1)
            other_little_x_element = wait_for_locate("indeed_other_little_x.png")
            move_mouse_to((other_little_x_element[0] + (0.25 * other_little_x_element[2])), (other_little_x_element[1] + (0.5 * other_little_x_element[3])), 0.25)
            mouse_left_click()
        first_time = False
        magnifying_glass_element = wait_for_locate_multiple(["indeed_magnifying_glass.png", "indeed_magnifying_glass_blue.png"], 0.8)
        pin_element = wait_for_locate("indeed_pin.png")
        search_element = wait_for_locate("indeed_search.png")
        move_mouse_to(((magnifying_glass_element[0] + pin_element[0]) / 2), (magnifying_glass_element[1] + (magnifying_glass_element[3] / 2)), 0.5)
        mouse_left_click()
        type_string(f"{parameters_set['search_title']}", 0.01)
        move_mouse_to(((pin_element[0] + search_element[0]) / 2), (pin_element[1] + (pin_element[3] / 2)), 0.5)
        little_x_element = wait_for_locate("indeed_little_x.png")
        move_mouse_to(*center_of_image(little_x_element), 0.5)
        mouse_left_click()
        move_mouse_to(((pin_element[0] + search_element[0]) / 2), (pin_element[1] + (pin_element[3] / 2)), 0.5)
        mouse_left_click()
        type_string(f"{parameters_set['search_location']}", 0.01)
        move_mouse_to(*center_of_image(search_element), 0.5)
        mouse_left_click()
        wait_seconds(2)
        press_hotkey(["ctrl", "l"])
        press_hotkey(["ctrl", "c"])
        urls.append(paste_from_clipboard())
        searches.append({"search_title": parameters_set["search_title"], "search_location": [parameters_set["search_location"]]})
    output = []
    for parameter in parameters:
        if not parameter["values"][0] == "placeholder":
            current_object = {"key": parameter["key"], "dictionary": {}}
            for index in range(0, len(urls)):
                if not searches[index][parameter["key"]] in current_object["dictionary"].keys():
                    urls[index] += "&" # This cheating might come back to bite me
                    if parameter["key"] == "search_title":
                        regex_pattern = r"(\?q=[^&]*)"
                    elif parameter["key"] == "search_location":
                        regex_pattern = r"(&l=[^&]*)"
                    match_value = re_search(regex_pattern, urls[index])
                    current_object["dictionary"][searches[index][parameter["key"]]] = match_value
            output.append(current_object)
    return output    

def search_base_url(*, print_statements=False):
    return "https://www.indeed.com/jobs"