from helpers.image_compare import HsvValidation

# GUI and main configuration settings
GUI_NAME = "BacklitManager"
ACTIVE_WINDOW_NAME = "MapleStory"

# Image recognition settings
PLAYER_ICON_MATCH_THRESHOLD = 0.30
RUNE_DETECTION_STABILITY_SECONDS = 5.0
RUNE_ICON_MATCH_THRESHOLD = 0.30
ENEMY_ICON_MATCH_THRESHOLD = 0.30

ICON_COLOR_VALIDATION = HsvValidation(
    hue_tolerance=20,
    saturation_tolerance=40,
    value_tolerance=30,
    min_match_ratio=0.75,
)

# Serial communication settings
DEFAULT_BAUDRATE = 115200
DEFAULT_PORT = "COM3"
PAUSE = 0.0
OPEN_DELAY_SECONDS = 0.25
HANDSHAKE_TIMEOUT_SECONDS = 2.0

# Common key bindings
JUMP_KEY = "v"
ROPE_LIFT_KEY = "h"
FMA_KEY = "r"
RUNE_KEY = "y"
BUFF_SEQUENCE_KEY = "a"
PET_FOOD_KEY = "9"
CASH_SHOP_KEY = "del"
TO_TOWN_KEY = "home"
