import pygame
from typing import Tuple, Union
from code.entities.entity import Entity
from code.ui.floating_heart import FloatingHeart
from code.core.image_loader import load_image

class LifeChest(Entity):
    def __init__(self, position: Tuple[int, int], tile_size: Union[int, Tuple[int, int]]):
        self.tile_size = self._normalize_size(tile_size)

        self.image_closed = load_image("assets/chest_closed.png", self.tile_size)
        self.image_opened = load_image("assets/chest_opened.png", self.tile_size)

        animations = {"down": [self.image_closed]}
        super().__init__(position, animations)

        self.opened = False
        self.rect.topleft = position
        self.heart_effect = None
        self.reward_sound = self._load_sound("assets/sfx/reward_magic.wav", volume=0.5)

    def _normalize_size(self, size: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(size, int):
            return (size, size)
        elif isinstance(size, tuple) and len(size) == 2:
            return size
        else:
            raise ValueError(f"[LifeChest] Tamanho inválido: {size}. Esperado int ou tupla (largura, altura)")

    def _load_sound(self, path: str, volume: float = 1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"[LifeChest] Erro ao carregar som: {path} → {e}")
            return None

    def update(self):
        if self.heart_effect:
            self.heart_effect.update(16)  # ou passe dt real se tiver

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if self.heart_effect and not self.heart_effect.is_finished():
            self.heart_effect.draw(surface)

    def open(self):
        if not self.opened:
            self.opened = True
            self.animations["down"] = [self.image_opened]
            self.image = self.image_opened
            self.heart_effect = FloatingHeart(self.position, self.tile_size[0])
            if self.reward_sound:
                self.reward_sound.play()