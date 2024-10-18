from keybinding import Keybinding
import pygame

class Settings:
    def __init__(self):
        """A class that stores and initializes game settings"""
        self.screen_width = 1000
        self.screen_height = 600
        self.background_color = (18, 2, 31)
        self.max_fps = 60

        # Keybindings
        self.move_left_keybinding = Keybinding([pygame.K_a, pygame.K_LEFT])
        self.move_right_keybinding = Keybinding([pygame.K_d, pygame.K_RIGHT])
        self.fire_bullet_keybinding = Keybinding([pygame.K_SPACE])

        # Bullet Settings
        self.bullet_fire_rate = 6 # per second
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (150, 150, 150)

        # Ship Settings
        self.ship_speed = 2