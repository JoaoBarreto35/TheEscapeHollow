import sys

import pygame
from code.Levels import levels, LevelsName
from code.Level import run_level, show_transition_screen
from code.Menu import show_menu
from code.ui.WinScreen import run_win_screen

def start_game():
    pygame.init()
    game_state = "menu"
    current_level_index = 0
    player_lives = 3

    while True:
        if game_state == "menu":
            choice = show_menu()
            if choice == "quit":
                break
            elif choice == "about":
                show_about_screen()
                game_state = "menu"
            elif choice == "play":
                current_level_index = 0
                player_lives = 3
                game_state = "playing"

        elif game_state == "playing":
            level_sequence = list(levels.keys())
            current_map = levels[level_sequence[current_level_index]]
            result = run_level(current_map, current_level_index, player_lives)

            if isinstance(result, tuple):
                status, player_lives = result
            else:
                status = result

            if status == "next":
                current_level_index += 1
                if current_level_index < len(level_sequence):
                    next_level_name = LevelsName[current_level_index]
                    show_transition_screen(next_level_name)
                else:
                    game_state = "win"

            elif status == "menu":
                game_state = "menu"
            elif status == "quit":
                break
            elif status == "win":
                game_state = "win"

        elif game_state == "win":
            result = run_win_screen()
            if result == "menu":
                game_state = "menu"
            elif result == "quit":
                break

    pygame.quit()
    sys.exit()


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