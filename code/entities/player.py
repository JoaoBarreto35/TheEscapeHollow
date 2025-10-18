import pygame
from code.entities.entity import Entity
from code.core.image_loader import load_spritesheet
from code.settings import PLAYER_NORMAL_SPEED, DeathReason


class Player(Entity):
    def __init__(self, position, scale=2):
        animations = load_spritesheet("assets/player_spritesheet.png", frame_count=6, scale=scale)
        super().__init__(position, animations)

        self.speed = PLAYER_NORMAL_SPEED
        self.lives = 3
        self.step_timer = 0
        self.rect.topleft = position

        self.step_sound = self._load_sound("assets/sfx/step.wav", volume=0.03)
        self.damage_sound = self._load_sound("assets/sfx/damage.wav", volume=0.6)
        self.gameover_sound = self._load_sound("assets/sfx/gameover.wav", volume=0.6)

        self.death_reason = DeathReason.UNKNOWN

    def _load_sound(self, path, volume=1.0):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"[Player] Erro ao carregar som: {path} → {e}")
            return None

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

        if moving and self.step_sound and now - self.step_timer > 200:
            self.step_sound.play(0)
            self.step_timer = now

        self.rect.topleft = self.position
        self.animate()

    def take_damage(self):
        self.lives -= 1
        pygame.mixer.music.stop()
        if self.lives <= 0 and self.gameover_sound:
            self.gameover_sound.play()
        elif self.damage_sound:
            self.damage_sound.play()