import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.color = self.settings.bullet_color
        #self.width = self.settings.bullet_width
        #self.height = self.settings.bullet_height
        self.speed = self.settings.bullet_speed

        self.y = float(self.rect.y)

        self.image = pygame.image.load("assets/cheese_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop

    def update(self):
        """Move the bullet up the screen"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
        