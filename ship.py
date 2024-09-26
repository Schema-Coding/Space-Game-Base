import pygame

class Ship:
    """A class to manage the ship"""
    
    def __init__(self, game):
        """Initialize the ship and set initial position"""

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.game = game

        self.image = pygame.image.load('assets/my_spaceship_small.png')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom middle of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement Flags
        self.is_moving_left = False
        self.is_moving_right = False

        # Bullets
        self.BULLET_EVENT = pygame.USEREVENT + 1

    def update(self):
        if self.is_moving_left:
            if self.rect.left > self.screen_rect.left:
                self.rect.x -= self.game.settings.ship_speed
        if self.is_moving_right:
            #print("moving right")
            self.rect.x += 1
            
=======
            if self.rect.right < self.screen_rect.right:
                self.rect.x += self.game.settings.ship_speed
>>>>>>> Stashed changes

    def blitme(self):
        """Draw the ship at the current location"""
        self.screen.blit(self.image, self.rect)



