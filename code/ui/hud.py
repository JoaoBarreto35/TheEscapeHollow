import pygame

class HUD:
    def __init__(self, font, tile_size):
        self.font = font
        self.tile_size = tile_size
        self.heart_img, self.dark_heart_img = self.load_heart_images(tile_size)

    def load_heart_images(self, tile_size):
        try:
            heart = pygame.image.load("assets/heart.png").convert_alpha()
        except:
            heart = pygame.Surface((tile_size - 5, tile_size - 5))
            heart.fill((255, 0, 0))

        heart = pygame.transform.scale(heart, (tile_size - 5, tile_size - 5))
        dark = heart.copy()
        overlay = pygame.Surface(dark.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        dark.blit(overlay, (0, 0))
        return heart, dark

    def draw(self, surface, player, level_name):
        title = self.font.render(level_name, True, (255, 255, 255))
        surface.blit(title, (10, 10))
        for i in range(5):
            heart = self.heart_img if i < player.lives else self.dark_heart_img
            x = 10 + i * (self.tile_size + 5)
            y = 10 + title.get_height() + 5
            surface.blit(heart, (x, y))