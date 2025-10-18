import pygame

class WinScreen:
    def __init__(self):
        pygame.display.set_mode((1, 1))
        pygame.mixer.music.load("assets/music/win_theme.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play()

        self.win_image = pygame.image.load("assets/ui/win_screen.png").convert()
        self.width, self.height = self.win_image.get_size()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vitória!")

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    return "menu"

            self.window.blit(self.win_image, (0, 0))
            pygame.display.update()