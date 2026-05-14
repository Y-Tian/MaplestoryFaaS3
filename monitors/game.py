from widgets.minimap import Minimap
import threading
from widgets.logger import init_logger
from widgets.player import Player
from helpers.screenshot import get_screenshot
from helpers.image_compare import find_coordinates_by_template

log = init_logger(__name__)

class GameMonitor:
    def __init__(self, minimap: Minimap, player: Player):
        self.minimap = minimap
        self.minimap_image = None
        self.player = player

    def set_minimap_image(self) -> None:
        self.minimap_image = get_screenshot(self.minimap)

    def update_player_coordinates(self):
        if self.player.icon is None or self.minimap_image is None:
            return

        player_coord = find_coordinates_by_template(self.minimap_image, self.player.icon, self.player.icon_match_threshold)
        if player_coord:
            self.player.set_coordinates(player_coord)

    def run(self, stop_event: threading.Event):
        log.info("Thread started")
        while not stop_event.is_set():
            grid = self.minimap.get_grid()
            if grid:
                self.set_minimap_image()
                self.update_player_coordinates()

            # Yield CPU and check stop status regularly.
            stop_event.wait(0.1)

        log.info("Thread stopped")
