import pygame

class Alien:
    """A class to manage the ship"""
    
    def __init__(self, game):
        """Initialize the ship and set initial position"""

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.game = game

        self.image = pygame.image.load('assets/cheese_spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = self.screen_rect.topleft

    def update(self):
        ...

    def blitme(self):
        """Draw the ship at the current location"""
        self.screen.blit(self.image, self.rect)



