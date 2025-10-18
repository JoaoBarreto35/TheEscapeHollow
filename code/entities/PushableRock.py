import pygame

from code.data.Settings import ROCK_PUSH_SPEED

stone_drag_sound = pygame.mixer.Sound("assets/sfx/stone_drag.wav")
stone_drag_sound.set_volume(0.1)

class PushableRock:
    def __init__(self, position, size):
        self.position = pygame.Vector2(position)
        self.size = size
        self.velocity = ROCK_PUSH_SPEED# mesma velocidade do player
        self.image = pygame.image.load("assets/rock.png").convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def try_push(self, direction, wall_rects, other_entities):
        offset = pygame.Vector2(0, 0)
        if direction == "up":
            offset.y = -self.velocity
        elif direction == "down":
            offset.y = self.velocity
        elif direction == "left":
            offset.x = -self.velocity
        elif direction == "right":
            offset.x = self.velocity

        new_rect = self.rect.move(offset)

        # Verifica colisão com parede
        if any(new_rect.colliderect(wall) for wall in wall_rects):
            return False

        # Verifica colisão com outras rochas
        if any(new_rect.colliderect(e.rect) for e in other_entities if isinstance(e, PushableRock) and e != self):
            return False

        # Verifica colisão com inimigos
        from code.entities.Enemy import Enemy
        if any(new_rect.colliderect(e.rect) for e in other_entities if isinstance(e, Enemy)):
            return False

        # Move a rocha
        self.position += offset
        self.rect.topleft = self.position

        if not stone_drag_sound.get_num_channels():  # evita tocar várias vezes
            stone_drag_sound.play(0)
        return True