import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable
from pathlib import Path
import importlib
import importlib.util
import hashlib
import time
from widgets.geometry import Point
from widgets.minimap import Minimap
from helpers.image_loader import get_image_boundaries
from helpers.paths import runtime_path
from widgets.player import Player
from widgets.rune import Rune
from widgets.anchor import Anchor


class GUI:
    def __init__(
        self,
        title: str,
        minimap: Minimap,
        player: Player,
        rune: Rune,
        anchor: Anchor,
        start_controller: Callable[[], None],
        stop_controller: Callable[[], None],
        start_monitor: Callable[[], None],
        stop_monitor: Callable[[], None],
        geometry: str = "400x650",
    ):
        self.minimap = minimap
        self.player = player
        self.rune = rune
        self.anchor = anchor
        self._start_controller = start_controller
        self._stop_controller = stop_controller
        self._start_monitor = start_monitor
        self._stop_monitor = stop_monitor
        self._controller_running = False
        self._monitor_running = False
        self._loaded_routine_path: Path | None = None
        self._app_start_time = time.monotonic()

        self.root = tk.Tk()

        # This is the section of code which define the main window
        self.root.geometry(geometry)
        self.root.title(title)
        self.root.resizable(False, False)

        # create all of the main containers
        initFrame = tk.Frame(
            self.root, width=200, height=200, borderwidth=2, relief="groove"
        )
        liveFrame = tk.Frame(
            self.root, width=155, height=200, borderwidth=2, relief="groove"
        )

        # layout all of the main containers
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        initFrame.grid(row=0, column=0, sticky="W", padx=15, pady=15)
        liveFrame.grid(row=0, column=1, sticky="E", padx=15, pady=15)

        tk.Label(
            self.root,
            text="Initialize Settings",
            fg="#000000",
            font=("arial", 9, "bold"),
        ).grid(row=0, column=0, sticky="N", pady=20)
        tk.Button(
            self.root,
            text="Load Data",
            bg="#F0FFFF",
            font=("arial", 9, "normal"),
            command=self.initialize_settings,
        ).grid(row=0, column=0, sticky="S", pady=40)

        tk.Label(
            self.root, text="Minimap:", fg="#000000", font=("arial", 9, "normal")
        ).grid(row=0, column=0, sticky="NW", padx=25, pady=85)
        self.miniMapLabel = tk.Label(
            self.root, text="Waiting", fg="#f0ae13", font=("arial", 9, "normal")
        )
        self.miniMapLabel.grid(row=0, column=0, sticky="NE", padx=35, pady=85)

        tk.Label(
            self.root, text="Live Info", fg="#000000", font=("arial", 9, "bold")
        ).grid(row=0, column=1, sticky="N", pady=20)

        tk.Label(
            self.root, text="Player:", fg="#000000", font=("arial", 9, "normal")
        ).grid(row=0, column=1, sticky="NW", padx=25, pady=85)
        self.playerCoordinatesLabel = tk.Label(
            self.root, text="(null,null)", fg="#123fff", font=("arial", 9, "normal")
        )
        self.playerCoordinatesLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=85)

        tk.Label(
            self.root, text="Start:", fg="#000000", font=("arial", 9, "normal")
        ).grid(row=0, column=1, sticky="NW", padx=25, pady=110)
        self.startCoordinatesLabel = tk.Label(
            self.root, text="(null,null)", fg="#123fff", font=("arial", 9, "normal")
        )
        self.startCoordinatesLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=110)

        tk.Label(
            self.root, text="Rune:", fg="#000000", font=("arial", 9, "normal")
        ).grid(row=0, column=1, sticky="NW", padx=25, pady=135)
        self.runeCoordinatesLabel = tk.Label(
            self.root, text="(null,null)", fg="#123fff", font=("arial", 9, "normal")
        )
        self.runeCoordinatesLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=135)

        tk.Label(
            self.root, text="Time:", fg="#000000", font=("arial", 9, "normal")
        ).grid(row=0, column=1, sticky="NW", padx=25, pady=160)
        self.elapsedRuntimeLabel = tk.Label(
            self.root, text="00:00:00", fg="#123fff", font=("arial", 9, "normal")
        )
        self.elapsedRuntimeLabel.grid(row=0, column=1, sticky="NE", padx=35, pady=160)

        # Start Section
        self.loadFileButton = tk.Button(
            self.root,
            text="Load Routine File",
            bg="#F0FFFF",
            font=("arial", 12, "normal"),
            command=self.select_routine_file,
        )
        self.loadFileButton.grid(row=2, columnspan=2, sticky="S", pady=5)

        self.startMonitorButton = tk.Button(
            self.root,
            text="Start Monitor",
            bg="#F0FFFF",
            font=("arial", 12, "normal"),
            command=self.toggle_monitor,
        )
        self.startMonitorButton.grid(row=3, columnspan=2, sticky="S", pady=7)

        self.setupButton = tk.Button(
            self.root,
            text="Setup Routine",
            bg="#F0FFFF",
            font=("arial", 12, "normal"),
            command=self.run_loaded_routine_setup,
        )
        self.setupButton.grid(row=4, columnspan=2, sticky="S", pady=7)

        self.startControllerButton = tk.Button(
            self.root,
            text="Start Controller",
            bg="#F0FFFF",
            font=("arial", 12, "normal"),
            command=self.toggle_controller,
        )
        self.startControllerButton.grid(row=5, columnspan=2, sticky="S", pady=10)

        tk.Label(
            self.root, text="Status:", fg="#000000", font=("arial", 10, "normal")
        ).grid(row=6, column=0, sticky="SW", padx=10)
        self.botStatusLabel = tk.Label(
            self.root, text="Offline", fg="#FF0000", font=("arial", 10, "normal")
        )
        self.botStatusLabel.grid(row=6, column=0, sticky="SW", padx=55)
        self.root.after(500, self.refresh_live_info)

    def updateMinimapLabel(self):
        self.miniMapLabel["text"] = "Done"
        self.miniMapLabel["fg"] = "#0aad20"

    def updatePlayerCurrentCoordinates(self, point: Point | None):
        if point:
            self.playerCoordinatesLabel["text"] = f"({point.x}, {point.y})"
        else:
            self.runeCoordinatesLabel["text"] = "(null,null)"

    def updateStartCurrentCoordinates(self, point: Point):
        self.startCoordinatesLabel["text"] = f"({point.x}, {point.y})"

    def updateRuneCurrentCoordinates(self, point: Point | None):
        if point:
            self.runeCoordinatesLabel["text"] = f"({point.x}, {point.y})"
        else:
            self.runeCoordinatesLabel["text"] = "(null,null)"

    def refresh_live_info(self):
        self.updatePlayerCurrentCoordinates(self.player.get_coordinates())
        self.updateStartCurrentCoordinates(self.player.get_start_coordinates())
        self.updateRuneCurrentCoordinates(self.rune.get_coordinates())
        self.updateRuntimeLabel()
        self.root.after(500, self.refresh_live_info)

    def updateRuntimeLabel(self):
        elapsed_seconds = int(time.monotonic() - self._app_start_time)
        hours, remainder = divmod(elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.elapsedRuntimeLabel["text"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def updateBotStatus(self, is_running: bool):
        self._controller_running = is_running
        if is_running:
            self.botStatusLabel["text"] = "Online"
            self.botStatusLabel["fg"] = "#0aad20"
            self.startControllerButton["text"] = "Stop Controller"
        else:
            self.botStatusLabel["text"] = "Offline"
            self.botStatusLabel["fg"] = "#ff0000"
            self.startControllerButton["text"] = "Start Controller"

    def toggle_controller(self):
        if not self._loaded_routine_path:
            messagebox.showerror("No routine loaded", "Load a routine file first.")
            return

        if self._controller_running:
            self._stop_controller()
            self.updateBotStatus(False)
        else:
            self._start_controller()
            self.updateBotStatus(True)

    def toggle_monitor(self):
        if self._monitor_running:
            self._stop_monitor()
            self._monitor_running = False
            self.startMonitorButton["text"] = "Start Monitor"
        else:
            self._start_monitor()
            self._monitor_running = True
            self.startMonitorButton["text"] = "Stop Monitor"

    def initialize_settings(self):
        minimap_boundaries = get_image_boundaries()
        self.minimap.set_grid(minimap_boundaries)
        self.updateMinimapLabel()

    def _get_routines_dir(self) -> Path:
        return runtime_path("routines")

    def select_routine_file(self):
        routines_dir = self._get_routines_dir()
        selected_file = filedialog.askopenfilename(
            title="Select routine",
            initialdir=str(routines_dir),
            filetypes=[("Python files", "*.py")],
        )
        if not selected_file:
            return

        selected_path = Path(selected_file).resolve()
        if selected_path.suffix.lower() != ".py":
            messagebox.showerror("Invalid routine", "Select a Python file.")
            return

        self._loaded_routine_path = selected_path
        messagebox.showinfo("Routine loaded", f"Loaded: {selected_path.name}")

    def run_loaded_routine_setup(self):
        if not self._loaded_routine_path:
            messagebox.showerror("No routine loaded", "Load a routine file first.")
            return
        self.setup_routine(self._loaded_routine_path)

    def setup_routine(self, routine_path: Path):
        module_name = f"loaded_routine_{hashlib.sha1(str(routine_path).encode()).hexdigest()}"
        spec = importlib.util.spec_from_file_location(module_name, routine_path)
        if spec is None or spec.loader is None:
            messagebox.showerror(
                "Invalid routine", f"Could not load module from {routine_path}."
            )
            return

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        rotation_cls = getattr(module, "Rotation", None)
        if rotation_cls is None:
            messagebox.showerror(
                "Invalid routine", f"{routine_path.name} has no Rotation class."
            )
            return

        try:
            rotation = rotation_cls(self.player, self.anchor)
            setup_fn = getattr(rotation, "setup", None)
            if not callable(setup_fn):
                raise AttributeError("Rotation.setup is missing or not callable.")
            setup_fn()
        except Exception as exc:
            messagebox.showerror(
                "Setup failed", f"Failed while running setup():\n{exc}"
            )
