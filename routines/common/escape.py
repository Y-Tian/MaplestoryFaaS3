from widgets.geometry import Point
import widgets.serial_input as serial_input
from config import ACTIVE_WINDOW_NAME, TO_TOWN_KEY
import time
import os
import win32gui
from helpers.screenshot import get_screenshot, save_screenshot

def to_town() -> None:
    active_window = win32gui.FindWindow(None, ACTIVE_WINDOW_NAME)
    if active_window:
        window_rect = win32gui.GetWindowRect(active_window)
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = window_rect

        screenshot = get_screenshot([
            Point(top_left_x, top_left_y),
            Point(bottom_right_x, bottom_right_y)
        ])
        save_screenshot(screenshot, "backups/enemy", "detection")

    # Press 2 times in case of network latency
    serial_input.press(TO_TOWN_KEY)
    serial_input.press(TO_TOWN_KEY)
    time.sleep(1)
    serial_input.press("enter")
    os._exit(1)
