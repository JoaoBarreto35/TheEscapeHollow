import pygame

class Entity:
    def __init__(self, position, animations):
        self.position = pygame.Vector2(position)
        self.animations = animations
        self.direction = "down"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=self.position)

    def animate(self):
        self.frame_index = (pygame.time.get_ticks() // 300) % len(self.animations[self.direction])
        self.image = self.animations[self.direction][self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)