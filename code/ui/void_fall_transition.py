import pygame


class VoidFallTransition:
    def __init__(self, player, font, width, height):
        self.player = player
        self.font = font
        self.width = width
        self.height = height
        self.timer = 0
        self.duration = 2000  # 2 segundos
        self.fall_speed = 2
        self.sound_played = False

        try:
            self.fall_sound = pygame.mixer.Sound("assets/sfx/fall.wav")
            self.fall_sound.set_volume(0.8)
        except:
            self.fall_sound = None

    def update(self, dt):
        self.timer += dt
        self.player.position.y += self.fall_speed
        self.player.rect.topleft = self.player.position

        if not self.sound_played and self.fall_sound:
            self.fall_sound.play()
            self.sound_played = True

    def draw(self, surface):
        surface.fill("black")
        self.player.draw(surface)

        text = self.font.render("Você está caindo no vazio...", True, (255, 255, 255))
        surface.blit(text, ((self.width - text.get_width()) // 2, self.height // 2 - 40))

    def is_finished(self):
        return self.timer >= self.duration