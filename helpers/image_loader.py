from pynput import keyboard
import pyautogui
from widgets.geometry import Point
from typing import List

def get_image_boundaries() -> List[Point]:
    boundaries: List[Point] = []

    def on_press(key) -> bool:
        if key == keyboard.Key.ctrl_l:
            mouse_x, mouse_y = pyautogui.position()
            boundaries.append(Point(mouse_x, mouse_y))

            if len(boundaries) == 2:
                return False
            
        return True

    with keyboard.Listener(on_press=on_press) as listener: # type: ignore
        listener.join()

    return boundaries