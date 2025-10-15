import pygame
from code.ImageLoader import load_player_spritesheet

class Enemy:
    def __init__(self, position, scale=2, patrol_axis="H"):
        self.position = pygame.Vector2(position)
        self.speed = 2.5
        self.direction = "right" if patrol_axis == "H" else "down"
        self.axis = patrol_axis  # "H" ou "V"

        self.frames = load_player_spritesheet("assets/enemy_spritesheet.png", scale)
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.image = self.frames[self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self):
        # Movimento automático
        offset = pygame.Vector2(0, 0)
        if self.direction == "up":
            offset.y = -self.speed
        elif self.direction == "down":
            offset.y = self.speed
        elif self.direction == "left":
            offset.x = -self.speed
        elif self.direction == "right":
            offset.x = self.speed

        self.position += offset
        self.rect.topleft = self.position

        # Animação
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
            self.image = self.frames[self.direction][self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def reverse_direction(self):
        if self.axis == "H":
            self.direction = "left" if self.direction == "right" else "right"
        else:
            self.direction = "up" if self.direction == "down" else "down"