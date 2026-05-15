from datetime import datetime
from pathlib import Path

from PIL import ImageGrab, Image
from widgets.geometry import Point
from typing import List


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

def save_screenshot(screenshot: Image.Image, folder: str, filename: str) -> None:
    screenshot.save(f"{Path(folder)}/{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
