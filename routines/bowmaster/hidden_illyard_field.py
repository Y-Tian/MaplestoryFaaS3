import routines.bowmaster.skills as skills
import routines.common.skills as common_skills
import routines.common.movement as movement
from widgets.anchor import Anchor
from widgets.geometry import Point
from widgets.player import Player
import time
from widgets.logger import init_logger
from routines.common.movement import go_to
import routines.common.buff as buff
import routines.common.pet as pet

log = init_logger(__name__)


class Rotation:
    def __init__(self, player: Player, anchor: Anchor) -> None:
        self.player = player
        self.anchor = anchor
        self.loot_timer = 0
        self.summon_timer = 0

    def setup(self) -> None:
        player_coords = self.player.get_coordinates()
        if not player_coords:
            return
        # Delay for the user to switch to the game window after clicking "Setup Routine"
        time.sleep(3)
        log.info("Setting up routine")
        self.player.set_start_coordinates(player_coords)
        skills.set_blink_shot_portal(initial=True)
        common_skills.flash_jump_right()
        movement.turn_left()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        player_coords = self.player.get_coordinates()
        if not player_coords:
            return
        self.anchor.set_coordinates(player_coords)
        skills.use_blink_shot_portal()
        log.info("Routine setup complete")

    def set_summons(self) -> None:
        skills.use_blink_shot_portal()
        go_to(self.player, self.player.get_start_coordinates(), 1)
        skills.set_blink_shot_portal()
        common_skills.set_erda_fountain()
        movement.turn_right()
        skills.jump_covering_fire()
        movement.turn_left()
        skills.swift_surge()
        skills.set_arrow_blaster()
        skills.swift_surge()
        skills.use_blink_shot_portal()
        go_to(self.player, self.player.get_start_coordinates(), 1)
        skills.set_blink_shot_portal()
        common_skills.flash_jump_right()
        movement.turn_left()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()

    def do_mobbing(self) -> None:
        go_to(self.player, self.anchor.get_coordinates(), 1)
        skills.jumping_hurricane_left_right(time.time() + 45)

    def mobbing_cycle(self) -> None:
        while time.time() - self.loot_timer < 120:
            self.set_summons()
            self.do_mobbing()

    def loot_cycle(self) -> None:
        buff.activate_sequence()
        pet.feed()

        skills.use_blink_shot_portal()
        go_to(self.player, self.player.get_start_coordinates(), 1)
        skills.set_blink_shot_portal()
        common_skills.activate_loot_sequence()
        movement.turn_left()
        skills.jump_covering_fire()
        # Delay for momentum
        time.sleep(1.5)
        skills.use_blink_shot_portal()
        movement.turn_left()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        skills.swift_surge()
        movement.turn_right()
        skills.jump_covering_fire()
        # Delay for momentum
        time.sleep(2)
        self.loot_timer = time.time()
