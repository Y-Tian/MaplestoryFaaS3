from widgets.minimap import Minimap

class GameMonitor:
    def __init__(self, minimap: Minimap):
        self.minimap = minimap

    def run(self):
        while True:
            if self.minimap.get_grid():
                print(self.minimap.get_grid())
