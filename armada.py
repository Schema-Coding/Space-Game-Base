import pygame
from alien import Alien

class Armada:
    def __init__(self, game):
        """Creates a collection of aliens that are spaced evenly"""
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
        self.update_value = 1

        # Calculate Armada Dimensions
        
        self.width = self.screen_rect.right - 2 * self.horizontal_margin
        self.height = self.screen_rect.bottom // 2
        self.x = self.horizontal_margin
        self.y = self.vertical_margin

        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        # Create Dictionary of Aliens
        self.aliens = { i: Alien([0, 0], game) for i in range(0, self.rows * self.columns) }

        # Get dimensions of one alien
        self.alien_width = self.aliens[0].rect.width
        self.alien_height = self.aliens[0].rect.height
        
        # Set gutter dimensions (space between rows and columns)
        self.column_gutter_width = (self.width - self.columns * self.alien_width) / self.column_gutters
        self.row_gutter_height = (self.height - self.rows * self.alien_height) / self.row_gutters

        # Set initial position of each alien in armada
        alien_id = 0
        for row_index in range(0, self.rows):
            y = self.rect.y + row_index * (self.alien_height + self.row_gutter_height)
            for _ in range(0, self.columns):
                self.aliens[alien_id].rect.x = self.rect.x + (alien_id % self.columns) * (self.alien_width + self.column_gutter_width)
                self.aliens[alien_id].rect.y = y
                alien_id += 1

    def _position_aliens(self):
        for alien in self.aliens.values():
            alien.rect.x += self.update_value

    def blitme(self):
        for alien in self.aliens.values():
            alien.blitme()

    def update(self):
        if self.rect.x <= 0 or (self.rect.x + self.rect.width) >= self.screen_rect.right:
            self.update_value = -self.update_value
        self.rect.x += self.update_value
        self._position_aliens()