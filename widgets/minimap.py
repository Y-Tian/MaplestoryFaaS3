from typing import List

from widgets.geometry import Point

class Minimap:
    def __init__(self, grid: List[Point]) -> None:
        self.grid = grid

    def set_grid(self, grid: List[Point]) -> None:
        self.grid = grid

    def get_grid(self) -> List[Point]:
        return self.grid