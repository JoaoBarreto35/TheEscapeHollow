import pygame
from typing import Tuple, Union
from code.settings import ROCK_PUSH_SPEED
from code.core.image_loader import load_image

class PushableRock:
    def __init__(self, position: Tuple[int, int], size: Union[int, Tuple[int, int]]):
        self.position = pygame.Vector2(position)
        self.size = self._normalize_size(size)
        self.velocity = ROCK_PUSH_SPEED

        self.image = load_image("assets/rock.png", self.size)
        self.rect = self.image.get_rect(topleft=self.position)

        self.stone_drag_sound = self._load_sound("assets/sfx/stone_drag.wav", volume=0.1)

    def _normalize_size(self, size: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(size, int):
            return (size, size)
        elif isinstance(size, tuple) and len(size) == 2:
            return size
        else:
            raise ValueError(f"[PushableRock] Tamanho inválido: {size}. Esperado int ou tupla (largura, altura)")

    def _load_sound(self, path: str, volume: float = 1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"[PushableRock] Erro ao carregar som: {path} → {e}")
            return None

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect.topleft)

    def try_push(self, direction: str, wall_rects, other_entities) -> bool:
        offset = pygame.Vector2(0, 0)
        if direction == "up":
            offset.y = -self.velocity
        elif direction == "down":
            offset.y = self.velocity
        elif direction == "left":
            offset.x = -self.velocity
        elif direction == "right":
            offset.x = self.velocity

        new_rect = self.rect.move(offset)

        # Colisão com parede
        if any(new_rect.colliderect(wall) for wall in wall_rects):
            return False

        # Colisão com outras rochas
        if any(new_rect.colliderect(e.rect) for e in other_entities if isinstance(e, PushableRock) and e != self):
            return False

        # Colisão com inimigos
        from code.entities.enemy import Enemy
        if any(new_rect.colliderect(e.rect) for e in other_entities if isinstance(e, Enemy)):
            return False

        # Move a rocha
        self.position += offset
        self.rect.topleft = self.position

        if self.stone_drag_sound and not self.stone_drag_sound.get_num_channels():
            self.stone_drag_sound.play(0)

        return True