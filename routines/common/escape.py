from widgets.geometry import Point
import widgets.serial_input as serial_input
from config import TO_TOWN_KEY
import time
import os
from helpers.screenshot import get_active_window, get_screenshot, save_screenshot


def to_town() -> None:
    active_window = get_active_window()
    screenshot = get_screenshot(
        [
            Point(active_window[0].x, active_window[0].y),
            Point(active_window[1].x, active_window[1].y),
        ]
    )
    save_screenshot(screenshot, "backups/enemy")

    # Press 2 times in case of network latency
    serial_input.press(TO_TOWN_KEY)
    serial_input.press(TO_TOWN_KEY)
    time.sleep(1)
    serial_input.press("enter")
    os._exit(1)


def whiteroom() -> None:
    active_window = get_active_window()
    screenshot = get_screenshot(
        [
            Point(active_window[0].x, active_window[0].y),
            Point(active_window[1].x, active_window[1].y),
        ]
    )
    save_screenshot(screenshot, "backups/whiteroom")

    os._exit(1)
