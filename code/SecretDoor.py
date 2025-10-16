from typing import Tuple, List
import pygame
from code.Target import Target  # ajuste o caminho conforme seu projeto

class SecretDoor(Target):
    def __init__(self, position, size, targetMatriz: List[Tuple[int, int]]):
        super().__init__(position, size, targetMatriz)
        self.active = False

    def toggle(self, state: bool):
        self.active = state

    def update(self):
        if self.active:
            self.rect.size = (0, 0)  # some fisicamente
        else:
            self.rect = self.image.get_rect(topleft=self.position)  # reaparece

    def draw(self, surface):
        if not self.active:
            surface.blit(self.image, self.rect.topleft)  # só desenha se estiver inativa