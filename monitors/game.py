from widgets.minimap import Minimap
import threading
from widgets.logger import init_logger

log = init_logger(__name__)

class GameMonitor:
    def __init__(self, minimap: Minimap):
        self.minimap = minimap

    def run(self, stop_event: threading.Event):
        log.info("Thread started")
        while not stop_event.is_set():
            grid = self.minimap.get_grid()
            if grid:
                log.info(f"Current minimap grid: {grid}")

            # Yield CPU and check stop status regularly.
            stop_event.wait(0.1)

        log.info("Thread stopped")
