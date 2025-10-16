import pygame
from code.Levels import LevelsEvents

class PuzzleMediator:
    def __init__(self, entities, triggers, targets):
        self.entities = entities
        self.triggers = triggers
        self.targets = targets

    def update_all(self):
        for entity in self.entities:
            for trigger in self.triggers:
                if entity.rect.colliderect(trigger.rect):
                    for event in LevelsEvents["level_2"]:
                        if trigger.triggerMatriz == event["trigger"]:
                            for target in self.targets:
                                print("Comparando:", trigger.triggerMatriz, "vs", event["trigger"])
                                if target.targetMatriz in event["targets"]:
                                    print("estado")
                                    target.toggle(True)