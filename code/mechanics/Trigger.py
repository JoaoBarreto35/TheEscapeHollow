from typing import Tuple, List

import pygame


class Trigger:

    def __init__(self, position, size, triggerMatriz: Tuple[int, int]):
        self.triggerMatriz = triggerMatriz

        self.position = pygame.Vector2(position)
        self.size = size
        self.image = pygame.image.load("assets/pressure_plate_off.png").convert()
        self.rect = self.image.get_rect(topleft=self.position)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def update(self, entity):
        pass
