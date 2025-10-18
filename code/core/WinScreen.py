import pygame

def run_win_screen():
    pygame.display.set_mode((1, 1))
    pygame.mixer.music.load("assets/music/win_theme.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play()

    win_image = pygame.image.load("assets/ui/win_screen.png").convert()
    width, height = win_image.get_size()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Vitória!")

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                return "menu"

        window.blit(win_image, (0, 0))
        pygame.display.update()