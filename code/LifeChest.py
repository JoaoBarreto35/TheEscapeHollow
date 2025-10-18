import pygame
from code.Entity import Entity
from code.FloatingHeart import FloatingHeart

class LifeChest(Entity):
    def __init__(self, position, tile_size):
        self.image_closed = pygame.image.load("assets/chest_closed.png").convert_alpha()
        self.image_opened = pygame.image.load("assets/chest_opened.png").convert_alpha()

        self.image_closed = pygame.transform.scale(self.image_closed, (tile_size, tile_size))
        self.image_opened = pygame.transform.scale(self.image_opened, (tile_size, tile_size))

        animations = {"down": [self.image_closed]}
        super().__init__(position, animations)

        self.opened = False
        self.rect.topleft = position
        self.tile_size = tile_size
        self.heart_effect = None

        try:
            self.reward_sound = pygame.mixer.Sound("assets/sfx/reward_magic.wav")
            self.reward_sound.set_volume(0.5)
        except FileNotFoundError:
            self.reward_sound = None

    def update(self):
        if self.heart_effect:
            self.heart_effect.update(16)  # ou passe dt real se tiver

    def draw(self, surface):
        super().draw(surface)
        if self.heart_effect and not self.heart_effect.is_finished():
            self.heart_effect.draw(surface)

    def open(self):
        if not self.opened:
            self.opened = True
            self.animations["down"] = [self.image_opened]
            self.image = self.image_opened
            self.heart_effect = FloatingHeart(self.position, self.tile_size)
            if self.reward_sound:
                self.reward_sound.play()