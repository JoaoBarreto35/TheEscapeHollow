import sys
import pygame

from code.data.Levels import levels, LevelsName
from code.core.level_scene import LevelScene
from code.ui.AboutScreen import show_about_screen
from code.ui.Menu import show_menu
from code.core.WinScreen import run_win_screen
from code.ui.TransitionScreen import TransitionScreen

def start_game():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/menu_theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, start=15.0)

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
            elif choice == "play":
                current_level_index = 0
                player_lives = 3
                game_state = "playing"

        elif game_state == "playing":
            level_keys = list(levels.keys())
            level_id = level_keys[current_level_index]
            current_map = levels[level_id]

            scene = LevelScene(current_map, current_level_index, player_lives)
            result = scene.run()

            if isinstance(result, tuple):
                status, player_lives = result
            else:
                status = result

            if status == "next":
                current_level_index += 1
                if current_level_index < len(level_keys):
                    next_name = LevelsName[current_level_index]
                    TransitionScreen(next_name).run()
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