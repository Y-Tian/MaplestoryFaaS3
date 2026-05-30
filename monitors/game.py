from widgets.enemy import Enemy
from widgets.minimap import Minimap
import threading
import time
from widgets.logger import init_logger
from widgets.player import Player
from helpers.screenshot import get_screenshot
from helpers.image_compare import find_coordinates_by_template
from widgets.rune import Rune
from config import (
    ICON_COLOR_VALIDATION,
    RUNE_DETECTION_STABILITY_SECONDS,
    RUNE_MISS_GRACE_FRAMES,
)

log = init_logger(__name__)


class GameMonitor:
    def __init__(self, minimap: Minimap, player: Player, rune: Rune, enemy: Enemy):
        self.minimap = minimap
        self.minimap_image = None
        self.player = player
        self.rune = rune
        self.enemy = enemy
        self._rune_first_seen_at: float | None = None
        self._pending_rune_coord = None
        self._rune_miss_count = 0
        self._confirmed_rune_coord = None

    def _clear_rune_state(self) -> None:
        self._rune_first_seen_at = None
        self._pending_rune_coord = None
        self._rune_miss_count = 0
        self._confirmed_rune_coord = None
        self.rune.set_coordinates(None)

    def _publish_rune_coord(self, rune_coord) -> None:
        self._confirmed_rune_coord = rune_coord
        self.rune.set_coordinates(rune_coord)

    def set_minimap_image(self) -> None:
        self.minimap_image = get_screenshot(self.minimap.get_grid())

    def update_player_coordinates(self):
        if self.player.icon is None or self.minimap_image is None:
            return

        player_coord = find_coordinates_by_template(
            self.minimap_image,
            self.player.icon,
            self.player.icon_match_threshold,
            color_validation=ICON_COLOR_VALIDATION,
        )
        if player_coord:
            self.player.set_coordinates(player_coord)
        else:
            self.player.set_coordinates(None)

    def update_rune_coordinates(self):
        if self.rune.icon is None or self.minimap_image is None:
            self._clear_rune_state()
            return

        rune_coord = find_coordinates_by_template(
            self.minimap_image,
            self.rune.icon,
            self.rune.icon_match_threshold,
            color_validation=ICON_COLOR_VALIDATION,
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
                self._clear_rune_state()
                return

            now = time.monotonic()
            self._rune_miss_count = 0
            if self._rune_first_seen_at is None:
                self._rune_first_seen_at = now
            self._pending_rune_coord = rune_coord

            if now - self._rune_first_seen_at >= RUNE_DETECTION_STABILITY_SECONDS:
                self._publish_rune_coord(self._pending_rune_coord)
            elif self._confirmed_rune_coord is not None:
                # Keep the last confirmed rune alive while it is still being observed.
                self._publish_rune_coord(self._confirmed_rune_coord)
        else:
            if self._confirmed_rune_coord is not None:
                self._rune_miss_count += 1
                if self._rune_miss_count < RUNE_MISS_GRACE_FRAMES:
                    self.rune.set_coordinates(self._confirmed_rune_coord)
                    return

            self._clear_rune_state()

    def update_enemy_coordinates(self):
        if self.enemy.icon is None or self.minimap_image is None:
            return

        enemy_coord = find_coordinates_by_template(
            self.minimap_image,
            self.enemy.icon,
            self.enemy.icon_match_threshold,
            color_validation=ICON_COLOR_VALIDATION,
        )
        if enemy_coord:
            self.enemy.set_coordinates(enemy_coord)

    def run(self, stop_event: threading.Event):
        log.info("Thread started")
        while not stop_event.is_set():
            grid = self.minimap.get_grid()
            if grid:
                self.set_minimap_image()
                self.update_player_coordinates()
                self.update_rune_coordinates()
                self.update_enemy_coordinates()

            # Yield CPU and check stop status regularly.
            stop_event.wait(0.1)

        log.info("Thread stopped")
