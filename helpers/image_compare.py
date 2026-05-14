import numpy as np
import cv2
from widgets.geometry import Point
from PIL import Image

def find_coordinates_by_template(background: Image.Image, template: Image.Image, threshold: float) -> Point | None:
    background_rgb = background.convert("RGB")
    template_rgb = template.convert("RGB")

    background_arr = np.array(background_rgb, dtype=np.uint8)
    template_arr = np.array(template_rgb, dtype=np.uint8)

    method = cv2.TM_SQDIFF_NORMED # type: ignore

    background_bgr = cv2.cvtColor(background_arr, cv2.COLOR_RGB2BGR) # type: ignore
    template_bgr = cv2.cvtColor(template_arr, cv2.COLOR_RGB2BGR) # type: ignore

    result = cv2.matchTemplate(background_bgr, template_bgr, method) # type: ignore
    min_score = float(np.amin(result))

    if min_score > threshold:
        return None
    
    _, _, min_loc, _ = cv2.minMaxLoc(result) # type: ignore
    match_x, match_y = min_loc
    
    return Point(x=match_x, y=match_y)