import routines.bowmaster.skills as skills
import routines.common.skills as common_skills
import routines.common.movement as movement
from widgets.geometry import Point
from widgets.player import Player
import time

class Rotation:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.loot_timer = 0
        self.summon_timer = 0
        self.hurricane_anchor = Point()

    def setup(self):
        # Delay for the user to switch to the game window after clicking "Setup Routine"
        time.sleep(3)
        self.player.set_start_coordinates(self.player.get_coordinates())
        skills.set_blink_shot_portal()
        common_skills.flash_jump_right()
        movement.turn_left()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        self.hurricane_anchor = self.player.get_coordinates()
        skills.use_blink_shot_portal()

    def phase_one(self):
        pass

    def phase_two(self):
        pass