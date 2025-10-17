from xml.dom.minidom import ProcessingInstruction

import pygame

from code import Levels
from code.SecretDoor import SecretDoor
from code.Levels import LevelsName, LevelsEvents
from code.MapBuilder import MapBuilder
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player
from code.PuzzleMediator import PuzzleMediator
from code.TargetFactory import TargetFactory
from code.TriggerFactory import TriggerFactory
from code.TutorialOverlay import TutorialOverlay


# 🎮 HUD: vidas e nome do level
def load_heart_images(tile_size):
    heart = pygame.image.load("assets/heart.png").convert_alpha()
    heart = pygame.transform.scale(heart, (tile_size - 5, tile_size - 5))
    dark = heart.copy()
    overlay = pygame.Surface(dark.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    dark.blit(overlay, (0, 0))
    return heart, dark


def draw_hud(surface, font, player, level_name, heart_img, dark_heart, tile_size):
    # 🧭 Nome do level
    title = font.render(level_name, True, (255, 255, 255))
    surface.blit(title, (10, 10))

    # ❤️ Vidas
    for i in range(5):
        heart = heart_img if i < player.lives else dark_heart
        x = 10 + i * (tile_size + 5)
        y = 10 + title.get_height() + 5
        surface.blit(heart, (x, y))


# ☠️ Tela de Game Over
def draw_game_over(surface, font, width, height):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    title = font.render("GAME OVER", True, (255, 0, 0))
    retry = font.render("ENTER para tentar novamente", True, (255, 255, 255))
    menu = font.render("M para voltar ao menu", True, (255, 255, 255))

    surface.blit(title, ((width - title.get_width()) // 2, height // 2 - 60))
    surface.blit(retry, ((width - retry.get_width()) // 2, height // 2))
    surface.blit(menu, ((width - menu.get_width()) // 2, height // 2 + 40))


# 🔁 Reset do mapa
def reset_entities(current_map, tile_size):
    factory = EntityFactory(tile_size)
    entities = []
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            x = col_idx * tile_size
            y = row_idx * tile_size
            entity = factory.create_entity(cell, (x, y))
            if entity:
                entities.append(entity)
    return entities


def reset_triggers(current_map, tile_size, levelName):
    factory = TriggerFactory(tile_size)
    triggers = []

    # Coleta todos os triggers definidos nos eventos
    all_triggers = [event["trigger"] for event in LevelsEvents[levelName]]

    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            if (row_idx, col_idx) in all_triggers:
                x = col_idx * tile_size
                y = row_idx * tile_size
                trigger = factory.create_trigger(cell, (x, y), (row_idx, col_idx))
                if trigger:
                    triggers.append(trigger)

    return triggers
def reset_targets(current_map, tile_size,levelName):
    factory = TargetFactory(tile_size)
    targets = []

    # Coleta todas as posições de targets definidas nos eventos
    all_targets = set()
    for event in LevelsEvents[levelName]:
        for pos in event["targets"]:
            all_targets.add(pos)

    # Cria targets apenas nas posições definidas
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            pos = (row_idx, col_idx)
            if pos in all_targets:
                x = col_idx * tile_size
                y = row_idx * tile_size
                target = factory.create_target(cell, (x, y), pos)
                if target:
                    targets.append(target)

    return targets
# 🚀 Execução do level
def run_level(current_map, level_index=0):

    pygame.display.set_mode((1, 1))  # necessário para .convert()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/menu_theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, start=15.0)

    # Calcula TILE_SIZE dinamicamente
    dummy_player = Player((0, 0), scale=2)
    tile_size = dummy_player.image.get_width() + 5

    rows = len(current_map)
    cols = len(current_map[0])
    width = cols * tile_size
    height = rows * tile_size

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Escape the Hollow")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    heart_img, dark_heart = load_heart_images(tile_size)
    map_builder = MapBuilder(tile_size, "assets/wall.png", "assets/floor.png")
    wall_rects = map_builder.get_wall_rects(current_map)

    triggers = reset_triggers(current_map, tile_size, f"level_{level_index}")
    targets = reset_targets(current_map, tile_size,f"level_{level_index}")
    entities = reset_entities(current_map, tile_size)
    entity_mediator = EntityMediator(entities, wall_rects)
    puzzle_mediator = PuzzleMediator(entities, triggers, targets, f"level_{level_index}")

    tutorial = TutorialOverlay("assets/ui/tutorial.png", 3000, (width, height))

    #adicionando  targets SecretDoor in wall_rects
    for secret_door in targets:
        if isinstance(secret_door, SecretDoor):
            wall_rects.append(secret_door)

    game_over = False
    level_name = LevelsName[level_index]

    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        window.fill("black")
        map_builder.draw_map(window, current_map)

        if not game_over:
            entity_mediator.update_all()
            puzzle_mediator.update_all()

            for entity in entities:
                if isinstance(entity, Player) and entity.lives <= 0:
                    game_over = True
                    break

            if entity_mediator.level_complete:
                return "next"
        else:
            draw_game_over(window, font, width, height)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                entities = reset_entities(current_map, tile_size)
                triggers = reset_triggers(current_map, tile_size, f"level_{level_index}")
                targets = reset_targets(current_map, tile_size,f"level_{level_index}")
                entity_mediator = EntityMediator(entities, wall_rects)
                puzzle_mediator = PuzzleMediator(entities, triggers, targets, f"level_{level_index}")
                game_over = False
            elif keys[pygame.K_m]:
                return "menu"

        # 🎯 HUD
        for entity in entities:
            if isinstance(entity, Player):
                draw_hud(window, font, entity, level_name, heart_img, dark_heart, tile_size)

        # 🔑 Triggers
        for trigger in triggers:
            trigger.update(entities)
            trigger.draw(window)

        for target in targets:
            target.update(dt)
            target.draw(window)

        # 🎮 Entidades
        for entity in entities:
            entity.draw(window)

        if level_index==0:
            # tutorial overlay
            tutorial.update()
            tutorial.draw(window)

        pygame.display.update()
