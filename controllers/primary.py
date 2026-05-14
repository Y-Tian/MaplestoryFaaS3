import threading
from widgets.logger import init_logger
from widgets.player import Player
from widgets.rune import Rune
from routines.common import rune

log = init_logger(__name__)


class PrimaryController:
    def __init__(self, player: Player, rune: Rune) -> None:
        self.player = player
        self.rune = rune

    def run(self, stop_event: threading.Event):
        log.info("Thread started")
        while not stop_event.is_set():
            # Invoke a known set of routines in sequence
            if rune.detect_rune_present(self.rune):
                log.info("Rune detected, solving...")
                rune.solve(self.player, self.rune)

            """
            Add routine phase 1 below
            """

            """
            Add routine phase 1 above
            """

            if rune.detect_rune_present(self.rune):
                log.info("Rune detected, solving...")
                rune.solve(self.player, self.rune)

            """
            Add routine phase 2 below
            """

            """
            Add routine phase 2 above
            """

            # Yield CPU and check stop status regularly.
            stop_event.wait(0.1)

        log.info("Thread stopped")
