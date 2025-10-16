from typing import Tuple, List

from code.PressurePlate import PressurePlate
from code.SecretDoor import SecretDoor


class TargetFactory:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def create_target(self, symbol, position, targetMatriz: List[Tuple[int, int]]):

        if symbol == "S":
            return SecretDoor(position, self.tile_size,targetMatriz)

        return None