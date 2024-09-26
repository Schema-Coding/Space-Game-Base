import sys

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class NotSpaceInvaders:
    """Totally *not* a reskinned version of Space Invaders.
        Also, this class manages all game assets and behavior. Just FYI.
    """

    def __init__(self):
        """Define what happens when the game starts, and also create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Definitely NOT Space Invaders")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

    def run_game(self):
        """Here's the loop that contains the functions that runs every frame of our game."""
        while True:
            self._check_events()
            self._draw_frame()
            self.bullets.update()
            self.ship.update()
            self.clock.tick(self.settings.max_fps)

    def _draw_frame(self):
        self.screen.fill(self.settings.background_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Make the most-recently-drawn scene visible (Draw frame to screen)
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            # Exit Event
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Keydown Events
            if self._check_keydown_events(event, self.settings.move_left_keybinding):
                self.ship.is_moving_left = True
                
            elif self._check_keydown_events(event, self.settings.move_right_keybinding):
                self.ship.is_moving_right = True
            
            if self._check_keydown_events(event, self.settings.fire_bullet_keybinding):
                self._fire_bullet()
                pygame.time.set_timer(self.ship.BULLET_EVENT,  1000 // self.settings.bullet_fire_rate)

            # Keyup Events
            if self._check_keyup_events(event, self.settings.move_left_keybinding):
                self.ship.is_moving_left = False

            if self._check_keyup_events(event, self.settings.move_right_keybinding):
                self.ship.is_moving_right = False

            if self._check_keyup_events(event, self.settings.fire_bullet_keybinding):
                pygame.time.set_timer(self.ship.BULLET_EVENT, 0)

            # User Events
            if event.type == self.ship.BULLET_EVENT:
                self._fire_bullet()

    def _check_keydown_events(self, event, keybinding):
        if event.type == pygame.KEYDOWN:
            key_events = [event.key == key for key in keybinding.keys]
            if any(key_events):
                return True
            
    def _check_keyup_events(self, event, keybinding):
        if event.type == pygame.KEYUP:
            key_events = [event.key == key for key in keybinding.keys]
            if any(key_events):
                return True
            
    def _fire_bullet(self):
        """Create a new bullet and add it to our group of bullet sprites"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

if __name__ == '__main__':
    # Instantiate the main app class and run the game.
    nsi = NotSpaceInvaders()
    nsi.run_game()