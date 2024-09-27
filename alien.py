import pygame

class Alien:
    def __init__(self, position, game):
        """Create Alien enemy and set initial position"""

        self.screen = game.screen
        self.image = pygame.image.load('assets/my_spaceship_small.png')
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = position

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        