import threading
from widgets.logger import init_logger
from widgets.player import Player
from widgets.rune import Rune
from routines.common import rune
from widgets.anchor import Anchor
from routines.bowmaster.hidden_illyard_field import Rotation

log = init_logger(__name__)


class PrimaryController:
    def __init__(self, player: Player, rune: Rune, anchor: Anchor) -> None:
        self.player = player
        self.rune = rune
        self.anchor = anchor

    def run(self, stop_event: threading.Event):
        log.info("Thread started")
        routine = Rotation(self.player, self.anchor)
        while not stop_event.is_set():
            # Invoke a known set of routines in sequence
            if rune.detect_rune_present(self.rune):
                log.info("Rune detected, solving...")
                rune.solve(self.player, self.rune)

            """
            Add routine phase 1 below
            """

            routine.mobbing_cycle()

            """
            Add routine phase 1 above
            """

            if rune.detect_rune_present(self.rune):
                log.info("Rune detected, solving...")
                rune.solve(self.player, self.rune)

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
