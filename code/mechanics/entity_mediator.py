import pygame

from code.settings import DeathReason
from code.entities.life_chest import LifeChest
from code.entities.player import Player
from code.entities.pushable_rock import PushableRock
from code.entities.enemy import Enemy
from code.entities.level_exit import LevelExit
from code.entities.secret_door import SecretDoor

class EntityMediator:
    def __init__(self, entities, wall_rects):
        # Lista de entidades presentes na cena
        self.entities = entities
        # Lista de retângulos que representam paredes
        self.wall_rects = wall_rects
        # Cooldown para evitar dano contínuo ao jogador
        self.damage_cooldown = 0
        # Flag que indica se o jogador chegou à saída do nível
        self.level_complete = False

    def update_all(self):
        # Captura o estado atual das teclas pressionadas
        keys = pygame.key.get_pressed()

        # Atualiza todas as entidades e trata colisões com paredes e rochas
        for entity in self.entities:
            old_position = entity.position.copy()
            entity.update()


            # Verifica colisão com parede
            if any(entity.rect.colliderect(wall) for wall in self.wall_rects):
                entity.position = old_position
                entity.rect.topleft = entity.position
                # Inimigos mudam de direção ao colidir com parede
                if isinstance(entity, Enemy):
                    entity.reverse_direction()

            # Verifica colisão entre inimigo e rocha
            if isinstance(entity, Enemy):
                for other in self.entities:
                    if isinstance(other, PushableRock) and entity.rect.colliderect(other.rect):
                        entity.position = old_position
                        entity.rect.topleft = entity.position
                        # Se for uma porta secreta ativa, ignora reversão
                        if isinstance(other, SecretDoor) and other.active:
                            pass
                        else:
                            entity.reverse_direction()

            # Verifica colisão entre jogador e rocha (tentativa de empurrar)
            if isinstance(entity, Player):
                for other in self.entities:
                    if isinstance(other, PushableRock) and entity.rect.colliderect(other.rect):
                        if keys[pygame.K_SPACE]:
                            # Tenta empurrar a rocha na direção do jogador
                            pushed = other.try_push(entity.direction, self.wall_rects, self.entities)
                            if not pushed:
                                # Se não conseguiu empurrar, desfaz movimento
                                entity.position = old_position
                                entity.rect.topleft = entity.position
                        else:
                            # Se não pressionou espaço, desfaz movimento
                            entity.position = old_position
                            entity.rect.topleft = entity.position

        # Reduz o cooldown de dano ao jogador
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Verifica colisão entre jogador e inimigo (aplica dano)
        for entity in self.entities:
            if isinstance(entity, Player):
                for other in self.entities:
                    if isinstance(other, Enemy) and entity.rect.colliderect(other.rect):
                        if self.damage_cooldown == 0:
                            entity.death_reason = DeathReason.ENEMY
                            entity.take_damage()
                            self.damage_cooldown = 60

        # Verifica colisão entre jogador e saída do nível
        for entity in self.entities:
            if isinstance(entity, Player):
                for other in self.entities:
                    if isinstance(other, LevelExit) and entity.rect.colliderect(other.rect):
                        # Toca som de transição e marca nível como completo
                        transition_sound = pygame.mixer.Sound("assets/sfx/transition.wav")
                        transition_sound.set_volume(0.6)
                        transition_sound.play()
                        pygame.mixer.music.stop()
                        self.level_complete = True

        # Verifica colisão entre jogador e baú de vida
        for entity in self.entities:
            if isinstance(entity, Player):
                for other in self.entities:
                    if isinstance(other, LifeChest) and not other.opened:
                        if entity.rect.colliderect(other.rect):
                            # Concede uma vida ao jogador e abre o baú
                            entity.lives = min(entity.lives + 1, 5)
                            other.open()
