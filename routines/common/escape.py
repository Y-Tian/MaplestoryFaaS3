import widgets.serial_input as serial_input
from config import TO_TOWN_KEY
import time
import os

def to_town() -> None:
    # Press 3 times in case of network latency
    serial_input.press(TO_TOWN_KEY)
    serial_input.press(TO_TOWN_KEY)
    time.sleep(1)
    serial_input.press("enter")
    os._exit(1)
