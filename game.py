import sys
import math
from random import randint

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet, EnemyBullet
from armada import Armada
from message import Message
from hand_tracking import LeapHandler

class NotSpaceInvaders:
    """Totally *not* a reskinned version of Space Invaders.
       Also, this class manages all game assets and behavior. Just FYI.
    """

    def __init__(self):
        """Define what happens when the game starts, and also create game resources."""
        self.settings = Settings()

        # Create Pygame Objects
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Definitely NOT Space Invaders")
        self.clock = pygame.time.Clock()

        # Create Game Objects
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.armada = Armada(self)
        self.message = Message(self)
        
        # Create User Event Types
        self.LEVEL_EVENT = pygame.USEREVENT + 1

        # Create Custom Events
        self.SHIP_BULLET_EVENT = pygame.USEREVENT + 2
        self.ENEMY_BULLET_EVENT = pygame.USEREVENT + 3
        self.MESSAGE_TIMEOUT_EVENT = pygame.USEREVENT + 4
        self.WIN_EVENT = pygame.event.Event(self.LEVEL_EVENT, outcome="win")
        self.LOSE_EVENT = pygame.event.Event(self.LEVEL_EVENT, outcome="lose")
        self.LEVEL_WARMUP_EVENT = pygame.event.Event(self.LEVEL_EVENT, outcome="")
        self.H_PINCH = pygame.event.Event(pygame.KEYDOWN, key="H_PINCH")
        self.H_UNPINCH = pygame.event.Event(pygame.KEYUP, key="H_PINCH")
        self.SECOND_EVENT = pygame.USEREVENT + 5

        self.leap = LeapHandler(self.H_PINCH, self.H_UNPINCH, self.screen, self.ship)

        self.block_controls()
        self.block_enemy_fire()
        pygame.time.set_timer(self.ENEMY_BULLET_EVENT, math.floor(1000 / self.armada.bullet_rate))
        pygame.time.set_timer(self.LEVEL_WARMUP_EVENT, 5000, 1)
        pygame.time.set_timer(self.SECOND_EVENT, 1000)
        self.display_message("Get Ready...", 1)
        self.level_warmup_duration = 5
        self.countdown = self.level_warmup_duration

    def run_game(self):
        """Here's the main loop containing all functions that run every frame of our game."""
        while True:
            self._check_events()
            self._draw_frame()
            self._check_hitboxes()
            self.bullets.update()
            self.enemy_bullets.update()
            self.ship.update()
            self.armada.update()
            self.clock.tick(self.settings.max_fps)

    def _draw_frame(self):
        """Draw all objects to the screen in their current position"""
        self.screen.fill(self.settings.background_color)
        self.ship.blitme()
        self.armada.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.enemy_bullets.sprites():
            bullet.draw_bullet()
        self.message.blitme()
        # Make the most-recently-drawn scene visible (Draw frame to screen)
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            # Exit Event
            if event.type == pygame.QUIT:
                sys.exit()
            # Keydown Events
            if self._check_keydown_event(event, self.settings.move_left_keybinding):
                self.ship.is_moving_left = True
                
            elif self._check_keydown_event(event, self.settings.move_right_keybinding):
                self.ship.is_moving_right = True
            
            if self._check_keydown_event(event, self.settings.fire_bullet_keybinding):
                self._fire_bullet()
                pygame.time.set_timer(self.SHIP_BULLET_EVENT,  math.floor(1000 / self.settings.bullet_fire_rate))

            # Keyup Events
            if self._check_keyup_event(event, self.settings.move_left_keybinding):
                self.ship.is_moving_left = False

            if self._check_keyup_event(event, self.settings.move_right_keybinding):
                self.ship.is_moving_right = False

            if self._check_keyup_event(event, self.settings.fire_bullet_keybinding):
                pygame.time.set_timer(self.SHIP_BULLET_EVENT, 0)

            # User Events
            if event.type == self.SHIP_BULLET_EVENT:
                self._fire_bullet()
            if event.type == self.ENEMY_BULLET_EVENT:
                self._fire_enemy_bullet()

            if event.type == self.LEVEL_EVENT:
                if event.outcome == "win":
                    self.display_message("Skibidi!")
                if event.outcome == "lose":
                    self.display_message("Wow, you suck!")

            if event.type == self.MESSAGE_TIMEOUT_EVENT:
                self.message.text = ""

            if event == self.LEVEL_WARMUP_EVENT:
                self.unblock_controls()
                self.unblock_enemy_fire()
                print("unblocked")

            if event.type == self.SECOND_EVENT:
                if self.countdown > 0:
                    self.display_message(str(self.countdown))
                    self.countdown -= 1
                else:
                    self.display_message("Let's Play!")
                    pygame.time.set_timer(self.SECOND_EVENT, 0)
                    


    def _check_keydown_event(self, event, keybinding):
        """Returns true if specified keys are pressed"""
        if event.type == pygame.KEYDOWN:
            key_events = [event.key == key for key in keybinding.keys]
            if any(key_events):
                return True
            
    def _check_keyup_event(self, event, keybinding):
        """Returns true if specified keys are unpressed"""
        if event.type == pygame.KEYUP:
            key_events = [event.key == key for key in keybinding.keys]
            if any(key_events):
                return True
            
    def _fire_bullet(self):
        """Create a new bullet and add it to our group of bullet sprites"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _fire_enemy_bullet(self):
        if len(self.armada.aliens) <= 1:
            random_index = 0
        else:
            random_index = randint(1, len(self.armada.aliens)) - 1
        alien_index_pool = list(self.armada.aliens.keys())
        alien_index = alien_index_pool[random_index]
        random_alien = self.armada.aliens[alien_index]
        new_bullet = EnemyBullet(self, random_alien)
        self.enemy_bullets.add(new_bullet)

    def _check_hitboxes(self):
        for bullet in self.bullets.sprites():
            hit_aliens = bullet.rect.collidedictall(self.armada.aliens, 1)
            if hit_aliens:
                bullet.kill()
                for k, _ in hit_aliens:
                    del self.armada.aliens[k]
                    self.armada.resize()
        
        for bullet in self.enemy_bullets.sprites():
            is_ship_hit = bullet.rect.colliderect(self.ship.rect)
            if is_ship_hit:
                bullet.kill()
                self.ship.lives -= 1
                if not self.ship.lives:
                    pygame.event.post(self.LOSE_EVENT)

    def display_message(self, message, seconds=3):
        self.message.text = message
        pygame.time.set_timer(self.MESSAGE_TIMEOUT_EVENT, seconds * 1000, 1)

    def block_controls(self):
        pygame.event.set_blocked((pygame.KEYUP, pygame.KEYDOWN))

    def unblock_controls(self):
        pygame.event.set_allowed((pygame.KEYUP, pygame.KEYDOWN))

    def block_enemy_fire(self):
        pygame.event.set_blocked(self.ENEMY_BULLET_EVENT)
    
    def unblock_enemy_fire(self):
        pygame.event.set_allowed(self.ENEMY_BULLET_EVENT)
                

if __name__ == '__main__':
    # Instantiate the main app class and run the game.
    nsi = NotSpaceInvaders()
    nsi.run_game()