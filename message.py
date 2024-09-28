import pygame

class message:
    def __init__(self, game, message):
        my_font = pygame.font.SysFont(None, 36)
        text_surface = my_font.render(message, True, (255, 255, 255))
        game.screen.blit(text_surface, (250, 250))