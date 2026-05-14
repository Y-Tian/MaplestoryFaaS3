from widgets.minimap import Minimap
import threading
from widgets.logger import init_logger
from widgets.player import Player
from helpers.screenshot import get_screenshot
from helpers.image_compare import find_coordinates_by_template
from widgets.rune import Rune

log = init_logger(__name__)


class GameMonitor:
    def __init__(self, minimap: Minimap, player: Player, rune: Rune):
        self.minimap = minimap
        self.minimap_image = None
        self.player = player
        self.rune = rune

    def set_minimap_image(self) -> None:
        self.minimap_image = get_screenshot(self.minimap)

    def update_player_coordinates(self):
        if self.player.icon is None or self.minimap_image is None:
            return

        player_coord = find_coordinates_by_template(
            self.minimap_image, self.player.icon, self.player.icon_match_threshold
        )
        if player_coord:
            self.player.set_coordinates(player_coord)

    def update_rune_coordinates(self):
        if self.rune.icon is None or self.minimap_image is None:
            self.rune.set_coordinates(None)
            return

        rune_coord = find_coordinates_by_template(
            self.minimap_image, self.rune.icon, self.rune.icon_match_threshold
        )
        if rune_coord:
            if (
                rune_coord.x < 0
                or rune_coord.y < 0
                or rune_coord.x > self.minimap.get_grid()[1].x
                or rune_coord.y > self.minimap.get_grid()[1].y
            ):
                log.error(
                    f"Found rune coordinates {rune_coord} are out of bounds, ignoring."
                )
                self.rune.set_coordinates(None)
                return

            self.rune.set_coordinates(rune_coord)
        else:
            self.rune.set_coordinates(None)

    def run(self, stop_event: threading.Event):
        log.info("Thread started")
        while not stop_event.is_set():
            grid = self.minimap.get_grid()
            if grid:
                self.set_minimap_image()
                self.update_player_coordinates()
                self.update_rune_coordinates()

            # Yield CPU and check stop status regularly.
            stop_event.wait(0.1)

        log.info("Thread stopped")
