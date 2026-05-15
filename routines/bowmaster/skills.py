import widgets.serial_input as serial_input
import time


def swift_surge() -> None:
    serial_input.key_down("j")
    time.sleep(0.05)
    serial_input.key_up("j")

    time.sleep(0.6)


def swift_surge_left() -> None:
    serial_input.key_down("left")
    serial_input.press("j")
    time.sleep(0.1)
    serial_input.key_up("left")

    time.sleep(1)


def swift_surge_right() -> None:
    serial_input.key_down("right")
    serial_input.press("j")
    time.sleep(0.1)
    serial_input.key_up("right")

    time.sleep(1)


def arrow_stream() -> None:
    serial_input.press("c")

    time.sleep(0.5)


def gritty_gust() -> None:
    serial_input.key_down("r")

    time.sleep(0.5)


def use_blink_shot_portal() -> None:
    serial_input.key_down("d")
    time.sleep(0.1)
    serial_input.key_up("d")

    time.sleep(0.5)


def set_blink_shot_portal(initial = False) -> None:
    if initial:
        use_blink_shot_portal()
    else:
        serial_input.key_down("down")
        time.sleep(0.1)
        serial_input.key_down("d")
        serial_input.key_up("d")
        serial_input.key_up("down")

        time.sleep(0.5)


def jumping_hurricane_left_right(duration: float) -> None:
    serial_input.key_down("x")
    serial_input.key_down("x")

    while time.time() < duration:
        time.sleep(0.07)
        serial_input.key_down("v")
        time.sleep(0.07)
        serial_input.key_down("left")
        serial_input.key_up("left")
        serial_input.key_up("v")

        time.sleep(0.07)
        serial_input.key_down("v")
        time.sleep(0.07)
        serial_input.key_down("right")
        serial_input.key_up("right")
        serial_input.key_up("v")

    serial_input.key_up("x")

    time.sleep(0.5)


def set_arrow_blaster() -> None:
    serial_input.key_down("u")
    time.sleep(0.05)
    serial_input.press("y")
    time.sleep(0.07)
    serial_input.key_up("y")
    serial_input.key_up("u")

    time.sleep(0.5)


def fj_left_atk() -> None:
    serial_input.key_down("left")
    serial_input.key_down("v")
    time.sleep(0.02)
    serial_input.key_up("v")

    time.sleep(0.01)
    serial_input.key_down("v")
    serial_input.key_down("c")
    time.sleep(0.05)
    serial_input.key_up("c")
    serial_input.key_up("v")

    serial_input.key_up("left")

    time.sleep(1)


def fj_right_atk() -> None:
    serial_input.key_down("right")
    serial_input.key_down("v")
    time.sleep(0.02)
    serial_input.key_up("v")

    time.sleep(0.01)
    serial_input.key_down("v")
    serial_input.key_down("c")
    time.sleep(0.05)
    serial_input.key_up("c")
    serial_input.key_up("v")

    serial_input.key_up("right")

    time.sleep(1)


def jump_covering_fire() -> None:
    serial_input.key_down("v")
    time.sleep(0.07)
    serial_input.key_down("space")
    time.sleep(0.05)
    serial_input.key_up("space")
    serial_input.key_up("v")

    time.sleep(0.5)


def covering_fire() -> None:
    serial_input.key_down("space")
    time.sleep(0.05)
    serial_input.key_up("space")

    time.sleep(1.5)
