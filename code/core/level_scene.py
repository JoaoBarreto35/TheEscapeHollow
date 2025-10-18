import pygame
from code.entities.player import Player
from code.core.map_builder import MapBuilder
from code.mechanics.entity_mediator import EntityMediator
from code.mechanics.puzzle_mediator import PuzzleMediator
from code.ui.tutorial_overlay import TutorialOverlay
from code.ui.pause_menu import PauseMenu
from code.ui.game_over_screen import GameOverScreen
from code.ui.hud import HUD
from code.core.level_loader import load_level_components
from code.data.levels import LevelsName, levelsHint
from code.entities.secret_door import SecretDoor
from code.ui.void_fall_transition import VoidFallTransition  # ✅ nova transição

class LevelScene:
    def __init__(self, current_map, level_index=0, player_lives=3):
        self.level_index = level_index
        self.level_name = LevelsName[level_index]
        self.level_hint = levelsHint[level_index]
        self.current_map = current_map
        self.player_lives = player_lives

        dummy_player = Player((0, 0), scale=2)
        self.tile_size = dummy_player.image.get_width() + 5
        self.width = len(current_map[0]) * self.tile_size
        self.height = len(current_map) * self.tile_size

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Escape the Hollow")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

        self.hud = HUD(self.font, self.tile_size)
        self.map_builder = MapBuilder(self.tile_size, "assets/wall.png", "assets/floor.png")
        self.wall_rects = self.map_builder.get_wall_rects(current_map)

        self.paused = False
        self.game_over = False
        self.falling_scene = None  # ✅ controle da transição

        self.load_components()

    def load_components(self):
        self.entities, self.triggers, self.targets = load_level_components(
            self.current_map, self.tile_size, f"level_{self.level_index}"
        )

        for entity in self.entities:
            if isinstance(entity, Player):
                entity.lives = self.player_lives

        self.entity_mediator = EntityMediator(self.entities, self.wall_rects)
        self.puzzle_mediator = PuzzleMediator(self.entities, self.triggers, self.targets, f"level_{self.level_index}")
        self.tutorial = TutorialOverlay("assets/ui/tutorial.png", 3000, (self.width, self.height))
        self.pause_menu = PauseMenu(self.font, self.width, self.height, self.level_hint)

        for target in self.targets:
            if isinstance(target, SecretDoor):
                self.wall_rects.append(target)

    def run(self):
        while True:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif self.paused:
                        action = self.pause_menu.handle_event(event)
                        if action == "Retomar":
                            self.paused = False
                        elif action == "Tutorial":
                            self.paused = False
                            self.tutorial = TutorialOverlay("assets/ui/tutorial.png", 3000, (self.width, self.height))
                        elif action == "Sair":
                            return "menu"

            self.window.fill("black")
            self.map_builder.draw_map(self.window, self.current_map)

            if self.falling_scene:
                self.falling_scene.update(dt)
                self.falling_scene.draw(self.window)
                if self.falling_scene.is_finished():
                    self.falling_scene = None
                    self.game_over = True

            elif not self.game_over and not self.paused:
                self.entity_mediator.update_all()
                self.puzzle_mediator.update_all()

                for entity in self.entities:
                    if isinstance(entity, Player) and entity.lives <= 0:
                        if entity.death_reason == "hole":
                            self.falling_scene = VoidFallTransition(entity, self.font, self.width, self.height)
                        else:
                            self.game_over = True
                        break

                if self.entity_mediator.level_complete:
                    for entity in self.entities:
                        if isinstance(entity, Player):
                            if self.level_index == len(LevelsName) - 1:
                                return "win"
                            else:
                                return "next", entity.lives

            elif self.game_over:
                result = self.handle_game_over()
                if result == "retry":
                    self.load_components()
                    self.game_over = False
                    continue
                elif result == "menu":
                    return "menu"

            self.draw(dt)
            pygame.display.update()

    def handle_game_over(self):
        player = next((e for e in self.entities if isinstance(e, Player)), None)
        death_reason = player.death_reason if player else "unknown"

        menu = GameOverScreen(self.font, self.width, self.height, death_reason)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                action = menu.handle_event(event)
                if action == "Tentar novamente":
                    return "retry"
                elif action == "Voltar ao menu":
                    return "menu"

            self.window.fill("black")
            self.map_builder.draw_map(self.window, self.current_map)
            menu.draw(self.window)
            pygame.display.update()
            self.clock.tick(60)

    def draw(self, dt):
        for entity in self.entities:
            if isinstance(entity, Player):
                self.hud.draw(self.window, entity, self.level_name)

        for trigger in self.triggers:
            trigger.update(self.entities)
            trigger.draw(self.window)

        for target in self.targets:
            target.update(dt)
            target.draw(self.window)

        for entity in self.entities:
            entity.draw(self.window)

        if self.level_index == 0:
            self.tutorial.update()
            self.tutorial.draw(self.window)

        if self.paused:
            self.pause_menu.draw(self.window)