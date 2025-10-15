import pygame
from code.Player import Player
from code.PushableRock import PushableRock
from code.Enemy import Enemy
from code.LevelExit import LevelExit

class EntityMediator:
    def __init__(self, entities, wall_rects):
        self.entities = entities
        self.wall_rects = wall_rects
        self.damage_cooldown = 0
        self.level_complete = False

    def update_all(self):
        keys = pygame.key.get_pressed()

        for entity in self.entities:
            old_position = entity.position.copy()
            entity.update()

            if any(entity.rect.colliderect(wall) for wall in self.wall_rects):
                entity.position = old_position
                entity.rect.topleft = entity.position
                if isinstance(entity, Enemy):
                    entity.reverse_direction()



            if isinstance(entity, Enemy):
                for other in self.entities:
                    if isinstance(other, PushableRock) and entity.rect.colliderect(other.rect):
                        entity.position = old_position
                        entity.rect.topleft = entity.position
                        entity.reverse_direction()

            if isinstance(entity, Player):
                for other in self.entities:
                    if isinstance(other, PushableRock):
                        if entity.rect.colliderect(other.rect):
                            if keys[pygame.K_RCTRL]:
                                pushed = other.try_push(entity.direction, self.wall_rects, self.entities)

                                if not pushed:
                                    entity.position = old_position
                                    entity.rect.topleft = entity.position
                            else:
                                entity.position = old_position
                                entity.rect.topleft = entity.position


        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        for entity in self.entities:
            if isinstance(entity, Player):
                for other in self.entities:
                    if isinstance(other, Enemy) and entity.rect.colliderect(other.rect):
                        if self.damage_cooldown == 0:
                            entity.take_damage()
                            self.damage_cooldown = 60

        for entity in self.entities:
            if isinstance(entity, Player):
                for other in self.entities:
                    if isinstance(other, LevelExit) and entity.rect.colliderect(other.rect):
                        transition_sound = pygame.mixer.Sound("assets/sfx/transition.wav")
                        transition_sound.set_volume(0.6)
                        transition_sound.play()
                        pygame.mixer.music.stop()
                        self.level_complete = True