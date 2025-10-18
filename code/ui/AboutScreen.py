import pygame

def show_about_screen():
    screen_width, screen_height = 640, 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sobre o jogo")
    clock = pygame.time.Clock()

    # Fundo
    try:
        background = pygame.image.load("assets/menu_background.png").convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        background = pygame.Surface((screen_width, screen_height))
        background.fill((20, 20, 20))

    # Fontes
    try:
        title_font = pygame.font.Font("assets/fonts/mystery.ttf", 48)
    except:
        title_font = pygame.font.SysFont("serif", 48)

    body_font = pygame.font.SysFont(None, 28)

    # Texto
    title = title_font.render("Escape the Hollow", True, (200, 50, 50))
    lines = [
        "Jogo criado por João Barreto",
        "Explore, sobreviva e avance pelas fases!",

    ]

    blink_timer = 0
    show_hint = True

    while True:
        dt = clock.tick(60)
        blink_timer += dt
        if blink_timer > 500:
            show_hint = not show_hint
            blink_timer = 0

        screen.blit(background, (0, 0))

        # Título
        screen.blit(title, ((screen_width - title.get_width()) // 2, 60))

        # Corpo
        for i, line in enumerate(lines):
            label = body_font.render(line, True, (255, 255, 255))
            x = (screen_width - label.get_width()) // 2
            y = 160 + i * 40
            screen.blit(label, (x, y))

        # Dica piscante
        if show_hint:
            hint = body_font.render(". . .Pressione qualquer tecla. . .", True, (180, 180, 180))
            screen.blit(hint, ((screen_width - hint.get_width()) // 2, screen_height - 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return