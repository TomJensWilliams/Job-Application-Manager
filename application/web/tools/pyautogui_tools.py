import pyautogui
import pyscreeze
import time
from web.tools.misc_tools import *

#########
# NOTES #
#########

# >>> pyautogui.click('button.png') # Find where button.png appears on the screen and click it.

# >>> pyautogui.PAUSE = 2.5

# >>> pyautogui.mouseDown(x=moveToX, y=moveToY, button='left')
# >>> pyautogui.mouseUp(x=moveToX, y=moveToY, button='left')



# Mouse Control Functions:

def get_screen_size():
    return pyautogui.size()

def get_mouse_position():
    return pyautogui.position()

def coordinates_on_screen(input):
    return pyautogui.onScreen(input)

def move_mouse_to(x_coordinate, y_coordinate, interval=0):
    # None in either coordinate can be used for no change.
    pyautogui.moveTo(x_coordinate, y_coordinate, interval)

def move_mouse_by(x_travel, y_travel, interval=0):
    # None in either coordinate can be used for no change.
    pyautogui.move(x_travel, y_travel, interval)

def drag_mouse_to():
    # TODO
    pass

def drag_mouse_by():
    # TODO
    pass

# TWEENING

def mouse_left_click():
    pyautogui.click(button='left')

def mouse_middle_click():
    # TODO
    pass

def mouse_right_click():
    pyautogui.click(button='right')

def hold_left_click():
    # TODO
    pass

def unhold_left_click():
    # TODO
    pass

def hold_right_click():
    # TODO
    pass

def unhold_right_click():
    # TODO
    pass

def vertical_mouse_scroll():
    # TODO
    pass


def horizontal_mouse_scroll():
    # TODO
    pass

# Keyboard Control Functions (Potentially Complete):

def type_string(string, interval=0):
    # A list of key names can be passed too
    pyautogui.write(string, interval)

def press_key(input, presses=1):
    pyautogui.press(input, presses)

def hold_key(input):
    pyautogui.keyDown(input)

def unhold_key(input):
    pyautogui.keyUp(input)

def with_hold_do(held_key, instructions):
    with pyautogui.hold(held_key):
        instructions()

def press_hotkey(input):
    pyautogui.hotkey(input)


# Message Box Functions:

def alert_message(text='', title='', button='OK'):
    return pyautogui.alert(text, title, button)

def confirm_message(text='', title='', buttons=['OK', 'Cancel']):
    return pyautogui.confirm(text, title, buttons)

def prompt_message(text='', title='', default=''):
    return pyautogui.prompt(text, title, default)

def password_message(text='', title='', default='', mask='*'):
    return pyautogui.password(text, title, default, mask)

# Screenshot Functions:

def take_screenshot(region=None, filename=None):
    return pyautogui.screenshot(region, filename)

def locate_on_screen(filename, confidence=0.9):
    try:
        return pyautogui.locateOnScreen(f"./web/pictures/{filename}", confidence=confidence)
    except pyscreeze.ImageNotFoundException:
        return []
    except pyautogui.ImageNotFoundException:
        return []

def center_of_image(image):
    return pyautogui.center(image)

def click_image_center(filename, confidence=0.9):
    # TODO
    pass

def center_on_screen(filename, confidence=0.9):
    # TODO
    pass


def all_on_screen(filename, confindence=0.9):
    # TODO
    pass

def locate_needle_haystack(needleFilename, imageFilename, grayscale=False):
    # TODO
    pass


def all_needle_haystack():
    # TODO
    pass

def check_a_pixel():
    # TODO
    pass

def get_a_pixel():
    # TODO
    pass

def pixel_matches_color():
    # TODO
    pass

# Simple Functions:

def open_url(input, interval=0):
    press_hotkey(['ctrl', 'l'])
    type_string(input, interval)

def open_window():
    press_hotkey(['ctrl', 'n'])

def close_window():
    press_hotkey(['ctrl', 'shift', 'w'])

def open_tab():
    press_hotkey(['ctrl', 't'])

def close_tab():
    press_hotkey(['ctrl', 'w'])

# Complex Functions:

def wait_for_locate(filename, confidence=0.9, waittime=50):
    counter = 0
    output = locate_on_screen(filename, confidence)
    while len(output) == 0 and counter < waittime:
        output = locate_on_screen(filename, confidence)
        counter += 1
        time.sleep(0.1)
    if counter >= waittime:
        raise pyscreeze.ImageNotFoundException('')
    return output

def get_all_html(urls_list, inspect_wait):
    output = []
    for url in urls_list:
        open_url(url)
        for x in range(0, inspect_wait):
            print(x)
            wait_seconds(1)
        output.append(get_html())
    return

def get_html():
    press_hotkey(['ctrl', 'shift', 'i'])
    body_element = wait_for_locate('body_tag.png', 0.8)
    move_mouse_to(*center_of_image(body_element), 0.5)
    mouse_right_click()
    copy_tab = wait_for_locate('copy.png', 0.8)
    move_mouse_to(center_of_image(copy_tab)[0], None, 0.25)
    move_mouse_to(*center_of_image(copy_tab), 0.25)
    copy_element = wait_for_locate('copy_element.png', 0.8)
    move_mouse_to(*center_of_image(copy_element), 0.5)
    mouse_left_click()
    html_content = paste_from_clipboard()
    press_hotkey(['ctrl', 'shift', 'j'])
    return html_content

def open_tabs_and_windows(id_list, unformatted_url):
    output = []
    current_tabs = 1
    last_was_tabs = True
    url_list = prepare_urls(id_list, unformatted_url)
    for url in url_list:
        open_url(url)
        for x in range(0, 5):
            print(x)
            wait_seconds(1)
        output.append(get_html())
        if current_tabs == 10:
            open_window()
            last_was_tabs = False
            current_tabs = 1
        else:
            open_tab()
            last_was_tabs = True
            current_tabs += 1
    if last_was_tabs:
        close_tab()
    else:
        close_window()
    return output