import widgets.serial_input as serial_input
import time


def flash_jump_left():
    serial_input.key_down("left")
    serial_input.key_down("v")
    time.sleep(0.05)
    serial_input.key_up("v")

    time.sleep(0.07)
    serial_input.key_down("v")
    time.sleep(0.05)
    serial_input.key_up("v")
    serial_input.key_up("left")

    time.sleep(1)


def flash_jump_right():
    serial_input.key_down("right")
    serial_input.key_down("v")
    time.sleep(0.05)
    serial_input.key_up("v")

    time.sleep(0.07)
    serial_input.key_down("v")
    time.sleep(0.05)
    serial_input.key_up("v")
    serial_input.key_up("right")

    time.sleep(1)


def set_erda_fountain():
    serial_input.key_down("down")
    time.sleep(0.05)
    serial_input.key_down("z")
    time.sleep(0.07)
    serial_input.key_up("z")
    serial_input.key_up("down")

    time.sleep(0.5)


def activate_loot_sequence():
    serial_input.key_down("end")
    time.sleep(1)
    serial_input.key_up("end")

    time.sleep(0.5)
