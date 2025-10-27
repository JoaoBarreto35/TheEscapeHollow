import json
from code.entities.enemy import Enemy
from code.settings import DeathReason
from code.entities.player import Player

class PuzzleMediator:
    def __init__(self, entities, triggers, targets, levelName):
        self.entities = entities
        self.triggers = triggers
        self.targets = targets
        self.levelName = levelName
        self.links = self._load_links(levelName)
        self.damage_cooldown = 0

    def _load_links(self, levelName):
        try:
            with open("assets/maps/events.json", "r", encoding="utf-8") as f:
                all_events = json.load(f)
            level_events = all_events.get(levelName, [])
            links = {}
            for event in level_events:
                trigger = tuple(event["trigger"])
                targets = [tuple(t) for t in event["targets"]]
                links[trigger] = targets
            return links
        except Exception as e:
            print(f"⚠️ Erro ao carregar eventos do nível {levelName}: {e}")
            return {}

    def update_all(self):

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        for trigger in self.triggers:
            trigger_pos = trigger.triggerMatriz
            if trigger_pos in self.links:
                for entity in self.entities:
                    if entity.rect.colliderect(trigger.rect):
                        for target in self.targets:
                            if target.targetMatriz in self.links[trigger_pos]:
                                target.toggle(True)
                        break
                    if trigger.__class__.__name__ == "SoundSensor" and trigger.is_pressed:
                        for target in self.targets:
                            if target.targetMatriz in self.links[trigger_pos]:
                                target.toggle(True)
                        break


        # Verifica colisões de Player com targets
        for entity in self.entities:
            if isinstance(entity, Player):
                for target in self.targets:
                    if entity.rect.colliderect(target.rect):
                        if target.__class__.__name__ == "HoleTrap" and target.active:
                            entity.death_reason = DeathReason.HOLE
                            entity.lives = 0
                        if target.__class__.__name__ == "Spikes" and target.active:
                            if self.damage_cooldown == 0:
                                entity.death_reason = DeathReason.SPIKE
                                entity.take_damage()
                                self.damage_cooldown = 60
                        if target.__class__.__name__ == "SpikesTrap" and target.active:
                            if self.damage_cooldown == 0:
                                entity.death_reason = DeathReason.SPIKE
                                entity.take_damage()
                                self.damage_cooldown = 60
