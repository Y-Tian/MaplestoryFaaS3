from gui import GUI
from widgets.minimap import Minimap
from monitors.game import GameMonitor
import threading

if __name__ == "__main__":
    minimap = Minimap([])
    game_monitor = GameMonitor(minimap)
    monitor_thread = threading.Thread(target=game_monitor.run, daemon=True)

    monitor_thread.start()

    gui = GUI("BacklitManager", minimap)
    gui.root.mainloop()
