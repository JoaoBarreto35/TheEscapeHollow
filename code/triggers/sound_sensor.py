import pygame
from code.mechanics.trigger import Trigger
from code.settings import SOUND_SENSOR_RAIO_TILES, PLAYER_NORMAL_SPEED


class SoundSensor(Trigger):
    def __init__(self, position, size, triggerMatriz):
        super().__init__(position, size, triggerMatriz)
        self.triggerMatriz = triggerMatriz
        self.position = pygame.Vector2(position)
        self.size = size
        self.raio = SOUND_SENSOR_RAIO_TILES  # raio em células

        self.image_off = pygame.image.load("assets/sound_sensor_off.png").convert()
        self.image_off = pygame.transform.scale(self.image_off, (size, size))
        self.image_on = pygame.image.load("assets/sound_sensor_on.png").convert()
        self.image_on = pygame.transform.scale(self.image_on, (size, size))

        self.image = self.image_off
        self.rect = self.image.get_rect(topleft=self.position)
        self.is_pressed = False
        self.draw_aura = False
        self._ultimas_posicoes = {}  # ← aqui guardamos os rastros

    def draw(self, surface):
        surface.blit(self.image_on if self.is_pressed else self.image_off, self.rect.topleft)
        self._draw_detection_aura(surface)

    def _draw_detection_aura(self, surface):
        if self.draw_aura:
            radius = self.raio * self.size
            aura = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura, (150, 150, 150, 40), (radius, radius), radius)
            surface.blit(aura, (self.rect.centerx - radius, self.rect.centery - radius))
        else:
            pass

    def update(self, entities):
        self.is_pressed = False
        radius = self.raio * self.size
        novas_posicoes = {}

        for entity in entities:
            dx = entity.rect.centerx - self.rect.centerx
            dy = entity.rect.centery - self.rect.centery
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia <= radius:
                eid = id(entity)
                pos_atual = pygame.Vector2(entity.rect.center)
                novas_posicoes[eid] = pos_atual  # salva pra atualizar depois

                if eid in self._ultimas_posicoes:
                    pos_anterior = self._ultimas_posicoes[eid]
                    delta = (pos_atual - pos_anterior).length()

                    if delta > PLAYER_NORMAL_SPEED*0.8:
                        self.is_pressed = True
                        break

        # Só atualiza as posições depois de comparar
        self._ultimas_posicoes.update(novas_posicoes)
        return self.is_pressed