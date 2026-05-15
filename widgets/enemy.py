from widgets.geometry import Point
from PIL import Image
from config import ENEMY_ICON_MATCH_THRESHOLD


class Enemy:
    def __init__(self) -> None:
        self.coord = Point()
        self.icon = Image.open("resources/enemy_icon.png")
        self.icon_match_threshold = ENEMY_ICON_MATCH_THRESHOLD

    def set_coordinates(self, point: Point) -> None:
        self.coord = point

    def get_coordinates(self) -> Point:
        return self.coord
