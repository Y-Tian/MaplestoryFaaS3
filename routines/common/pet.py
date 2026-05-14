import widgets.serial_input as serial_input
from config import PET_FOOD_KEY


def feed():
    # Press 3 times in case of network latency
    serial_input.press(PET_FOOD_KEY)
    serial_input.press(PET_FOOD_KEY)
    serial_input.press(PET_FOOD_KEY)
