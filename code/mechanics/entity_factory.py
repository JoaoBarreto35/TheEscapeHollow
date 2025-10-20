from typing import Tuple, Optional
from code.entities.player import Player
from code.entities.pushable_rock import PushableRock
from code.entities.enemy import Enemy
from code.entities.life_chest import LifeChest
from code.entities.level_exit import LevelExit

class EntityFactory:
    def __init__(self, tile_size: int):
        self.tile_size = tile_size

    def create_entity(self, symbol: str, position: Tuple[int, int]) -> Optional[object]:

        # Player
        if symbol == "P":
            return Player(position, scale=2)

        # PushableRock
        elif symbol == "R":
            return PushableRock(position, size=self.tile_size - 5)

        # HorizontalEnenmy
        elif symbol == "H":
            return Enemy(position, scale=2, patrol_axis="H")

        # VerticalEnemy
        elif symbol == "V":
            return Enemy(position, scale=2, patrol_axis="V")

        # LevelExit
        elif symbol == "X":
            return LevelExit(position, tile_size=self.tile_size)

        # LifeChest
        elif symbol == "C":
            return LifeChest(position, tile_size=self.tile_size)

        # None
        return None