import pygame

from code.settings import DeathReason


class GameOverScreen:
    def __init__(self, font, width, height, death_reason=DeathReason.UNKNOWN):
        self.options = ["Tentar novamente", "Voltar ao menu"]
        self.selected = 0
        self.font = font
        self.width = width
        self.height = height
        self.death_reason = death_reason
        self.played_sound = False

        try:
            self.sound = pygame.mixer.Sound("assets/sfx/game_over.wav")
            self.sound.set_volume(0.8)
        except Exception:
            self.sound = None

    def get_death_message(self):
        if self.death_reason == DeathReason.HOLE:
            return "Você caiu em um buraco sem fim…"
        elif self.death_reason == DeathReason.ENEMY:
            return "Você foi derrotado por um inimigo."
        elif self.death_reason == DeathReason.TRAP:
            return "Você foi pego por uma armadilha."
        elif self.death_reason == DeathReason.TIMEOUT:
            return "O tempo acabou."
        elif self.death_reason == DeathReason.SPIKE:
            return "Cuidado com os espinho..."
        else:
            return "Você foi derrotado."

    def draw(self, surface):
        # Máscara escura
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Título
        title = self.font.render("GAME OVER", True, (255, 0, 0))
        surface.blit(title, ((self.width - title.get_width()) // 2, self.height // 2 - 120))

        # Mensagem personalizada
        message = self.get_death_message()
        message_text = self.font.render(message, True, (255, 255, 255))
        surface.blit(message_text, ((self.width - message_text.get_width()) // 2, self.height // 2 - 80))

        # Opções
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            surface.blit(text, ((self.width - text.get_width()) // 2, self.height // 2 - 20 + i * 40))

        # Som de derrota (toca só uma vez)
        if not self.played_sound and self.sound:
            self.sound.play()
            self.played_sound = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None