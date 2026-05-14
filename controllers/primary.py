import threading
from widgets.logger import init_logger
from widgets.player import Player
from widgets.rune import Rune
from routines.common import buff, pet, rune 

log = init_logger(__name__)

class PrimaryController:
    def __init__(self, player: Player, rune: Rune) -> None:
        self.player = player
        self.rune = rune

    def run(self, stop_event: threading.Event):
        log.info("Thread started")
        while not stop_event.is_set():
            # Invoke a known set of routines in sequence
            buff.activate_sequence()
            pet.feed()

            # Yield CPU and check stop status regularly.
            stop_event.wait(0.1)

        log.info("Thread stopped")