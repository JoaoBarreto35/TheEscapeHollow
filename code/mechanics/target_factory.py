from typing import Tuple, List

from code.entities.hole_trap import HoleTrap
from code.entities.secret_door import SecretDoor
from code.settings import MapSymbol


class TargetFactory:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def create_target(self, symbol: str, position, targetMatriz: List[Tuple[int, int]]):

        match symbol:
            case MapSymbol.SECRET_DOOR:
                return SecretDoor(position, self.tile_size, targetMatriz)
            case MapSymbol.HOLE_TRAP:
                return HoleTrap(position, self.tile_size, targetMatriz)
            case _:
                return None
