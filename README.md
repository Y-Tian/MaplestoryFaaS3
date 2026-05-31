# MaplestoryFaaS3

A Python desktop automation project for MapleStory with a Tkinter control panel, image-based game state monitoring, and pluggable routines.

## What it does

- Tracks live minimap entities (player, rune, enemy) from screenshots.
- Runs a routine controller loop independently from the monitor loop.
- Supports loading a routine module dynamically from `routines/` and running its `setup()`.
- Includes rune solving logic with safety fallbacks (including hard reset after repeated failures).

## Project structure

- `main.py`: app entrypoint, thread lifecycle wiring.
- `gui.py`: Tkinter UI and control buttons.
- `monitors/game.py`: monitor loop (screenshot + template matching updates).
- `controllers/primary.py`: primary routine loop.
- `routines/`: class/routine implementations.
- `routines/common/`: shared movement/skills/rune logic.
- `routines/bowmaster/`: example job-specific routine.
- `helpers/`: screenshot and image matching utilities.
- `widgets/`: state objects and IO helpers.
- `config.py`: thresholds, window name, keys, serial config.
- `pico/`: Raspberry Pi Pico firmware notes/scripts for serial key input.

## Requirements

- Python 3.10+
- Windows (uses `pywin32` window APIs)
- MapleStory running with window title matching `ACTIVE_WINDOW_NAME` in `config.py`
- Optional: Raspberry Pi Pico serial device if using hardware key injection

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` before running:

- `ACTIVE_WINDOW_NAME`: target game window title
- Match thresholds:
- `PLAYER_ICON_MATCH_THRESHOLD`
- `RUNE_ICON_MATCH_THRESHOLD`
- `ENEMY_ICON_MATCH_THRESHOLD`
- Serial settings:
- `DEFAULT_PORT`
- `DEFAULT_BAUDRATE`
- Key bindings:
- `FMA_KEY`, `RUNE_KEY`, `CASH_SHOP_KEY`, etc.

## Run

```bash
python main.py
```

## GUI workflow

Recommended order:

1. Click `Load Data` to set minimap boundaries.
2. Click `Load Routine File` and select a module from `routines/`.
3. Click `Start Monitor` to begin live minimap detection updates.
4. Click `Setup Routine` to run selected routine's `Rotation(...).setup()`.
5. Click `Start Controller` to run the primary routine loop.

Controls are split intentionally:

- `Start/Stop Monitor`: only controls `GameMonitor` thread.
- `Start/Stop Controller`: only controls `PrimaryController` thread.

## Routine module contract

A loadable routine file should expose a `Rotation` class with compatible constructor/signatures used by `gui.py` and `controllers/primary.py`.

Current expectations:

- Constructor compatible with `Rotation(player, anchor)`
- Optional setup method used by GUI:
- `setup()`
- Runtime methods used by controller:
- `mobbing_cycle()`
- `loot_cycle()`

## Rune behavior

- Rune coordinates are only published after stable detections over a time window in `monitors/game.py`.
- If rune solving fails repeatedly, `controllers/primary.py` triggers `hard_reset_rune_spinning_arrows()` after 3 consecutive failed attempts.

## Troubleshooting

- No detections:
- verify `Load Data` was run and minimap region is correct.
- tune thresholds in `config.py`.
- verify icons in `resources/` match in-game visuals.
- Serial key input not working:
- check `DEFAULT_PORT`, baudrate, and Pico firmware setup in `pico/PICO_SETUP.md`.
- Routine load errors:
- ensure selected file is inside `routines/` and defines `Rotation`.

## Development notes

- Screenshot backups for rune attempts are saved under `backups/`.
- Logging output helps track monitor/controller thread status and rune solving decisions.

## Building a Windows EXE

Use the included PyInstaller spec:

```bash
py -m PyInstaller --clean --noconfirm BacklitManager.spec
```

The packaged build outputs `dist/BacklitManager/BacklitManager.exe`.

Runtime notes for the packaged build:

- bundled assets are resolved from the PyInstaller extraction directory
- screenshots and recovery images are written next to the executable in `backup/`
- `MAPLE_PICO_PORT` still applies