import pygame

class LevelExit:
    def __init__(self, position, image_path="assets/door.png", tile_size=32):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.position = pygame.Vector2(position)
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)