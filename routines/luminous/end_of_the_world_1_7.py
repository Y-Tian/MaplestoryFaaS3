import routines.luminous.skills as skills
import routines.common.skills as common_skills
from widgets.anchor import Anchor
from widgets.player import Player
import time
from widgets.logger import init_logger
from routines.common.movement import go_to

log = init_logger(__name__)


class Rotation:
    def __init__(self, player: Player, anchor: Anchor) -> None:
        self.player = player
        self.anchor = anchor
        self.loot_timer = 0

    """
    left lowest platform, next to red banner flag portal
    """
    def setup(self) -> None:
        player_coords = self.player.get_coordinates()
        if not player_coords:
            return
        # Delay for the user to switch to the game window after clicking "Setup Routine"
        time.sleep(3)
        log.info("Setting up routine")
        self.player.set_start_coordinates(player_coords)
        log.info("Routine setup complete")

    def do_mobbing(self) -> None:
        """
        Clear bottom platform, only works with vac pet
        """
        go_to(self.player, self.player.get_start_coordinates(), 1)
        skills.tp_right_atk()
        skills.tp_right_atk()
        skills.tp_right_atk()
        skills.tp_right_atk()
        skills.tp_right_atk()

        skills.tp_left_atk()
        skills.tp_left_atk()
        skills.tp_left_atk()
        skills.tp_left_atk()
        skills.tp_left_atk()
        skills.tp_left_atk()
        
        skills.tp_right_atk()

    def mobbing_cycle(self) -> None:
        while time.time() - self.loot_timer < 60:
            self.do_mobbing()

    def loot_cycle(self) -> None:
        go_to(self.player, self.player.get_start_coordinates(), 1)
        common_skills.tp_up()
        skills.tp_left_atk()
        skills.tp_right_atk()
        skills.tp_right_atk()
        skills.tp_right_atk()
        time.sleep(1.2)
        common_skills.tp_down()
        skills.tp_left_atk()
        skills.tp_left_atk()
        self.loot_timer = time.time()
