import tkinter as tk
from typing import Callable
from widgets.geometry import Point
from widgets.minimap import Minimap
from helpers.image_loader import get_image_boundaries
from widgets.player import Player

class GUI:
    def __init__(
        self,
        title: str,
        minimap: Minimap,
        player: Player,
        start_engine: Callable[[], None],
        stop_engine: Callable[[], None],
        geometry: str = "400x400",
    ):
        self.minimap = minimap
        self._start_engine = start_engine
        self._stop_engine = stop_engine
        self._engine_running = False

        self.root = tk.Tk()

        # This is the section of code which define the main window
        self.root.geometry(geometry)
        self.root.title(title)
        self.root.resizable(False, False)

        # create all of the main containers
        initFrame = tk.Frame(self.root, width=200, height=200, borderwidth=2, relief="groove")
        liveFrame = tk.Frame(self.root, width=155, height=200, borderwidth=2, relief="groove")

        # layout all of the main containers
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        initFrame.grid(row=0, column=0, sticky="W", padx=15, pady=15)
        liveFrame.grid(row=0, column=1, sticky="E", padx=15, pady=15)

        tk.Label(
            self.root, text="Initialize Settings", fg="#000000", font=("arial", 9, "bold")
        ).grid(row=0, column=0, sticky="N", pady=20)
        tk.Button(
            self.root,
            text="Load Data",
            bg="#F0FFFF",
            font=("arial", 9, "normal"),
            command=self.initialize_settings,
        ).grid(row=0, column=0, sticky="S", pady=40)


        tk.Label(
            self.root, text="Minimap Position:", fg="#000000", font=("arial", 9, "normal")
        ).grid(row=0, column=0, sticky="NW", padx=25, pady=85)
        self.miniMapLabel = tk.Label(self.root, text="Waiting", fg="#f0ae13", font=("arial", 9, "normal"))
        self.miniMapLabel.grid(row=0, column=0, sticky="NE", padx=35, pady=85)

        tk.Label(self.root, text="Live Info", fg="#000000", font=("arial", 9, "bold")).grid(
            row=0, column=1, sticky="N", pady=20
        )

        tk.Label(self.root, text="Coordinates:", fg="#000000", font=("arial", 9, "normal")).grid(
            row=0, column=1, sticky="NW", padx=25, pady=85
        )
        self.coordinatesLabel = tk.Label(
            self.root, text="(null,null)", fg="#123fff", font=("arial", 9, "normal")
        )
        self.coordinatesLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=85)

        tk.Label(self.root, text="Elapsed:", fg="#000000", font=("arial", 9, "normal")).grid(
            row=0, column=1, sticky="NW", padx=25, pady=110
        )
        self.elapsedRuntimeLabel = tk.Label(
            self.root, text="00:00:00", fg="#123fff", font=("arial", 9, "normal")
        )
        self.elapsedRuntimeLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=110)

        # Start Section
        self.startButton = tk.Button(
            self.root,
            text="Start Engine",
            bg="#F0FFFF",
            font=("arial", 12, "normal"),
            command=self.toggle_engine,
        )
        self.startButton.grid(row=4, columnspan=2, sticky="S", pady=10)

        tk.Label(self.root, text="Status:", fg="#000000", font=("arial", 10, "normal")).grid(
            row=5, column=0, sticky="SW", padx=10
        )
        self.botStatusLabel = tk.Label(
            self.root, text="Offline", fg="#FF0000", font=("arial", 10, "normal")
        )
        self.botStatusLabel.grid(row=5, column=0, sticky="SW", padx=55)

    def updateMinimapLabel(self):
        self.miniMapLabel["text"] = "Done"
        self.miniMapLabel["fg"] = "#0aad20"

    def updateCurrentCoordinate(self, point: Point):
        self.coordinatesLabel["text"] = f"({point.x}, {point.y})"

    def updateBotStatus(self, is_running: bool):
        self._engine_running = is_running
        if is_running:
            self.botStatusLabel["text"] = "Online"
            self.botStatusLabel["fg"] = "#0aad20"
            self.startButton["text"] = "Stop Engine"
        else:
            self.botStatusLabel["text"] = "Offline"
            self.botStatusLabel["fg"] = "#ff0000"
            self.startButton["text"] = "Start Engine"

    def toggle_engine(self):
        if self._engine_running:
            self._stop_engine()
            self.updateBotStatus(False)
        else:
            self._start_engine()
            self.updateBotStatus(True)

    def initialize_settings(self):
        minimap_boundaries = get_image_boundaries()
        self.minimap.set_grid(minimap_boundaries)
        self.updateMinimapLabel()
