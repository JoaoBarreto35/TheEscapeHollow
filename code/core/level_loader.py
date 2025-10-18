from code.entities.EntityFactory import EntityFactory
from code.mechanics.TriggerFactory import TriggerFactory
from code.mechanics.TargetFactory import TargetFactory
from code.data.Levels import LevelsEvents

def load_level_components(current_map, tile_size, level_name):
    entities = []
    triggers = []
    targets = []

    # Entities
    entity_factory = EntityFactory(tile_size)
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            x = col_idx * tile_size
            y = row_idx * tile_size
            entity = entity_factory.create_entity(cell, (x, y))
            if entity:
                entities.append(entity)

    # Triggers
    trigger_factory = TriggerFactory(tile_size)
    all_triggers = [event["trigger"] for event in LevelsEvents[level_name]]
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            if (row_idx, col_idx) in all_triggers:
                x = col_idx * tile_size
                y = row_idx * tile_size
                trigger = trigger_factory.create_trigger(cell, (x, y), (row_idx, col_idx))
                if trigger:
                    triggers.append(trigger)

    # Targets
    target_factory = TargetFactory(tile_size)
    all_targets = {pos for event in LevelsEvents[level_name] for pos in event["targets"]}
    for row_idx, row in enumerate(current_map):
        for col_idx, cell in enumerate(row):
            if (row_idx, col_idx) in all_targets:
                x = col_idx * tile_size
                y = row_idx * tile_size
                target = target_factory.create_target(cell, (x, y), (row_idx, col_idx))
                if target:
                    targets.append(target)

    return entities, triggers, targets