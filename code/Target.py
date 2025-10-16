from typing import Tuple, List

import pygame


class Target:

    def __init__(self, position, size, targetMatriz: List[Tuple[int, int]]):
        self.targetMatriz = targetMatriz
        self.position = pygame.Vector2(position)
        self.size = size
        self.image = pygame.image.load("assets/wall.png").convert()
        self.rect = self.image.get_rect(topleft=self.position)
        self.active = False

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def toggle(self, toggle):
        self.active = toggle

