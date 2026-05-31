from widgets.geometry import Point
from widgets.player import Player
import widgets.serial_input as serial_input
import time
from config import JUMP_KEY, ROPE_LIFT_KEY
import routines.common.skills as common_skills 


def turn_left() -> None:
    serial_input.key_down("left")
    time.sleep(0.05)
    serial_input.key_up("left")

    time.sleep(0.5)


def turn_right() -> None:
    serial_input.key_down("right")
    time.sleep(0.05)
    serial_input.key_up("right")

    time.sleep(0.5)


def rope_lift() -> None:
    serial_input.press(ROPE_LIFT_KEY)

    time.sleep(3)


def down_jump() -> None:
    serial_input.key_down("down")
    time.sleep(0.05)
    serial_input.key_down("v")
    time.sleep(0.05)
    serial_input.key_up("v")
    serial_input.key_up("down")

    time.sleep(0.5)


def get_walk_hold_time(distance: int) -> float:
    remaining_distance = abs(distance)

    # Serial input has command latency, so very short taps barely move the character.
    if remaining_distance >= 20:
        return 0.18
    if remaining_distance >= 12:
        return 0.12
    if remaining_distance >= 6:
        return 0.08
    return 0.05


def hold_key(key: str, hold_time: float) -> None:
    hold_ms = max(int(hold_time * 1000), 20)
    serial_input.hold(key, hold_ms)


def move_horizontal(direction_key: str, distance: int) -> None:
    if abs(distance) >= 30:
        if direction_key == "left":
            # common_skills.flash_jump_left()
            common_skills.tp_left()
        else:
            # common_skills.flash_jump_right()
            common_skills.tp_right()
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
        time.sleep(1.5)
    else:
        serial_input.key_down("down")
        # Delay to slide down a rope, if there is one (assumption)
        time.sleep(0.4)
        serial_input.press(JUMP_KEY)
        serial_input.key_up("down")
        # Delay for air time momentum
        time.sleep(1.1)


def get_horizontal_jitter_distance(buffer_distance: float) -> int:
    # Keep the probe small so we can search for a better ledge/rope position
    # without drifting far outside the original target window.
    return max(1, min(2, int(buffer_distance) if buffer_distance >= 1 else 1))


def get_horizontal_jitter_direction(
    delta_x: int, jitter_flip: bool
) -> tuple[str, bool]:
    base_direction = "right" if delta_x >= 0 else "left"
    alternate_direction = "left" if base_direction == "right" else "right"

    # Alternate sides so the bot can probe for the ledge/rope angle that works.
    return (
        (alternate_direction if jitter_flip else base_direction),
        not jitter_flip,
    )


def go_to(player: Player, target_point: Point, buffer_distance: float = 0) -> None:
    player_coords = player.get_coordinates()
    if not player_coords:
        return

    current_player_x = player_coords.x
    delta_x = target_point.x - current_player_x
    while abs(delta_x) > buffer_distance:
        direction = "right" if delta_x > 0 else "left"
        move_horizontal(direction, delta_x)
        player_coords = player.get_coordinates()
        if not player_coords:
            return
        current_player_x = player_coords.x
        delta_x = target_point.x - current_player_x

    current_player_y = player_coords.y
    delta_y = target_point.y - current_player_y
    vertical_stall_attempts = 0
    jitter_flip = False
    # Add some wiggle room for vertical movement
    while abs(delta_y) > (buffer_distance + 5):
        previous_player_y = current_player_y
        direction = "down" if delta_y > 0 else "up"
        move_vertical(direction)
        player_coords = player.get_coordinates()
        if not player_coords:
            return
        current_player_y = player_coords.y
        delta_y = target_point.y - current_player_y

        if current_player_y == previous_player_y:
            vertical_stall_attempts += 1
        else:
            vertical_stall_attempts = 0

        if vertical_stall_attempts >= 3:
            jitter_direction, jitter_flip = get_horizontal_jitter_direction(
                delta_x, jitter_flip
            )
            move_horizontal(
                jitter_direction, get_horizontal_jitter_distance(buffer_distance)
            )
            player_coords = player.get_coordinates()
            if not player_coords:
                return
            current_player_x = player_coords.x
            delta_x = target_point.x - current_player_x
            vertical_stall_attempts = 0
