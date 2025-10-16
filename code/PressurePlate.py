import pygame

from code.Trigger import Trigger


class PressurePlate(Trigger):

    def __init__(self, position, size,triggerMatriz):
        super().__init__(position, size, triggerMatriz,)
        self.triggerMatriz = triggerMatriz
        self.position = pygame.Vector2(position)
        self.size = size
        self.image_off = pygame.image.load("assets/pressure_plate_off.png").convert()
        self.image_off = pygame.transform.scale(self.image_off, (size, size))
        self.image_on = pygame.image.load("assets/pressure_plate_on.png").convert()
        self.image_on = pygame.transform.scale(self.image_on, (size, size))

        self.is_pressed = False

        self.image = self.image_off
        self.rect = self.image.get_rect(topleft=self.position)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.is_pressed:
            surface.blit(self.image_on, self.rect.topleft)
        else:
            surface.blit(self.image_off, self.rect.topleft)

    def update(self, entity):
        if entity.rect.colliderect(self.rect):
            self.is_pressed = True
            return True

        else:
            self.is_pressed = False
            return False


