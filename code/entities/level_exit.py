import pygame
from typing import Tuple, Union
from code.core.image_loader import load_image

class LevelExit:
    def __init__(self, position: Tuple[int, int], tile_size: Union[int, Tuple[int, int]] = 32, image_path: str = "assets/door.png"):
        self.position = pygame.Vector2(position)
        self.size = self._normalize_size(tile_size)

        self.image = load_image(image_path, self.size)
        self.rect = self.image.get_rect(topleft=self.position)

    def _normalize_size(self, size: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(size, int):
            return (size, size)
        elif isinstance(size, tuple) and len(size) == 2:
            return size
        else:
            raise ValueError(f"[LevelExit] Tamanho inválido: {size}. Esperado int ou tupla (largura, altura)")

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect.topleft)