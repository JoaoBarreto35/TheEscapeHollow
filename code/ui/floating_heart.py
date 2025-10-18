import pygame

class FloatingHeart:
    def __init__(self, position, tile_size):
        self.image = pygame.image.load("assets/heart.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size - 5, tile_size - 5))
        self.position = pygame.Vector2(position)
        self.alpha = 255
        self.timer = 0

    def update(self, dt):
        self.position.y -= 0.05 * dt
        self.alpha -= 1.5
        self.timer += dt

    def draw(self, surface):
        if self.alpha <= 0:
            return
        temp = self.image.copy()
        temp.set_alpha(max(0, int(self.alpha)))
        surface.blit(temp, self.position)

    def is_finished(self):
        return self.alpha <= 0 or self.timer > 2000