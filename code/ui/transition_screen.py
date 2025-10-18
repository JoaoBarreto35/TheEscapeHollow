import pygame

class TransitionScreen:
    def __init__(self, level_name, width=640, height=480, duration=2000):
        self.level_name = level_name
        self.width = width
        self.height = height
        self.duration = duration

        try:
            self.font = pygame.font.Font("assets/fonts/mystery.ttf", 28)
        except:
            self.font = pygame.font.SysFont("serif", 28)

        self.title = self.font.render(level_name, True, (255, 255, 255))
        self.title_x = (self.width - self.title.get_width()) // 2
        self.title_y = (self.height - self.title.get_height()) // 2

        try:
            self.background = pygame.image.load("assets/ui/transition.png").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except:
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill((10, 10, 10))

    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Próxima fase")
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    return

            if pygame.time.get_ticks() - start_time > self.duration:
                return

            screen.blit(self.background, (0, 0))
            screen.blit(self.title, (self.title_x, self.title_y))
            pygame.display.update()