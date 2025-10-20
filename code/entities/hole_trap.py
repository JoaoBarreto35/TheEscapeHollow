import pygame
from typing import Tuple, List, Union
from code.mechanics.target import Target
from code.core.image_loader import load_image
from code.settings import TIME_HOLE_TRAP


class HoleTrap(Target):
    def __init__(self, position: Tuple[int, int], size: Union[int, Tuple[int, int]], target_matrix: List[Tuple[int, int]]):
        super().__init__(position, self._normalize_size(size), target_matrix)
        self.active = False
        self.open_timer = 0

        normalized_size = self._normalize_size(size)
        self.image = load_image("assets/floor.png", normalized_size)
        self.rect = self.image.get_rect(topleft=self.position)

    def _normalize_size(self, size: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(size, int):
            return (size, size)
        elif isinstance(size, tuple) and len(size) == 2:
            return size
        else:
            raise ValueError(f"[HoleTrap] Tamanho inválido: {size}. Esperado int ou tupla (largura, altura)")

    def toggle(self, state: bool):
        if state and not self.active:
            self.active = True
            self.open_timer = TIME_HOLE_TRAP
        else:
            self.open_timer = TIME_HOLE_TRAP

    def update(self, dt: int):
        if self.active:
            self.open_timer -= dt
            if self.open_timer <= 0:
                self.active = False

    def draw(self, surface: pygame.Surface):
        if self.active:
            pygame.draw.rect(surface, "black", self.rect)
        else:
            surface.blit(self.image, self.rect.topleft)