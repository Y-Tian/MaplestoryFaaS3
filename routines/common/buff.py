import widgets.serial_input as serial_input
from config import BUFF_SEQUENCE_KEY


def activate_sequence() -> None:
    # Press 2 times in case of network latency
    serial_input.press(BUFF_SEQUENCE_KEY)
    serial_input.press(BUFF_SEQUENCE_KEY)
