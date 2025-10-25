from typing import Tuple

from code.settings import MapSymbol
from code.triggers.pressure_plate import PressurePlate
from code.triggers.sound_sensor import SoundSensor


class TriggerFactory:
    def __init__(self, tile_size):
        self.tile_size = tile_size

    def create_trigger(self, symbol, position,triggerMatriz: Tuple[int, int]):
        match symbol:
            case MapSymbol.PRESSURE_PLATE:
                return PressurePlate(position, self.tile_size,triggerMatriz)
            case MapSymbol.SOUND_SENSOR:
                return SoundSensor(position, self.tile_size,triggerMatriz)
            case _:
                return None