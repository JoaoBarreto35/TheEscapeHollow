from code.entities.enemy import Enemy
from code.mechanics.level_exit import LevelExit
from code.entities.life_chest import LifeChest
from code.entities.player import Player
from code.entities.pushable_rock import PushableRock


# from code.PushableRock import PushableRock
# from code.Enemy import Enemy

class EntityFactory:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def create_entity(self, symbol, position):
        if symbol == "P":
            return Player(position, scale=2)
        elif symbol == "R":
             return PushableRock(position, size=self.tile_size-5)
        elif symbol == "H":
            return Enemy(position, scale=2, patrol_axis="H")
        elif symbol == "V":
            return Enemy(position, scale=2, patrol_axis="V")
        elif symbol == "X":
            return LevelExit(position, tile_size=self.tile_size) #correct?
        elif symbol == "C":
            return LifeChest(position, tile_size=self.tile_size)  # correct?

        return None