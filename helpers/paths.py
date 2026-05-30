from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent


def is_frozen():
    return getattr(sys, "frozen", False)


def resource_path(*parts):
    """
    Resolve a bundled asset path.

    PyInstaller extracts data files into sys._MEIPASS at runtime, while
    normal source runs use the project directory.
    """
    base_path = (
        Path(getattr(sys, "_MEIPASS", PROJECT_ROOT)) if is_frozen() else PROJECT_ROOT
    )
    return base_path.joinpath(*parts)


def runtime_path(*parts):
    """
    Resolve a writable path.

    Frozen builds should write next to the executable; source runs write
    next to the repository checkout.
    """
    if is_frozen():
        base_path = Path(sys.executable).resolve().parent
    else:
        base_path = PROJECT_ROOT

    return base_path.joinpath(*parts)


def ensure_parent_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return path


def ensure_dir(*parts):
    path = runtime_path(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path
