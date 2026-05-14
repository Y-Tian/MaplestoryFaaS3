from widgets.player import Player
from widgets.rune import Rune
from routines.common import movement
import win32gui
from config import ACTIVE_WINDOW_NAME
from PIL import ImageGrab, Image
from typing import List
import widgets.serial_input as serial_input
import time
import random
from widgets.logger import init_logger

log = init_logger(__name__)

def detect_rune_present(rune: Rune) -> bool:
    return rune.get_coordinates() is not None

def get_rune_screenshot() -> Image.Image | None:
    active_window = win32gui.FindWindow(None, ACTIVE_WINDOW_NAME)
    if active_window:
        window_rect = win32gui.GetWindowRect(active_window)
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = window_rect

        window_height = bottom_right_y - top_left_y
        window_width = bottom_right_x - top_left_x

        # Split window into thirds and use the middle third
        rune_section_top_left_x = (window_width / 3) + top_left_x
        rune_section_top_left_y = (window_height / 4) + top_left_y
        rune_section_bottom_right_x = (window_width / 3) + top_left_x
        rune_section_bottom_right_y = (window_height / 4) + top_left_y

        rune_screenshot = ImageGrab.grab(bbox=(
            rune_section_top_left_x,
            rune_section_top_left_y,
            rune_section_bottom_right_x,
            rune_section_bottom_right_y
        ))
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

            if 235 <= rgb_pixel[1] <= 255 and 0 < rgb_pixel[0] < 50 and rgb_pixel[2] < 200:
                for arrow in arrow_sequence:
                    if abs(arrow[1] - x) <= 25:
                        to_add = False
                if to_add:
                    direction = get_rune_arrow_direction(screenshot, x, y)
                    if direction:
                        arrow_sequence.append((direction, x))

    return sorted(arrow_sequence, key=get_arrow_sequence_key)

def solve(player: Player, rune: Rune):
    rune_coords = rune.get_coordinates()
    if not rune_coords:
        return
    movement.go_to(player, rune_coords, buffer_distance=1.5)

    rune_screenshot = get_rune_screenshot()
    if rune_screenshot:
        arrow_key_sequence = get_rune_arrow_sequence(rune_screenshot)
        if arrow_key_sequence == 4:
            for arrow_key in arrow_key_sequence:
                # Delay for input processing on the rune puzzle
                time.sleep(random.uniform(0.12, 0.22))
                serial_input.press(arrow_key[0])
        else:
            log.error(f"Expected 4 arrows for rune puzzle, but found {len(arrow_key_sequence)}. Sequence: {arrow_key_sequence}")
                
    # Reset the rune after the attempt (assume it succeeded)
    rune.set_coordinates(None)
    # Reset the player position after the attempt
    movement.go_to(player, player.get_start_coordinates(), buffer_distance=1)