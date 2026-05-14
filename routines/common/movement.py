from widgets.geometry import Point
from widgets.player import Player
import widgets.serial_input as serial_input
import time
from config import JUMP_KEY, ROPE_LIFT_KEY


def turn_left():
    serial_input.key_down("left")
    time.sleep(0.05)
    serial_input.key_up("left")

    time.sleep(0.5)


def turn_right():
    serial_input.key_down("right")
    time.sleep(0.05)
    serial_input.key_up("right")

    time.sleep(0.5)


def rope_lift():
    serial_input.press("h")

    time.sleep(3)


def down_jump():
    serial_input.key_down("down")
    time.sleep(0.05)
    serial_input.key_down("v")
    time.sleep(0.05)
    serial_input.key_up("v")
    serial_input.key_up("down")

    time.sleep(0.5)


def get_walk_hold_time(distance) -> float:
    remaining_distance = abs(distance)

    # Serial input has command latency, so very short taps barely move the character.
    if remaining_distance >= 20:
        return 0.18
    if remaining_distance >= 12:
        return 0.12
    if remaining_distance >= 6:
        return 0.08
    return 0.05


def hold_key(key, hold_time) -> None:
    hold_ms = max(int(hold_time * 1000), 20)
    serial_input.hold(key, hold_ms)


def move_horizontal(direction_key: str, distance: int) -> None:
    if abs(distance) >= 30:
        # Swap this out for flash jump/teleport when available (import as map_routine.fast_move_left/right)
        hold_key(direction_key, get_walk_hold_time(distance))
    else:
        hold_key(direction_key, get_walk_hold_time(distance))

    # Delay for movement momentum
    time.sleep(0.05)


def move_vertical(direction_key: str) -> None:
    if direction_key == "up":
        serial_input.key_down(JUMP_KEY)
        # Delay to be in the air to reach the highest platform
        time.sleep(0.05)
        serial_input.press(ROPE_LIFT_KEY)
        serial_input.key_up(JUMP_KEY)
        # Delay for rope lift momentum
        time.sleep(1.1)
    else:
        serial_input.key_down("down")
        # Delay to slide down a rope, if there is one (assumption)
        time.sleep(0.4)
        serial_input.press(JUMP_KEY)
        serial_input.key_up("down")
        # Delay for air time momentum
        time.sleep(1.1)


def go_to(player: Player, target_point: Point, buffer_distance: float = 0) -> None:
    current_player_x = player.get_coordinates().x
    delta_x = target_point.x - current_player_x
    while abs(delta_x) > buffer_distance:
        direction = "right" if delta_x > 0 else "left"
        move_horizontal(direction, delta_x)
        current_player_x = player.get_coordinates().x
        delta_x = target_point.x - current_player_x

    current_player_y = player.get_coordinates().y
    delta_y = target_point.y - current_player_y
    # Add some wiggle room for vertical movement
    while abs(delta_y) > (buffer_distance + 5):
        direction = "up" if delta_y > 0 else "down"
        move_vertical(direction)
        current_player_y = player.get_coordinates().y
        delta_y = target_point.y - current_player_y
