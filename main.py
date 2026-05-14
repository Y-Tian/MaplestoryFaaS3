from gui import GUI
from widgets.minimap import Minimap
from monitors.game import GameMonitor
import threading
from widgets.logger import init_logger
from typing import Dict, Any
from config import GUI_NAME

log = init_logger(__name__)

if __name__ == "__main__":
    minimap = Minimap([])
    game_monitor = GameMonitor(minimap)
    engine_state: Dict[str, Any] = {"thread": None}
    stop_event = threading.Event()

    def start_engine():
        log.info("Started")
        stop_event.clear()
        game_monitor_thread = threading.Thread(
            target=game_monitor.run,
            args=(stop_event,),
            daemon=True,
        )
        engine_state["thread"] = game_monitor_thread
        game_monitor_thread.start()

    def stop_engine():
        log.info("Stop requested")
        stop_event.set()

    gui = GUI(GUI_NAME, minimap, start_engine, stop_engine)
    try:
        gui.root.mainloop()
    finally:
        stop_engine()
