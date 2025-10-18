import pygame

from code.TutorialOverlay import TutorialOverlay


class PauseMenu:
    def __init__(self, font, width, height, hint_text):
        self.options = ["Retomar", "Tutorial", "Dicas", "Sair"]
        self.selected = 0
        self.font = font
        self.width = width
        self.height = height
        self.hint_text = hint_text

    def draw(self, surface):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        title = self.font.render("PAUSADO", True, (255, 255, 255))
        surface.blit(title, ((self.width - title.get_width()) // 2, self.height // 2 - 100))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            surface.blit(text, ((self.width - text.get_width()) // 2, self.height // 2 - 40 + i * 40))

        if self.selected == 2:  # Dicas
            hint = self.font.render(self.hint_text, True, (200, 200, 200))
            surface.blit(hint, ((self.width - hint.get_width()) // 2, self.height // 2 + 140))


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None