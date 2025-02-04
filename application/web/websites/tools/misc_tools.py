import webbrowser
import time
import datetime
import pyperclip
import re

# Webbrowser:

def open_google_chrome():
    webbrowser.open('https://www.google.com/', new=1)

# Time:

def wait_seconds(input, print_statements=True):
    for index in range(0, input):
        if print_statements: print(index)
        time.sleep(1)

# Datetime:

def current_time():
    return datetime.datetime.now()

# Pyperclip:

def copy_to_clipboard(string):
    pyperclip.copy(string)

def paste_from_clipboard():
    return pyperclip.paste()

def wait_for_clipboard(timeout=5):
    pyperclip.waitForPaste(timeout)

def wait_for_copy(timeout=5):
    pyperclip.waitNewForPaste(timeout)

# Re:

def list_regex_coordinates(regex_pattern, searched_text):
        output = []
        for regex_match in re.finditer(regex_pattern, searched_text):
            output.append(regex_match.span())
        return output

def re_search(pattern, text):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return ""

# Simple Functions:

def prepare_urls(id_list, unformatted_url):
    output =[]
    for id in id_list:
        output.append(f"{unformatted_url.format(id)}\n\n")
    return output


# Complex Functions: