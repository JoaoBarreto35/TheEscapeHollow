from code.data.Levels import LevelsEvents


class PuzzleMediator:
    def __init__(self, entities, triggers, targets,levelName):
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


        # Verifica colisão com portas fechadas

