import pygame


class Overlay:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.health_surf = pygame.image.load('../graphics/health.png').convert_alpha()

    def display(self):
        for life in range(self.player.health):
            pos_x = 10 + life * (self.health_surf.get_width() + 4)
            self.display_surface.blit(self.health_surf, (pos_x, 10))
