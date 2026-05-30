import threading
from widgets.enemy import Enemy
from widgets.logger import init_logger
from widgets.player import Player
from widgets.rune import Rune
from routines.common import rune
from widgets.anchor import Anchor
from routines.luminous.end_of_the_world_1_7 import Rotation
import time
from routines.common import escape

log = init_logger(__name__)


class PrimaryController:
    def __init__(
        self, player: Player, rune: Rune, enemy: Enemy, anchor: Anchor
    ) -> None:
        self.player = player
        self.rune = rune
        self.enemy = enemy
        self.anchor = anchor
        self._consecutive_rune_failures = 0

    def escape_whiteroom_if_present(self):
        if self.player.get_coordinates():
            return

        log.info("Player coordinates not detected, escaping potential whiteroom...")
        escape.whiteroom()

    def solve_rune_until_solved(self, stop_event: threading.Event):
        if not rune.detect_rune_present(self.rune):
            return

        log.info("Rune detected, prioritizing solve attempts...")
        while not stop_event.is_set() and rune.detect_rune_present(self.rune):
            solved = rune.solve(self.player, self.rune)
            if solved:
                self._consecutive_rune_failures = 0
                log.info("Rune solve input sequence sent successfully.")
                return

            self._consecutive_rune_failures += 1
            log.warning(
                "Rune solve failed (%s/3 consecutive failures)",
                self._consecutive_rune_failures,
            )
            if self._consecutive_rune_failures >= 3:
                log.warning(
                    "Rune solve failed 3 times in a row. Running hard rune reset."
                )
                rune.hard_reset_rune_spinning_arrows()
                self._consecutive_rune_failures = 0

            # Brief yield before the next retry to avoid tight retry loops.
            stop_event.wait(0.1)

    def escape_enemy_if_present(self):
        if self.enemy.get_coordinates():
            return

        log.info("Enemy detected, escaping...")
        escape.to_town()

    def check_defaults(self, stop_event: threading.Event):
        self.escape_whiteroom_if_present()
        self.solve_rune_until_solved(stop_event)
        self.escape_enemy_if_present()

    def run(self, stop_event: threading.Event):
        # Delay for user to switch to the game window after starting the thread
        time.sleep(3)
        log.info("Thread started")
        routine = Rotation(self.player, self.anchor)
        while not stop_event.is_set():
            # Invoke a known set of routines in sequence
            self.check_defaults(stop_event)

            """
            Add routine phase 1 below
            """

            routine.mobbing_cycle()

            """
            Add routine phase 1 above
            """

            self.check_defaults(stop_event)

            """
            Add routine phase 2 below
            """

            routine.loot_cycle()

            """
            Add routine phase 2 above
            """

            # Yield CPU and check stop status regularly.
            stop_event.wait(0.1)

        log.info("Thread stopped")
