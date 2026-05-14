from gui import GUI
from widgets.minimap import Minimap
from monitors.game import GameMonitor
from controllers.primary import PrimaryController
import threading
from widgets.logger import init_logger
from typing import Dict, Any
from config import GUI_NAME
from widgets.player import Player
from widgets.rune import Rune
from widgets.anchor import Anchor

log = init_logger(__name__)

if __name__ == "__main__":
    minimap = Minimap([])
    player = Player()
    rune = Rune()
    anchor = Anchor()

    game_monitor = GameMonitor(minimap, player, rune)
    primary_controller = PrimaryController(player, rune, anchor)
    monitor_state: Dict[str, Any] = {"thread": None, "stop_event": threading.Event()}
    controller_state: Dict[str, Any] = {"thread": None, "stop_event": threading.Event()}

    def start_monitor():
        monitor_thread = monitor_state["thread"]
        if monitor_thread and monitor_thread.is_alive():
            log.info("Game monitor already running")
            return

        log.info("Starting game monitor")
        monitor_state["stop_event"].clear()
        game_monitor_thread = threading.Thread(
            target=game_monitor.run,
            args=(monitor_state["stop_event"],),
            daemon=True,
        )
        monitor_state["thread"] = game_monitor_thread
        game_monitor_thread.start()

    def stop_monitor():
        log.info("Game monitor stop requested")
        monitor_state["stop_event"].set()

    def start_controller():
        controller_thread = controller_state["thread"]
        if controller_thread and controller_thread.is_alive():
            log.info("Primary controller already running")
            return

        log.info("Starting primary controller")
        controller_state["stop_event"].clear()
        primary_controller_thread = threading.Thread(
            target=primary_controller.run,
            args=(controller_state["stop_event"],),
            daemon=True,
        )
        controller_state["thread"] = primary_controller_thread
        primary_controller_thread.start()

    def stop_controller():
        log.info("Primary controller stop requested")
        controller_state["stop_event"].set()

    gui = GUI(
        GUI_NAME,
        minimap,
        player,
        rune,
        anchor,
        start_controller,
        stop_controller,
        start_monitor,
        stop_monitor,
    )
    try:
        gui.root.mainloop()
    finally:
        stop_controller()
        stop_monitor()
