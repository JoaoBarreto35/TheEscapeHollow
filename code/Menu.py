import pygame

def show_menu(screen_width=640, screen_height=480):
    pygame.display.set_caption("Escape the Hollow — Menu")
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/menu_theme.mp3")
    pygame.mixer.music.play(-1)  # -1 = loop infinito
    # Fontes
    try:
        title_font = pygame.font.Font("assets/fonts/mystery.ttf", 48)
    except:
        title_font = pygame.font.SysFont("serif", 48)

    option_font = pygame.font.SysFont(None, 36)

    # Fundo
    try:
        background = pygame.image.load("assets/menu_background.png").convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        background = pygame.Surface((screen_width, screen_height))
        background.fill((10, 10, 10))

    # Opções: (texto exibido, valor retornado)
    options = [("Jogar", "play"), ("Sobre o jogo", "about"), ("Sair", "quit")]
    selected = 0

    clock = pygame.time.Clock()
    while True:
        window.blit(background, (0, 0))

        # Título
        title_text = title_font.render("Escape the Hollow", True, (200, 50, 50))
        title_x = (screen_width - title_text.get_width()) // 2
        title_y = 60
        window.blit(title_text, (title_x, title_y))

        # Opções
        for i, (text, _) in enumerate(options):
            color = (255, 255, 255) if i == selected else (180, 180, 180)
            label = option_font.render(text, True, color)
            x = (screen_width - label.get_width()) // 2
            y = 200 + i * 50
            window.blit(label, (x, y))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected][1]