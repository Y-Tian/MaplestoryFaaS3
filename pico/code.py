"""
Pico firmware for USB HID keyboard emulation over a single USB cable.

The Pico appears to the host computer as both:
1. A USB keyboard for HID output
2. A USB CDC serial device for receiving commands

Commands (newline-terminated):
  - press:{key}          - Press and release key immediately
  - down:{key}           - Press key (hold down)
  - up:{key}             - Release key
  - hold:{key}:{ms}      - Hold key for milliseconds

Key names (standard): left, right, up, down, space, enter, esc, a-z, etc.
"""

import random

import usb_cdc
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

# USB keyboard setup
kbd = Keyboard(usb_hid.devices)

# Use the standard console CDC serial port for host commands.
serial_port = usb_cdc.console

# Mapping of string key names to HID keycodes
KEY_MAP = {
    "a": Keycode.A,
    "b": Keycode.B,
    "c": Keycode.C,
    "d": Keycode.D,
    "e": Keycode.E,
    "f": Keycode.F,
    "g": Keycode.G,
    "h": Keycode.H,
    "i": Keycode.I,
    "j": Keycode.J,
    "k": Keycode.K,
    "l": Keycode.L,
    "m": Keycode.M,
    "n": Keycode.N,
    "o": Keycode.O,
    "p": Keycode.P,
    "q": Keycode.Q,
    "r": Keycode.R,
    "s": Keycode.S,
    "t": Keycode.T,
    "u": Keycode.U,
    "v": Keycode.V,
    "w": Keycode.W,
    "x": Keycode.X,
    "y": Keycode.Y,
    "z": Keycode.Z,
    "0": Keycode.ZERO,
    "1": Keycode.ONE,
    "2": Keycode.TWO,
    "3": Keycode.THREE,
    "4": Keycode.FOUR,
    "5": Keycode.FIVE,
    "6": Keycode.SIX,
    "7": Keycode.SEVEN,
    "8": Keycode.EIGHT,
    "9": Keycode.NINE,
    "space": Keycode.SPACE,
    "enter": Keycode.ENTER,
    "esc": Keycode.ESCAPE,
    "escape": Keycode.ESCAPE,
    "tab": Keycode.TAB,
    "backspace": Keycode.BACKSPACE,
    "del": Keycode.DELETE,
    "delete": Keycode.DELETE,
    "=": Keycode.EQUALS,
    "left": Keycode.LEFT_ARROW,
    "right": Keycode.RIGHT_ARROW,
    "up": Keycode.UP_ARROW,
    "down": Keycode.DOWN_ARROW,
    "shift": Keycode.SHIFT,
    "ctrl": Keycode.CONTROL,
    "alt": Keycode.ALT,
    "end": Keycode.END,
    "home": Keycode.HOME,
}

# Track currently held keys
held_keys = set()


def send_response(message):
    if serial_port is None:
        return

    try:
        serial_port.write(f"{message}\n".encode("utf-8"))
    except OSError:
        pass


def get_keycode(key_name):
    """Convert string key name to HID keycode."""
    key_name = key_name.lower().strip()
    return KEY_MAP.get(key_name)


def process_command(cmd):
    """Process a serial command."""
    global held_keys

    cmd = cmd.strip()
    if not cmd:
        return

    try:
        if cmd == "ping":
            send_response("pong")
            return

        if cmd == "status":
            send_response("ready")
            return

        if cmd.startswith("press:"):
            key_name = cmd[6:]
            keycode = get_keycode(key_name)
            if keycode:
                kbd.press(keycode)
                kbd.release(keycode)
                send_response(f"ok:press:{key_name}")
            else:
                send_response(f"error:unknown_key:{key_name}")

        elif cmd.startswith("down:"):
            key_name = cmd[5:]
            keycode = get_keycode(key_name)
            if keycode:
                kbd.press(keycode)
                held_keys.add(keycode)
                send_response(f"ok:down:{key_name}")
            else:
                send_response(f"error:unknown_key:{key_name}")

        elif cmd.startswith("up:"):
            key_name = cmd[3:]
            keycode = get_keycode(key_name)
            if keycode and keycode in held_keys:
                kbd.release(keycode)
                held_keys.discard(keycode)
                send_response(f"ok:up:{key_name}")
            elif keycode:
                send_response(f"error:not_held:{key_name}")
            else:
                send_response(f"error:unknown_key:{key_name}")

        elif cmd.startswith("hold:"):
            parts = cmd[5:].split(":")
            if len(parts) == 2:
                key_name, duration_ms = parts
                keycode = get_keycode(key_name)
                duration_s = int(duration_ms) / 1000.0
                if keycode:
                    kbd.press(keycode)
                    time.sleep(duration_s)
                    kbd.release(keycode)
                    send_response(f"ok:hold:{key_name}:{duration_ms}")
                else:
                    send_response(f"error:unknown_key:{key_name}")
            else:
                send_response("error:bad_hold")
        else:
            send_response("error:unknown_command")

    except Exception as e:
        send_response(f"error:{e}")


# Main loop
if serial_port is None:
    raise RuntimeError(
        "usb_cdc.console is not enabled. Copy boot.py to the Pico and reconnect it."
    )

serial_port.timeout = 0.1
serial_port.write_timeout = 0.1

ready_sent = False

while True:
    if serial_port.connected and not ready_sent:
        send_response("ready")
        ready_sent = True

    if not serial_port.connected:
        ready_sent = False

    # Read one full command line at a time from the USB CDC data channel.
    line = serial_port.readline()
    if line:
        process_command(line.decode("utf-8", "ignore"))

    time.sleep(random.uniform(0.01, 0.02))  # Small delay to reduce CPU usage
