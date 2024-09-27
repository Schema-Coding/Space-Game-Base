import pygame
from alien import Alien

class Armada:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.game = game

        # Settings
        self.rows = 3
        self.columns = 8
        self.row_gutters = self.rows - 1
        self.column_gutters = self.columns - 1
        self.vertical_margin = 50
        self.horizontal_margin = 100

        # Calculate Armada Dimensions
        self.width = self.screen_rect.right - 2 * self.horizontal_margin
        self.height = self.screen_rect.bottom // 2

        self.screen_rect.x = self.screen_rect.midtop[0] - self.width / 2
        self.screen_rect.y = self.vertical_margin

        # Create Dictionary of Aliens
        self.aliens = { i: Alien([0, 0], game) for i in range(0, self.rows * self.columns) }

        # Get dimensions of one alien
        self.alien_width = self.aliens[0].rect.right - self.aliens[0].rect.left
        self.alien_height = self.aliens[0].rect.bottom - self.aliens[0].rect.top
        
        # Set gutter dimensions (space between rows and columns)
        self.column_gutter_width = (self.width - self.columns * self.alien_width) / self.column_gutters
        self.row_gutter_height = (self.height - self.rows * self.alien_height) / self.row_gutters

        alien_id = 0
        for row_index in range(0, self.rows):
            y = self.screen_rect.y + row_index * (self.alien_height + self.row_gutter_height)
            for column_index in range(0, self.columns):
                self.aliens[alien_id].rect.x = self.screen_rect.x + column_index * (self.alien_width + self.column_gutter_width)
                self.aliens[alien_id].rect.y = y
                alien_id += 1

    def blitme(self):
        for alien in self.aliens.values():
            alien.blitme()