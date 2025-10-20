from code.data.levels import LevelsEvents
from code.entities.enemy import Enemy
from code.settings import DeathReason
from code.entities.player import Player


class PuzzleMediator:
    def __init__(self, entities, triggers, targets, levelName):
        self.entities = entities
        self.triggers = triggers
        self.targets = targets
        self.levelName = levelName

    def update_all(self):
        for event in LevelsEvents[self.levelName]:
            # Verifica se algum trigger vinculado ao evento está sendo pressionado

            for trigger in self.triggers:
                if trigger.triggerMatriz == event["trigger"]:

                    for entity in self.entities:
                        if entity.rect.colliderect(trigger.rect):

                            for target in self.targets:

                                if target.targetMatriz in event["targets"]:
                                    target.toggle(True)
                            break

        # Verifica colisões de Player com targets
        for entity in self.entities:
            old_position = entity.position.copy()

            if isinstance(entity, Player):
                for target in self.targets:
                    if entity.rect.colliderect(target.rect):
                        # Verifica se o jogador caiu em um HoleTrap ativo
                        if target.__class__.__name__ == "HoleTrap" and target.active:
                            entity.death_reason = DeathReason.HOLE
                            entity.lives = 0






