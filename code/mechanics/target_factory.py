from typing import Tuple, List

from code.entities.hole_trap import HoleTrap
from code.entities.secret_door import SecretDoor



class TargetFactory:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def create_target(self, symbol, position, targetMatriz: List[Tuple[int, int]]):

        if symbol == "S":
            return SecretDoor(position, self.tile_size,targetMatriz)
        elif symbol == "T":
            return HoleTrap(position, self.tile_size,targetMatriz )
        return None