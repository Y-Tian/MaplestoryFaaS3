from dataclasses import dataclass

import numpy as np
import cv2
from widgets.geometry import Point
from PIL import Image


@dataclass(frozen=True)
class HsvValidation:
    hue_tolerance: int = 8
    saturation_tolerance: int = 28
    value_tolerance: int = 22
    min_match_ratio: float = 0.95


def _build_validation_mask(template_rgba: np.ndarray, template_hsv: np.ndarray) -> np.ndarray:
    alpha = template_rgba[..., 3]
    if np.any(alpha < 255):
        mask = alpha > 0
        if np.any(mask):
            return mask

    mask = (template_hsv[..., 1] > 10) | (template_hsv[..., 2] > 10)
    if np.any(mask):
        return mask

    return np.ones(template_hsv.shape[:2], dtype=bool)


def _passes_hsv_validation(
    background_arr: np.ndarray,
    template_rgba: np.ndarray,
    template_hsv: np.ndarray,
    location: tuple[int, int],
    validation: HsvValidation,
) -> bool:
    match_x, match_y = location
    template_height, template_width = template_hsv.shape[:2]
    candidate_arr = background_arr[
        match_y : match_y + template_height,
        match_x : match_x + template_width,
    ]

    if candidate_arr.shape[:2] != template_hsv.shape[:2]:
        return False

    candidate_hsv = cv2.cvtColor(candidate_arr, cv2.COLOR_RGB2HSV)  # type: ignore
    template_mask = _build_validation_mask(template_rgba, template_hsv)

    candidate_hsv_int = candidate_hsv.astype(np.int16)
    template_hsv_int = template_hsv.astype(np.int16)

    hue_diff = np.abs(candidate_hsv_int[..., 0] - template_hsv_int[..., 0])
    hue_diff = np.minimum(hue_diff, 180 - hue_diff)
    saturation_diff = np.abs(candidate_hsv_int[..., 1] - template_hsv_int[..., 1])
    value_diff = np.abs(candidate_hsv_int[..., 2] - template_hsv_int[..., 2])

    matches = (
        (hue_diff <= validation.hue_tolerance)
        & (saturation_diff <= validation.saturation_tolerance)
        & (value_diff <= validation.value_tolerance)
    )

    validated_pixels = matches[template_mask]
    if validated_pixels.size == 0:
        return False

    return float(np.mean(validated_pixels)) >= validation.min_match_ratio


def find_coordinates_by_template(
    background: Image.Image,
    template: Image.Image,
    threshold: float,
    *,
    color_validation: HsvValidation | None = None,
) -> Point | None:
    background_rgb = background.convert("RGB")
    template_rgba = template.convert("RGBA")
    template_rgb = template_rgba.convert("RGB")

    background_arr = np.array(background_rgb, dtype=np.uint8)
    template_arr = np.array(template_rgb, dtype=np.uint8)
    template_rgba_arr = np.array(template_rgba, dtype=np.uint8)

    method = cv2.TM_SQDIFF_NORMED  # type: ignore

    if (
        background_arr.shape[0] < template_arr.shape[0]
        or background_arr.shape[1] < template_arr.shape[1]
    ):
        return None

    background_bgr = cv2.cvtColor(background_arr, cv2.COLOR_RGB2BGR)  # type: ignore
    template_bgr = cv2.cvtColor(template_arr, cv2.COLOR_RGB2BGR)  # type: ignore

    result = cv2.matchTemplate(background_bgr, template_bgr, method)  # type: ignore
    candidate_locations = np.where(result <= threshold)
    if candidate_locations[0].size == 0:
        return None

    candidate_scores = result[candidate_locations]
    candidate_order = np.argsort(candidate_scores)
    template_hsv = cv2.cvtColor(template_arr, cv2.COLOR_RGB2HSV)  # type: ignore

    for candidate_index in candidate_order:
        match_y = int(candidate_locations[0][candidate_index])
        match_x = int(candidate_locations[1][candidate_index])

        if color_validation is not None and not _passes_hsv_validation(
            background_arr,
            template_rgba_arr,
            template_hsv,
            (match_x, match_y),
            color_validation,
        ):
            continue

        return Point(x=match_x, y=match_y)

    return None
