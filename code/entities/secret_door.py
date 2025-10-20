import pygame
from typing import Tuple, List, Union
from code.mechanics.target import Target
from code.core.image_loader import load_image
from code.settings import TIME_SECRET_DOOR


class SecretDoor(Target):
    def __init__(self, position: Tuple[int, int], size: Union[int, Tuple[int, int]], target_matrix: List[Tuple[int, int]]):
        super().__init__(position, self._normalize_size(size), target_matrix)
        self.active = False
        self.open_timer = 0

        normalized_size = self._normalize_size(size)
        self.image = load_image("assets/wall.png", normalized_size)
        self.rect = self.image.get_rect(topleft=self.position)

        self.stone_drag_sound = self._load_sound("assets/sfx/stone_drag.wav", volume=0.1)

    def _normalize_size(self, size: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(size, int):
            return (size, size)
        elif isinstance(size, tuple) and len(size) == 2:
            return size
        else:
            raise ValueError(f"[SecretDoor] Tamanho inválido: {size}. Esperado int ou tupla (largura, altura)")

    def _load_sound(self, path: str, volume: float = 1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"[SecretDoor] Erro ao carregar som: {path} → {e}")
            return None

    def toggle(self, state: bool):
        if state and not self.active:
            if self.stone_drag_sound:
                self.stone_drag_sound.play(0)
            self.active = True
            self.open_timer = TIME_SECRET_DOOR
        else:
            self.open_timer = TIME_SECRET_DOOR

    def update(self, dt: int):
        if self.active:
            self.rect = pygame.Rect(self.position[0], self.position[1], 0, 0)
            self.open_timer -= dt
            if self.open_timer <= 0:
                if self.stone_drag_sound:
                    self.stone_drag_sound.play(0)
                self.active = False
        else:
            self.rect = self.image.get_rect(topleft=self.position)

    def draw(self, surface: pygame.Surface):
        if not self.active:
            surface.blit(self.image, self.rect.topleft)