from typing import Tuple, Optional
from code.entities.player import Player
from code.entities.pushable_rock import PushableRock
from code.entities.enemy import Enemy
from code.entities.life_chest import LifeChest
from code.entities.level_exit import LevelExit
from code.settings import MapSymbol


class EntityFactory:
    def __init__(self, tile_size: int):
        self.tile_size = tile_size

    def create_entity(self, symbol: str, position: Tuple[int, int]) -> Optional[object]:

        match symbol:
            case MapSymbol.PLAYER:
                return Player(position, scale=2)
            case MapSymbol.PUSHABLE_ROCK:
                return PushableRock(position, size=self.tile_size - 5)
            case MapSymbol.ENEMY_HORIZONTAL:
                return Enemy(position, scale=2, patrol_axis="H")
            case MapSymbol.ENEMY_VERTICAL:
                return Enemy(position, scale=2, patrol_axis="V")
            case MapSymbol.LEVEL_EXIT:
                return LevelExit(position, tile_size=self.tile_size)
            case MapSymbol.LIFE_CHEST:
                return LifeChest(position, tile_size=self.tile_size)
            case _:
                return None
