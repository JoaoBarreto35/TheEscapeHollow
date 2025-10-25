import pygame
from typing import Tuple, List, Union
from code.mechanics.target import Target
from code.core.image_loader import load_image

class SpikeReverse(Target):
    def __init__(self, position: Tuple[int, int], size: Union[int, Tuple[int, int]], target_matrix: List[Tuple[int, int]]):
        super().__init__(position, self._normalize_size(size), target_matrix)
        self.position = position
        self.size = self._normalize_size(size)
        self.image = load_image("assets/spikes.png", self.size)
        self.rect = self.image.get_rect(topleft=self.position)

        self.active = True
        self.anim_progress = 1.0
        self.anim_speed = 0.05
        self.animating = False
        self.anim_direction = 0
        self.reappear_timer = 0  # tempo restante pra reaparecer
        self.reappear_delay = 1000  # milissegundos até reaparecer (1 segundo)

        self.stone_drag_sound = self._load_sound("assets/sfx/stone_drag.wav", volume=0.1)

    def _normalize_size(self, size: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(size, int):
            return (size, size)
        elif isinstance(size, tuple) and len(size) == 2:
            return size
        else:
            raise ValueError(f"[Spikes] Tamanho inválido: {size}. Esperado int ou tupla (largura, altura)")

    def _load_sound(self, path: str, volume: float = 1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"[Spikes] Erro ao carregar som: {path} → {e}")
            return None

    def toggle(self, state: bool):
        print(f"[TOGGLE] Recebido toggle({state}) | active={self.active} | animating={self.animating} | anim_progress={self.anim_progress:.2f}")
        self.animating = True
        self.anim_direction = -1 if state else 1
        if self.stone_drag_sound:
            self.stone_drag_sound.play(0)

    def update(self, dt: int):
        if self.animating:
            self.anim_progress += self.anim_direction * self.anim_speed

            if self.anim_progress >= 1.0:
                self.anim_progress = 1.0
                self.animating = False
                self.active = True
                self.reappear_timer = 0
                print("[UPDATE] Animação completa: ATIVADO")

            elif self.anim_progress <= 0.0:
                self.anim_progress = 0.0
                self.animating = False
                self.active = False
                self.reappear_timer = self.reappear_delay
                print("[UPDATE] Animação completa: DESATIVADO")

        elif not self.active and self.reappear_timer > 0:
            self.reappear_timer -= dt
            print(f"[TIMER] reappear_timer={self.reappear_timer}")
            if self.reappear_timer <= 0:
                print("[TIMER] Reativando espinho!")
                self.toggle(False)  # inicia animação de surgimento

        altura = int(self.size[1] * self.anim_progress)
        if altura > 0:
            self.rect = pygame.Rect(self.position[0], self.position[1] + self.size[1] - altura, self.size[0], altura)
        else:
            self.rect = pygame.Rect(self.position[0], self.position[1], 0, 0)

    def draw(self, surface: pygame.Surface):
        if self.anim_progress > 0:
            altura = int(self.size[1] * self.anim_progress)
            img = pygame.transform.scale(self.image, (self.size[0], altura))
            y_offset = self.position[1] + self.size[1] - altura
            surface.blit(img, (self.position[0], y_offset))