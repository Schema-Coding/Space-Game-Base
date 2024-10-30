import pygame

class Message:
    def __init__(self, game):
        pygame.font.init()
        self.__game = game
        self.text = ""
        self.rect = None
        self.screen_rect = game.screen.get_rect()
    
    def blitme(self):
        my_font = pygame.font.SysFont("comicsansms", 36)
        text_surface = my_font.render(self.text, True, (255, 255, 255))
        self.rect = text_surface.get_rect()
        self.rect.center = self.screen_rect.center
        self.__game.screen.blit(text_surface, self.rect)