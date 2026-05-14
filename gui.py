import tkinter as tk
from widgets.geometry import Point

class GUI:
    def __init__(self, title: str, geometry: str="400x400"):
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
            # command=handler.initButtonClick,
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
            # command=handler.startButtonClick,
        )
        self.startButton.grid(row=4, columnspan=2, sticky="S", pady=10)

        tk.Label(self.root, text="Status:", fg="#000000", font=("arial", 10, "normal")).grid(
            row=5, column=0, sticky="SW", padx=10
        )
        self.botStatusLabel = tk.Label(
            self.root, text="Offline", fg="#FF0000", font=("arial", 10, "normal")
        )
        self.botStatusLabel.grid(row=5, column=0, sticky="SW", padx=55)

    def updateMiniMapLabel(self, error: str = ""):
        if error is not None:
            self.miniMapLabel["text"] = error
            self.miniMapLabel["fg"] = "#c70c0c"
        else:
            self.miniMapLabel["text"] = "Done"
            self.miniMapLabel["fg"] = "#0aad20"


    def updateCurrentCoordinate(self, point: Point):
        self.coordinatesLabel["text"] = f"({point.x}, {point.y})"


    def updateBotStatus(self, is_running: bool):
        if is_running:
            self.botStatusLabel["text"] = "Online"
            self.botStatusLabel["fg"] = "#0aad20"
            self.startButton["text"] = "Stop Engine"
        else:
            self.botStatusLabel["text"] = "Offline"
            self.botStatusLabel["fg"] = "#ff0000"
            self.startButton["text"] = "Start Engine"
