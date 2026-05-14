from widgets.geometry import Point


class Anchor:
    def __init__(self) -> None:
        self.coord = Point()

    def set_coordinates(self, point: Point) -> None:
        self.coord = point

    def get_coordinates(self) -> Point:
        return self.coord
