import argparse
import sys
import time

import serial
from serial.tools import list_ports

DEFAULT_PORT = "COM3"
DEFAULT_BAUDRATE = 115200
STARTUP_DELAY_SECONDS = 2.0
KEY_DELAY_SECONDS = 0.15
TYPE_DELAY_SECONDS = 0.08
TEST_MESSAGE = "pico keyboard test 123"
READ_TIMEOUT_SECONDS = 2.0


def send_command(connection, command):
    connection.write(f"{command}\n".encode("utf-8"))
    connection.flush()
    time.sleep(0.1)


def read_line(connection, timeout=READ_TIMEOUT_SECONDS):
    deadline = time.time() + timeout

    while time.time() < deadline:
        line = connection.readline()
        if line:
            return line.decode("utf-8", errors="replace").strip()
        time.sleep(0.05)

    return None


def read_expected_line(connection, expected, timeout=READ_TIMEOUT_SECONDS):
    deadline = time.time() + timeout

    while time.time() < deadline:
        line = read_line(
            connection, timeout=min(0.5, max(deadline - time.time(), 0.05))
        )
        if not line:
            continue
        if line == expected:
            return line
        print(f"Ignoring serial line: {line}")

    return None


def press(connection, key, delay=KEY_DELAY_SECONDS):
    send_command(connection, f"press:{key}")
    time.sleep(delay)


def hold(connection, key, duration_ms, delay=KEY_DELAY_SECONDS):
    send_command(connection, f"hold:{key}:{int(duration_ms)}")
    time.sleep(max(duration_ms / 1000.0, delay))


def type_message(connection, message):
    for char in message:
        if char == " ":
            key = "space"
        elif char.isalnum():
            key = char.lower()
        else:
            raise ValueError(f"Unsupported test character: {char!r}")

        press(connection, key, delay=TYPE_DELAY_SECONDS)


def run_test(port, baudrate):
    print(f"Opening Pico serial bridge on {port} at {baudrate} baud...")

    with serial.Serial(
        port, baudrate=baudrate, timeout=1, write_timeout=1
    ) as connection:
        connection.dtr = True
        connection.rts = True
        time.sleep(0.25)
        connection.reset_input_buffer()
        connection.reset_output_buffer()

        ready_message = read_expected_line(connection, "ready", timeout=1.5)
        if ready_message:
            print(f"Pico response on connect: {ready_message}")
        else:
            print("No startup message received from Pico.")

        send_command(connection, "ping")
        ping_response = read_expected_line(connection, "pong")
        if ping_response != "pong":
            raise RuntimeError(
                f"Expected 'pong' from Pico, but received: {ping_response!r}"
            )

        send_command(connection, "status")
        status_response = read_expected_line(connection, "ready")
        if status_response != "ready":
            raise RuntimeError(
                f"Expected 'ready' from Pico, but received: {status_response!r}"
            )

        print("Handshake succeeded. Pico firmware is receiving commands.")
        print(
            f"Connected. Focus a text field within {STARTUP_DELAY_SECONDS:.0f} seconds "
            "to observe typed output."
        )
        time.sleep(STARTUP_DELAY_SECONDS)

        print(f"Typing: {TEST_MESSAGE!r}")
        type_message(connection, TEST_MESSAGE)
        for _ in TEST_MESSAGE:
            response = read_line(connection)
            if response:
                print(f"Pico response: {response}")
        press(connection, "enter")
        enter_response = read_line(connection)
        if enter_response:
            print(f"Pico response: {enter_response}")

        print("Running arrow-key hold test: holding RIGHT for 750 ms.")
        hold(connection, "right", 750)
        hold_response = read_line(connection)
        if hold_response:
            print(f"Pico response: {hold_response}")

        print("\nExpected result:")
        print(f"1. The text field should contain: {TEST_MESSAGE}")
        print("2. A new line should be inserted.")
        print("3. The cursor or selection should move right briefly.")
        print("If all three happened, the Pico keyboard path is working.")


def handshake(port, baudrate):
    with serial.Serial(
        port, baudrate=baudrate, timeout=1, write_timeout=1
    ) as connection:
        connection.dtr = True
        connection.rts = True
        time.sleep(0.25)
        connection.reset_input_buffer()
        connection.reset_output_buffer()

        ready_message = read_expected_line(connection, "ready", timeout=1.5)
        send_command(connection, "ping")
        ping_response = read_expected_line(connection, "pong")
        send_command(connection, "status")
        status_response = read_expected_line(connection, "ready")

        return ready_message, ping_response, status_response


def scan_ports(baudrate):
    print("Scanning serial ports for the Pico data channel...")

    for port_info in list_ports.comports():
        port = port_info.device
        description = port_info.description or ""
        print(f"\nTesting {port} ({description})")

        try:
            ready_message, ping_response, status_response = handshake(port, baudrate)
            print(f"  ready: {ready_message!r}")
            print(f"  ping: {ping_response!r}")
            print(f"  status: {status_response!r}")
        except Exception as exc:
            print(f"  error: {exc}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simple Raspberry Pi Pico USB keyboard smoke test."
    )
    parser.add_argument(
        "--port", default=DEFAULT_PORT, help="Serial port for the Pico."
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        default=DEFAULT_BAUDRATE,
        help="Serial baudrate for the Pico bridge.",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Probe all serial ports and print the Pico handshake responses.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        if args.scan:
            scan_ports(args.baudrate)
            return 0
        run_test(args.port, args.baudrate)
    except serial.SerialException as exc:
        print(f"Serial error: {exc}", file=sys.stderr)
        print(
            "Verify that the Pico bridge is on the expected COM port and that no other "
            "program is using it.",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        print("\nTest cancelled.")
        return 130
    except Exception as exc:
        print(f"Test failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
