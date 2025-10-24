import sys
import pygame

from code.core.map_loader import MapLoader
from code.core.level_scene import LevelScene
from code.editor.editor_scene import run_editor
from code.ui.about_screen import show_about_screen
from code.ui.menu import show_menu
from code.ui.win_screen import WinScreen
from code.ui.transition_screen import TransitionScreen

def start_game():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/menu_theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, start=15.0)

    game_state = "menu"
    current_level_index = 0
    player_lives = 3

    map_loader = MapLoader()
    level_keys = map_loader.list_levels()  # ['level_0', 'level_1', ...]

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
            elif choice == "editor":

                editor = run_editor()
                result = editor.run()
                if result == "menu":
                    game_state = "menu"
                elif result == "quit":
                    break



        elif game_state == "playing":
            level_id = level_keys[current_level_index]
            scene = LevelScene(level_id, player_lives)
            result = scene.run()

            if isinstance(result, tuple):
                status, player_lives = result
            else:
                status = result

            if status == "next":
                current_level_index += 1
                if current_level_index < len(level_keys):
                    next_map = map_loader.load(level_keys[current_level_index])
                    TransitionScreen(next_map.name).run()
                else:
                    game_state = "win"
            elif status == "menu":
                game_state = "menu"
            elif status == "quit":
                break
            elif status == "win":
                game_state = "win"

        elif game_state == "win":
            result = WinScreen().run()
            if result == "menu":
                game_state = "menu"
            elif result == "quit":
                break

    pygame.quit()
    sys.exit()