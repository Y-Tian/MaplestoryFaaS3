from widgets.geometry import Point
from widgets.player import Player
from widgets.rune import Rune
from routines.common import movement
import win32gui
from config import ACTIVE_WINDOW_NAME, FMA_KEY, RUNE_KEY
from PIL import Image
from typing import List
import widgets.serial_input as serial_input
import time
import random
from widgets.logger import init_logger
from config import CASH_SHOP_KEY
from helpers.screenshot import get_screenshot, save_screenshot

log = init_logger(__name__)


def detect_rune_present(rune: Rune) -> bool:
    return rune.get_coordinates() is not None


def is_in_range(
    target_x: float, target_y: float, player_coords: Point, wanted_range: float
) -> bool:
    x_range = abs(target_x - player_coords.x)
    y_range = abs(target_y - player_coords.y)
    return x_range < wanted_range and y_range < wanted_range


def get_rune_screenshot() -> Image.Image | None:
    active_window = win32gui.FindWindow(None, ACTIVE_WINDOW_NAME)
    if active_window:
        window_rect = win32gui.GetWindowRect(active_window)
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = window_rect

        window_height = bottom_right_y - top_left_y
        window_width = bottom_right_x - top_left_x

        # Capture the center third (x-axis) and middle half (y-axis) of the game window
        rune_section_top_left_x = int(top_left_x + (window_width / 3))
        rune_section_top_left_y = int(top_left_y + (window_height / 4))
        rune_section_bottom_right_x = int(rune_section_top_left_x + (window_width / 3))
        rune_section_bottom_right_y = int(rune_section_top_left_y + (window_height / 4))

        rune_screenshot = get_screenshot(
            [
                Point(rune_section_top_left_x, rune_section_top_left_y),
                Point(rune_section_bottom_right_x, rune_section_bottom_right_y),
            ]
        )

        save_screenshot(rune_screenshot, "backups/rune")

        return rune_screenshot

    return None


def get_rune_arrow_direction(screenshot: Image.Image, x: int, y: int) -> str | None:
    max_x, max_y = screenshot.size

    for i in range(1, 20, 1):
        if x + i < max_x:
            right_pixel = screenshot.getpixel((x + i, y))
            if right_pixel[1] == 255 and 150 < right_pixel[0] < 230:
                return "right"

        left_pixel = screenshot.getpixel((x - i, y))
        if left_pixel[1] == 255 and 150 < left_pixel[0] < 230:
            return "left"

        up_pixel = screenshot.getpixel((x, y - i))
        if up_pixel[1] == 255 and 150 < up_pixel[0] < 230:
            return "up"

        if y + i < max_y:
            down_pixel = screenshot.getpixel((x, y + i))
            if down_pixel[1] == 255 and 150 < down_pixel[0] < 230:
                return "down"
    return None


def get_arrow_sequence_key(arrows_key: tuple) -> int:
    return arrows_key[1]


def get_rune_arrow_sequence(screenshot: Image.Image) -> List[str]:
    width, height = screenshot.size
    arrow_sequence = []

    for x in range(width):
        for y in range(height):
            to_add = True
            rgb_pixel = screenshot.getpixel((x, y))

            # grabs the green pixels from the rune arrows
            if (
                235 <= rgb_pixel[1] <= 255
                and 0 < rgb_pixel[0] < 50
                and rgb_pixel[2] < 200
            ):
                for arrow in arrow_sequence:
                    if abs(arrow[1] - x) <= 25:
                        to_add = False
                if to_add:
                    direction = get_rune_arrow_direction(screenshot, x, y)
                    if direction:
                        arrow_sequence.append((direction, x))

    return sorted(arrow_sequence, key=get_arrow_sequence_key)


def hard_reset_rune_spinning_arrows() -> None:
    time.sleep(0.5)
    serial_input.press(CASH_SHOP_KEY)
    time.sleep(12)
    serial_input.press("esc")
    time.sleep(1)
    serial_input.press("enter")
    time.sleep(7)


def solve(player: Player, rune: Rune) -> bool:
    rune_coords = rune.get_coordinates()
    if not rune_coords:
        return False
    movement.go_to(player, rune_coords, buffer_distance=1.5)

    # Double check that we are next to the rune as we need to stand next to it
    player_coords = player.get_coordinates()
    if not is_in_range(rune_coords.x, rune_coords.y, player_coords, wanted_range=4):
        movement.go_to(player, rune_coords, buffer_distance=2)

    # Clear monsters nearby before attempting to solve
    serial_input.press(FMA_KEY)
    # Delay for general FMA animation
    time.sleep(1.2)
    serial_input.press(RUNE_KEY)
    # Delay for rune puzzle opening animation
    time.sleep(0.8)

    solve_success = False
    rune_screenshot = get_rune_screenshot()
    if rune_screenshot:
        arrow_key_sequence = get_rune_arrow_sequence(rune_screenshot)
        if len(arrow_key_sequence) == 4:
            for arrow_key in arrow_key_sequence:
                # Delay for input processing on the rune puzzle
                time.sleep(random.uniform(0.12, 0.22))
                serial_input.press(arrow_key[0])
            solve_success = True
        else:
            log.error(
                f"Expected 4 arrows for rune puzzle, but found {len(arrow_key_sequence)}. Sequence: {arrow_key_sequence}"
            )

    # Reset the rune after the attempt (assume it succeeded)
    rune.set_coordinates(None)
    # Reset the player position after the attempt
    movement.go_to(player, player.get_start_coordinates(), buffer_distance=1)
    return solve_success
