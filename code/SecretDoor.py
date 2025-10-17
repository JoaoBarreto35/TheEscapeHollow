from typing import Tuple, List
import pygame
from code.Target import Target  # ajuste o caminho conforme seu projeto

stone_drag_sound = pygame.mixer.Sound("assets/sfx/stone_drag.wav")
stone_drag_sound.set_volume(0.1)
class SecretDoor(Target):
    def __init__(self, position, size, targetMatriz: List[Tuple[int, int]]):
        super().__init__(position, size, targetMatriz)
        self.active = False
        self.open_timer = 0  # tempo restante em milissegundos


    def toggle(self, state: bool):
        if state:
            if not self.active:
                stone_drag_sound.play(0)
            self.active = True
            self.open_timer = 2000  # tempo em ms (ex: 2 segundos)
        # não desativa aqui — o tempo vai controlar isso

    def update(self, dt):
        if self.active:
            self.open_timer -= dt
            if self.open_timer <= 0:
                stone_drag_sound.play(0)
                self.active = False

        # atualiza o rect com base no estado
        if self.active:
            self.rect.size = (0, 0)

        else:
            self.rect = self.image.get_rect(topleft=self.position)

    def draw(self, surface):
        if not self.active:
            surface.blit(self.image, self.rect.topleft)