import threading
import time
import serial
from serial.tools import list_ports
from config import (
    DEFAULT_BAUDRATE,
    DEFAULT_PORT,
    PAUSE,
    OPEN_DELAY_SECONDS,
    HANDSHAKE_TIMEOUT_SECONDS,
)

_bridge = None
_bridge_lock = threading.Lock()


def _normalize_key(key):
    if key is None:
        raise ValueError("Key cannot be None")

    if isinstance(key, str):
        return key.lower().strip()

    if hasattr(key, "value"):
        return str(key.value).lower().strip()

    return str(key).lower().strip()


def _read_line(connection, timeout=HANDSHAKE_TIMEOUT_SECONDS):
    deadline = time.time() + timeout

    while time.time() < deadline:
        line = connection.readline()
        if line:
            return line.decode("utf-8", errors="replace").strip()
        time.sleep(0.05)

    return None


def _read_expected_line(connection, expected, timeout=HANDSHAKE_TIMEOUT_SECONDS):
    deadline = time.time() + timeout

    while time.time() < deadline:
        line = _read_line(
            connection, timeout=min(0.5, max(deadline - time.time(), 0.05))
        )
        if not line:
            continue
        if line == expected:
            return line

    return None


def _send_command(connection, command):
    connection.write(f"{command}\n".encode("utf-8"))
    connection.flush()
    time.sleep(0.1)


def _probe_port(port, baudrate, timeout):
    try:
        with serial.Serial(
            port, baudrate=baudrate, timeout=timeout, write_timeout=timeout
        ) as connection:
            connection.dtr = True
            connection.rts = True
            time.sleep(OPEN_DELAY_SECONDS)
            connection.reset_input_buffer()
            connection.reset_output_buffer()
            _read_expected_line(connection, "ready", timeout=1.5)
            _send_command(connection, "ping")
            return _read_expected_line(connection, "pong") == "pong"
    except serial.SerialException:
        return False


def _find_pico_port(baudrate, timeout):
    for port_info in list_ports.comports():
        description = (port_info.description or "").lower()
        if "usb serial device" not in description and "pico" not in description:
            continue

        if _probe_port(port_info.device, baudrate, timeout):
            return port_info.device

    return None


def _open_serial(port, baudrate, timeout):
    connection = serial.Serial(
        port,
        baudrate=baudrate,
        timeout=timeout,
        write_timeout=timeout,
    )
    connection.dtr = True
    connection.rts = True
    time.sleep(OPEN_DELAY_SECONDS)
    connection.reset_input_buffer()
    connection.reset_output_buffer()
    return connection


def _handshake(connection, port):
    ready_message = _read_expected_line(connection, "ready", timeout=1.5)
    _send_command(connection, "ping")
    ping_response = _read_expected_line(connection, "pong")
    _send_command(connection, "status")
    status_response = _read_expected_line(connection, "ready")

    if ping_response != "pong" or status_response != "ready":
        raise RuntimeError(
            f"Pico handshake failed on {port}. "
            f"ready={ready_message!r}, ping={ping_response!r}, status={status_response!r}"
        )


class SerialKeyboardBridge:
    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE, timeout=0.1):
        requested_port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.port = requested_port
        self._write_lock = threading.Lock()

        try:
            self._serial = _open_serial(self.port, self.baudrate, self.timeout)
            _handshake(self._serial, self.port)
        except (serial.SerialException, RuntimeError):
            if "_serial" in self.__dict__ and self._serial.is_open:
                self._serial.close()

            detected_port = _find_pico_port(self.baudrate, self.timeout)
            if not detected_port:
                raise

            self.port = detected_port
            self._serial = _open_serial(self.port, self.baudrate, self.timeout)
            _handshake(self._serial, self.port)

    def _write_line(self, command):
        with self._write_lock:
            _send_command(self._serial, command)

    def press(self, key):
        self._write_line(f"press:{_normalize_key(key)}")
        if PAUSE:
            time.sleep(PAUSE)

    def key_down(self, key):
        self._write_line(f"down:{_normalize_key(key)}")
        if PAUSE:
            time.sleep(PAUSE)

    def key_up(self, key):
        self._write_line(f"up:{_normalize_key(key)}")
        if PAUSE:
            time.sleep(PAUSE)

    def hold(self, key, duration_ms):
        self._write_line(f"hold:{_normalize_key(key)}:{int(duration_ms)}")
        if PAUSE:
            time.sleep(PAUSE)

    def close(self):
        with self._write_lock:
            if self._serial.is_open:
                self._serial.close()


def get_bridge():
    global _bridge
    if _bridge is None:
        with _bridge_lock:
            if _bridge is None:
                _bridge = SerialKeyboardBridge()
    return _bridge


def press(key):
    get_bridge().press(key)


def key_down(key):
    get_bridge().key_down(key)


def key_up(key):
    get_bridge().key_up(key)


def hold(key, duration_ms):
    get_bridge().hold(key, duration_ms)


def close():
    global _bridge
    if _bridge is not None:
        _bridge.close()
        _bridge = None
