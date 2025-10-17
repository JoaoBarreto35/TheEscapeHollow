import pygame
from code.Entity import Entity
from code.ImageLoader import load_player_spritesheet
from code.Settings import PLAYER_NORMAL_SPEED

# Carrega som de passo
step_sound = pygame.mixer.Sound("assets/sfx/step.wav")
step_sound.set_volume(0.03)
damage_sound = pygame.mixer.Sound("assets/sfx/damage.wav")
damage_sound.set_volume(0.6)
gameover_sound = pygame.mixer.Sound("assets/sfx/gameover.wav")
gameover_sound.set_volume(0.6)


class Player(Entity):
    def __init__(self, position, scale=2):
        raw_animations = load_player_spritesheet("assets/player_spritesheet.png")
        animations = {
            direction: [pygame.transform.scale(frame, (frame.get_width() * scale, frame.get_height() * scale))
                        for frame in frames]
            for direction, frames in raw_animations.items()
        }
        super().__init__(position, animations)
        self.speed = PLAYER_NORMAL_SPEED
        self.lives = 3
        self.step_timer = 0
        self.rect.topleft = position

    def update(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        moving = False

        if keys[pygame.K_UP]:
            self.position.y -= self.speed
            self.direction = "up"
            moving = True
        elif keys[pygame.K_DOWN]:
            self.position.y += self.speed
            self.direction = "down"
            moving = True
        elif keys[pygame.K_LEFT]:
            self.position.x -= self.speed
            self.direction = "left"
            moving = True
        elif keys[pygame.K_RIGHT]:
            self.position.x += self.speed
            self.direction = "right"
            moving = True

        if moving and now - self.step_timer > 200:
            step_sound.play(0)
            self.step_timer = now

        self.rect.topleft = self.position
        self.animate()

    def take_damage(self):
        self.lives -= 1
        if self.lives <= 0:
            gameover_sound.play()
        pygame.mixer.music.stop()
        damage_sound.play()