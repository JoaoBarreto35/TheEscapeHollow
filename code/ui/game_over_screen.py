import pygame

class GameOverScreen:
    def __init__(self, font, width, height, hint_text=""):
        self.options = ["Tentar novamente", "Voltar ao menu"]
        self.selected = 0
        self.font = font
        self.width = width
        self.height = height
        self.hint_text = hint_text
        self.played_sound = False  # ← Adiciona o atributo aqui

        try:
            self.sound = pygame.mixer.Sound("assets/sfx/game_over.wav")
        except:
            self.sound = None

    def draw(self, surface):
        # Máscara escura
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Título
        title = self.font.render("GAME OVER", True, (255, 0, 0))
        surface.blit(title, ((self.width - title.get_width()) // 2, self.height // 2 - 100))

        # Opções
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            surface.blit(text, ((self.width - text.get_width()) // 2, self.height // 2 - 40 + i * 40))

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