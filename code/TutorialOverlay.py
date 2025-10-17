import pygame


class TutorialOverlay:
    def __init__(self, image_path, duration_ms, screen_size):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.start_time = pygame.time.get_ticks()
        self.duration = duration_ms
        self.active = True

        # Redimensiona a imagem para ocupar toda a tela
        self.image = pygame.transform.scale(self.image, screen_size)

        # Cria o fundo escurecido
        self.fade_surface = pygame.Surface(screen_size)
        self.fade_surface.fill((0, 0, 0))
        self.fade_surface.set_alpha(180)  # intensidade do escurecimento

    def update(self):
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.active = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.fade_surface, (0, 0))  # fundo escuro
            surface.blit(self.image, (0, 0))         # tutorial por cima