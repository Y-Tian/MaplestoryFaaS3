from PIL import ImageGrab, Image
from widgets.minimap import Minimap

def get_screenshot(minimap: Minimap) -> Image.Image:
    screenshot = ImageGrab.grab(
        bbox=(
            minimap.grid[0].x,
            minimap.grid[0].y,
            minimap.grid[1].x,
            minimap.grid[1].y
        )
    )

    return screenshot