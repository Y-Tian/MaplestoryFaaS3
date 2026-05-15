from datetime import datetime
from pathlib import Path
import win32gui
from PIL import ImageGrab, Image
from config import ACTIVE_WINDOW_NAME
from widgets.geometry import Point
from typing import List


def get_active_window() -> List[Point]:
    active_window = win32gui.FindWindow(None, ACTIVE_WINDOW_NAME)
    window_rect = win32gui.GetWindowRect(active_window)
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = window_rect
    return [Point(top_left_x, top_left_y), Point(bottom_right_x, bottom_right_y)]


def get_screenshot(matrix: List[Point]) -> Image.Image:
    screenshot = ImageGrab.grab(
        bbox=(
            matrix[0].x,
            matrix[0].y,
            matrix[1].x,
            matrix[1].y,
        )
    )

    return screenshot


def save_screenshot(
    screenshot: Image.Image, folder: str, filename: str = "detection"
) -> None:
    screenshot.save(
        f"{Path(folder)}/{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )
