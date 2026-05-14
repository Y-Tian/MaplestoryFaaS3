class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"
