import json
from code.mechanics.entity_factory import EntityFactory
from code.mechanics.trigger_factory import TriggerFactory
from code.mechanics.target_factory import TargetFactory

def load_level_components(current_map, tile_size, level_name):

    entities = []
    triggers = []
    targets = []
    links = {}
    trigger_positions = set()
    target_positions = set()

    # 🔗 Carrega eventos dinamicamente do JSON
    with open("assets/maps/events.json", "r", encoding="utf-8") as f:
        all_events = json.load(f)

    level_events = all_events.get(level_name, [])

    # Reconstrói os vínculos
    for event in level_events:
        trigger = tuple(event["trigger"])
        targets_list = [tuple(t) for t in event["targets"]]
        links[trigger] = targets_list
        trigger_positions.add(trigger)
        target_positions.update(targets_list)

    # 🧍 Entities
    entity_factory = EntityFactory(tile_size)
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            x = col_idx * tile_size
            y = row_idx * tile_size
            entity = entity_factory.create_entity(cell, (x, y))
            if entity:
                entities.append(entity)

    # 🔘 Triggers
    trigger_factory = TriggerFactory(tile_size)
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            if (row_idx, col_idx) in trigger_positions:
                x = col_idx * tile_size
                y = row_idx * tile_size
                trigger = trigger_factory.create_trigger(cell, (x, y), (row_idx, col_idx))
                if trigger:
                    triggers.append(trigger)

    # 🎯 Targets
    target_factory = TargetFactory(tile_size)
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            if (row_idx, col_idx) in target_positions:
                x = col_idx * tile_size
                y = row_idx * tile_size
                target = target_factory.create_target(cell, (x, y), (row_idx, col_idx))
                if target:
                    targets.append(target)
    print("Level name:", level_name)
    print("Triggers esperados:", trigger_positions)
    print("Targets esperados:", target_positions)
    return entities, triggers, targets#, links