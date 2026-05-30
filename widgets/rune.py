from helpers import paths
from widgets.geometry import Point
from PIL import Image
from config import RUNE_ICON_MATCH_THRESHOLD


class Rune:
    def __init__(self) -> None:
        self.coord = None
        self.icon = Image.open(paths.resource_path("resources/rune_icon.png"))
        self.icon_match_threshold = RUNE_ICON_MATCH_THRESHOLD

    def set_coordinates(self, point: Point | None) -> None:
        self.coord = point

    def get_coordinates(self) -> Point | None:
        return self.coord
