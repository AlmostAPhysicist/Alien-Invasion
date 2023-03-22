import pygame



class Spaceship():

    def __init__(self, game_settings, screen):
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.settings = game_settings

    #Load the image and get it's rect (rectangle) object
        self.image = pygame.image.load('images/spaceship_maroon.png')
        self.image.set_alpha(self.settings.spaceship_opacity)

        #Resizing the ship
        self.size_to_screen = self.settings.spaceship_size_to_screen
        self.image = self.settings.set_size(self.image, self.screen_size, self.size_to_screen)
        
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #Spaceship default positioning
        self.rect.centerx = self.screen_rect.centerx #the centers of both the ship and the screen are aligned at the same x coordinate
        self.rect.bottom = self.screen_rect.bottom #the bottoms of both the ship and the screen are aligned at the same y coordinate
        self.center = float(self.rect.centerx)

    # Movement flags
        self.moving_right = False
        self.moving_left = False

    def move_right(self, speed):
        self.center += speed

    def move_left(self, speed):
        self.center -= speed

    def update(self, speed):
        """Updating the spaceship's position based on the movement flags"""
        if self.moving_left and self.rect.left > 0:
            self.move_left(speed)
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.move_right(speed)
        self.rect.centerx = self.center

    def reset(self, speed):
        if self.center != self.screen_rect.centerx:
            gap = self.screen_rect.centerx - self.center 
            if self.center < self.screen_rect.centerx:
                if gap > speed:
                    self.move_right(speed)
                else:
                    self.move_right(gap)
            else:
                if -gap > speed:
                    self.move_left(speed)
                else:
                    self.move_left(-gap)
            self.rect.centerx = self.center

    def render(self):
        """Render the ship at it's current location"""
        self.screen.blit(self.image, self.rect)