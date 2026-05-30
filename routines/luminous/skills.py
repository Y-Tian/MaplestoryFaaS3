import widgets.serial_input as serial_input
import time


def reflection() -> None:
    serial_input.press("c")

    time.sleep(0.5)

def tp_left_atk() -> None:
    serial_input.key_down("left")
    time.sleep(0.02)
    serial_input.key_down("c")
    time.sleep(0.07)
    serial_input.key_down("space")

    time.sleep(0.02)
    serial_input.key_up("space")
    time.sleep(0.02)
    serial_input.key_up("c")
    time.sleep(0.02)
    serial_input.key_up("left")

    time.sleep(0.5)

def tp_right_atk() -> None:
    serial_input.key_down("right")
    time.sleep(0.02)
    serial_input.key_down("c")
    time.sleep(0.07)
    serial_input.key_down("space")

    time.sleep(0.02)
    serial_input.key_up("space")
    time.sleep(0.02)
    serial_input.key_up("c")
    time.sleep(0.02)
    serial_input.key_up("right")

    time.sleep(0.5)