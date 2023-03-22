import pygame
from pygame.sprite import Sprite
from settings import Settings


class Bullet(Sprite):

    def __init__(self, game_settings, screen, spaceship):
        '''To create a bullet object at the spaceship's current position'''

        super(Bullet, self).__init__()
        self.screen = screen
        self.settings = Settings()

        #Creating the bullet rect, and setting the current position
        self.image = pygame.image.load('images/bullet_teardrop.png')
        self.image.set_alpha(self.settings.bullet_opacity)
        self.dimentions = (game_settings.bullet_width, game_settings.bullet_height)
        self.image = pygame.transform.scale(self.image, self.dimentions)
        self.rect = self.image.get_rect()
        # self.rect = pygame.Rect(0, 0, game_settings.bullet_width, game_settings.bullet_height)

        self.color = 60, 60, 60
        self.rect.centerx = spaceship.rect.centerx
        self.rect.top = spaceship.rect.top

        #Store current position (on the y axis) as a floating point value
        self.y = float(self.rect.y)

        self.opacity = self.settings.bullet_opacity


    def update(self, speed):
        """Moves the bullet up"""
        self.y -= speed
        self.rect.y = self.y
    
    def death_animation(self):
        self.center = self.rect.center
        self.opacity -= self.settings.bullet_opacity_decrease
        self.image.set_alpha(self.opacity)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def render(self):#you call it update because later on, the bullets.update() will call update()
        """rednering the bullet"""
        self.screen.blit(self.image, self.rect)
        # pygame.draw.rect(self.screen, self.color, self.rect)


