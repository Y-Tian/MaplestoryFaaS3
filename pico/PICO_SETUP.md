# Raspberry Pi Pico Keyboard Setup

## Overview
This project uses a Raspberry Pi Pico running CircuitPython as a USB HID keyboard. The same USB cable is used for:

- HID keyboard output back to the host PC
- serial command input from the host PC to the Pico

This replaces software-only input methods such as `pyautogui` or `pydirectinput`.

## Hardware Requirements
- Raspberry Pi Pico (RP2040)
- USB cable
- Windows PC or other host machine

No separate USB-to-UART adapter is required for the current setup.

## Files Used
- [`pico/boot.py`](boot.py)
- [`pico/code.py`](code.py)
- [`serial_input.py`](../serial_input.py)
- [`pico/tester.py`](tester.py)

## How It Works
`boot.py` configures the Pico USB interfaces during startup by enabling the standard USB CDC console and disabling the secondary CDC data channel.

In the current working setup:
- `usb_cdc.console` is enabled
- `usb_cdc.data` is disabled
- the Pico appears to the host as:
  - a USB keyboard
  - a single USB serial port

`code.py` runs the keyboard bridge:

- reads newline-terminated commands from the Pico USB serial console
- translates commands like `press:a` or `hold:right:750`
- sends the corresponding HID keyboard events back to the same host PC
- returns simple acknowledgements such as `pong`, `ready`, and `ok:press:a`

## Pico Setup

### 1. Install CircuitPython
1. Download CircuitPython for Raspberry Pi Pico from:
   https://circuitpython.org/board/raspberry_pi_pico/
2. Hold `BOOTSEL` while plugging in the Pico.
3. Drag the downloaded `.uf2` file onto the `RPI-RP2` drive.
4. After reboot, the Pico should appear as `CIRCUITPY`.

### 2. Install the HID Library
Download the CircuitPython library bundle or `adafruit-circuitpython-hid`, then copy the `adafruit_hid` folder onto the Pico here:

```text
CIRCUITPY/lib/adafruit_hid/
```

Important:
- the folder must be named `adafruit_hid`
- it must be inside `lib`
- do not use `libs`

### 3. Copy the Pico Files
Copy these files to the root of the Pico:

- copy [`pico/boot.py`](boot.py) to `CIRCUITPY/boot.py`
- copy [`pico/code.py`](code.py) to `CIRCUITPY/code.py`

Then unplug and replug the Pico.

`boot.py` only takes effect after reconnecting the board.

## Desktop Setup

### 1. Install Python Dependency
Install `pyserial` on the host machine:

```bash
py -m pip install pyserial
```

### 2. Identify the Pico COM Port
On Windows, the Pico should appear as a `USB Serial Device`, typically something like `COM3`.

To inspect ports:

```bash
py -m serial.tools.list_ports -v
```

## Testing

### Automatic Port Scan
Use the included test script to probe available COM ports:

```bash
py pico/tester.py --scan
```

Expected result for the Pico port:
- `ping: 'pong'`
- `status: 'ready'`

Example:

```text
Testing COM3 (USB Serial Device (COM3))
  ready: None
  ping: 'pong'
  status: 'ready'
```

### Keyboard Smoke Test
Once you know the correct port:

```bash
py pico/tester.py --port COM3
```

What the test does:
- opens the Pico serial bridge
- verifies the handshake with `ping` and `status`
- types `pico keyboard test 123`
- presses `Enter`
- holds `Right Arrow` for 750 ms

To observe the result:
1. open Notepad or another text field
2. focus that window
3. run the test

Expected behavior:
1. `pico keyboard test 123` is typed
2. a newline is inserted
3. the cursor moves right briefly

## Using It In Code
The project-side serial bridge is [`serial_input.py`](../serial_input.py).

Example:

```python
import serial_input

serial_input.press("a")
serial_input.hold("right", 300)
serial_input.close()
```

`serial_input.py` now:
- defaults to `COM3`
- supports `MAPLE_PICO_PORT` or `PICO_SERIAL_PORT`
- performs a handshake on connect
- can scan for the working Pico port if the configured port is wrong

## Command Protocol
Commands sent to the Pico are newline-terminated:

- `ping`
- `status`
- `press:{key}`
- `down:{key}`
- `up:{key}`
- `hold:{key}:{ms}`

Examples:

```text
press:a
press:space
down:left
up:left
hold:right:750
```

Responses from the Pico include:

- `pong`
- `ready`
- `ok:press:a`
- `ok:hold:right:750`
- `error:unknown_key:...`

## Supported Keys
The current firmware supports:

- `a-z`
- `0-9`
- `space`
- `enter`
- `esc`
- `tab`
- `backspace`
- `delete`
- `left`
- `right`
- `up`
- `down`
- `shift`
- `ctrl`
- `alt`
- `end`
- `home`
- `=`

## Troubleshooting

### The Pico Shows Up But Does Not Type
- Confirm `CIRCUITPY/boot.py` and `CIRCUITPY/code.py` were copied correctly
- Confirm `CIRCUITPY/lib/adafruit_hid/` exists
- Replug the Pico after changing `boot.py`
- Run `py pico/tester.py --scan` and verify one port returns `pong` and `ready`

### The Script Opens the Port But Nothing Happens
- Make sure the active text field is focused before running the test
- Confirm you are using the working COM port from `py pico/tester.py --scan`
- Close any serial monitor or REPL session that may already be using the Pico COM port

### The Pico Types Into the Wrong Window
- This setup sends real HID keyboard input to the current focused window
- Focus the target application before the bot sends commands

### `code.py` Crashes On Startup
- Re-copy the latest [`pico/code.py`](code.py) as `CIRCUITPY/code.py`
- If the board enters REPL immediately, open the serial console and inspect the traceback

### Port Number Changes
- Windows may assign a different COM port after reconnecting the Pico
- Re-run:

```bash
py pico/tester.py --scan
```

## Notes
- the working firmware uses the USB console CDC port as its command channel
- the Pico can both receive serial commands and send keyboard events to the same host PC over one USB cable
