from typing import Tuple, List

from code.PressurePlate import PressurePlate


class TriggerFactory:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def create_trigger(self, symbol, position,triggerMatriz: Tuple[int, int]):

        if symbol == "L":
            return PressurePlate(position, self.tile_size,triggerMatriz)

        return None