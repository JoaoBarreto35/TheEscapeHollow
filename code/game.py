import pygame
from code.Levels import levels
from code.Level import run_level
from code.Menu import show_menu

def start_game():
    pygame.init()
    choice = show_menu()
    if choice == "quit":
        pygame.quit()
        return

    level_sequence = list(levels.keys())
    current_level_index = 0
    player_lives = 3  # vidas persistentes

    while True:
        current_map = levels[level_sequence[current_level_index]]
        result = run_level(current_map, current_level_index, player_lives)

        if isinstance(result, tuple):
            status, player_lives = result
        else:
            status = result

        if status == "next":
            current_level_index = (current_level_index + 1) % len(level_sequence)
        elif status == "menu":
            start_game()
        elif status == "quit":
            break

    pygame.quit()


def show_about_screen():
    screen = pygame.display.set_mode((640, 480))
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    text_lines = [
        "Escape the Hollow",
        "Jogo criado por João",
        "Explore, sobreviva e avance pelas fases!",
        "Pressione qualquer tecla para voltar ao menu"
    ]

    while True:
        screen.fill((10, 10, 10))
        for i, line in enumerate(text_lines):
            label = font.render(line, True, (255, 255, 255))
            screen.blit(label, ((640 - label.get_width()) // 2, 150 + i * 40))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return