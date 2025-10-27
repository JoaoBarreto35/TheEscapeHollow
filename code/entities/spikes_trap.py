import pygame
from typing import Tuple, List, Union
from code.mechanics.target import Target
from code.core.image_loader import load_image

class SpikesTrap(Target):
    def __init__(self, position: Tuple[int, int], size: Union[int, Tuple[int, int]], target_matrix: List[Tuple[int, int]]):
        super().__init__(position, self._normalize_size(size), target_matrix)
        self.position = position
        self.size = self._normalize_size(size)
        self.image = load_image("assets/spikes.png", self.size)
        self.rect = self.image.get_rect(topleft=self.position)

        # Estado inicial
        self.active = False
        self.anim_progress = 0.0
        self.anim_speed = 0.05
        self.animating = False
        self.anim_direction = 0

        # Timer de duração ativa
        self.active_timer = 0
        self.active_duration = 1000  # ms visível

        self.spikes_sound = self._load_sound("assets/sfx/spikes.wav", volume=0.1)

    def _normalize_size(self, size: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(size, int):
            return (size, size)
        elif isinstance(size, tuple) and len(size) == 2:
            return size
        raise ValueError(f"[SpikeTrap] Tamanho inválido: {size}. Esperado int ou tupla (largura, altura)")

    def _load_sound(self, path: str, volume: float = 1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"[SpikeTrap] Erro ao carregar som: {path} → {e}")
            return None

    def toggle(self, state: bool):
        self.animating = True
        self.anim_direction = 1 if state else -1
        if self.spikes_sound:
            self.spikes_sound.play(0)

    def update(self, dt: int):
        # Animação de surgimento ou recolhimento
        if self.animating:
            self.anim_progress += self.anim_direction * self.anim_speed

            if self.anim_progress >= 1.0:
                self.anim_progress = 1.0
                self.animating = False
                self.active = True
                self.active_timer = self.active_duration

            elif self.anim_progress <= 0.0:
                self.anim_progress = 0.0
                self.animating = False
                self.active = False

        # Timer de duração ativa
        elif self.active and self.active_timer > 0:
            self.active_timer -= dt
            if self.active_timer <= 0:
                self.toggle(False)

        # Atualiza área de colisão
        altura = int(self.size[1] * self.anim_progress)
        if altura > 0:
            self.rect = pygame.Rect(
                self.position[0],
                self.position[1] + self.size[1] - altura,
                self.size[0],
                altura
            )
        else:
            self.rect = pygame.Rect(self.position[0], self.position[1], 0, 0)

    def draw(self, surface: pygame.Surface):
        if self.anim_progress > 0:
            altura = int(self.size[1] * self.anim_progress)
            img = pygame.transform.scale(self.image, (self.size[0], altura))
            y_offset = self.position[1] + self.size[1] - altura
            surface.blit(img, (self.position[0], y_offset))