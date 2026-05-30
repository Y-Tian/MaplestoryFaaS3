import widgets.serial_input as serial_input
import time


def flash_jump_left() -> None:
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


def flash_jump_right() -> None:
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

def tp_right() -> None:
    serial_input.key_down("right")
    time.sleep(0.02)
    serial_input.key_down("space")
    time.sleep(0.02)
    serial_input.key_up("space")
    time.sleep(0.02)
    serial_input.key_up("right")

    time.sleep(0.5)

def tp_left() -> None:
    serial_input.key_down("left")
    time.sleep(0.02)
    serial_input.key_down("space")
    time.sleep(0.02)
    serial_input.key_up("space")
    time.sleep(0.02)
    serial_input.key_up("left")

    time.sleep(0.5)

def tp_up() -> None:
    serial_input.key_down("v")
    time.sleep(0.1)
    serial_input.key_down("up")
    time.sleep(0.02)
    serial_input.key_down("space")
    time.sleep(0.1)
    serial_input.key_up("space")
    time.sleep(0.02)
    serial_input.key_up("up")
    time.sleep(0.02)
    serial_input.key_up("v")

    time.sleep(0.5)

def tp_down() -> None:
    serial_input.key_down("down")
    time.sleep(0.02)
    serial_input.key_down("space")
    time.sleep(0.1)
    serial_input.key_up("space")
    time.sleep(0.02)
    serial_input.key_up("down")

    time.sleep(0.5)

def set_erda_fountain() -> None:
    serial_input.key_down("shift")
    time.sleep(0.05)
    serial_input.key_down("z")
    time.sleep(0.07)
    serial_input.key_up("z")
    serial_input.key_up("shift")

    time.sleep(0.5)


def activate_loot_sequence() -> None:
    serial_input.key_down("end")
    time.sleep(1)
    serial_input.key_up("end")

    time.sleep(0.5)
