import numpy as np
import zlib
from widgets.geometry import Point
from PIL import Image


def find_coordinates_by_template(
    background: Image.Image, template: Image.Image, threshold: float
) -> Point | None:
    # Kept for backward compatibility with existing callers/config.
    _ = threshold

    background_arr = np.array(background.convert("RGB"), dtype=np.uint8)
    template_arr = np.array(template.convert("RGB"), dtype=np.uint8)

    bg_h, bg_w = background_arr.shape[:2]
    tpl_h, tpl_w = template_arr.shape[:2]

    if tpl_h > bg_h or tpl_w > bg_w:
        return None

    template_hash = zlib.crc32(template_arr.tobytes())
    first_px = template_arr[0, 0]
    max_y = bg_h - tpl_h + 1
    max_x = bg_w - tpl_w + 1

    for y in range(max_y):
        row = background_arr[y : y + tpl_h]
        for x in range(max_x):
            if not np.array_equal(background_arr[y, x], first_px):
                continue

            patch = row[:, x : x + tpl_w]
            if zlib.crc32(patch.tobytes()) != template_hash:
                continue

            if np.array_equal(patch, template_arr):
                return Point(x=x, y=y)

    return None
