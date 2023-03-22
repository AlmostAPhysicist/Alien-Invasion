from math import ceil, floor
import random
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class representing a single Alien"""


    def __init__(self, game_settings, screen, colour):
        """Initialize the alien and set its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.settings = game_settings

        #Loading an alien image and setting it's attributes
        self.alien_colour = colour
        self.alien_colour_index = self.settings.alien_colours.index(self.alien_colour)
        self.alien_value = self.settings.alien_values[self.alien_colour_index]
        self.alien_hp = self.settings.alien_hps[self.alien_colour_index]
        self.alien_size_to_screen = self.settings.alien_sizes[self.alien_colour_index]


        self.image_path = 'images/alien_{}.png'.format(self.alien_colour)
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.rotate(self.image, 180)
        self.opacity = self.settings.alien_opacity
        self.image.set_alpha(self.opacity)
        self.image = self.settings.set_size(self.image, self.screen_size, self.alien_size_to_screen)

        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.image_width = self.size[0]
        self.width = self.image_width + self.settings.alien_sideways_range
        self.half_width = self.width/2
        
        self.mean_center = 0
        self.centerx = 0
        self.rect.bottom = 0
        self.bottom = self.rect.bottom
        self.move_range = range(-floor(self.settings.alien_sideways_range/2), (floor(self.settings.alien_sideways_range/2) + 1))
        self.move = 0
        self.position = 0
        self.single_step = self.settings.alien_sideways_speed
        self.at_spawn = True

        
    
    def set_meanx(self, x_coordinate):
        self.mean_center = x_coordinate
        self.centerx = x_coordinate
        self.rect.centerx = self.centerx
        self.left_most = self.mean_center - ceil(self.half_width)
        self.right_most = self.mean_center + ceil(self.half_width)
        self.occupied = range(self.left_most, self.right_most + 1, 2)

    def choose_alien_position(self, x_occupied, x_all):
        self.x_unavailable = []
        self.x_available = []
        screen_width = len(x_all)
        for pixel_alien in range(0, ceil(self.half_width) + 1):
            self.x_unavailable.append(pixel_alien)
            self.x_unavailable.append(screen_width - pixel_alien)
            
        
            for pixel in x_occupied:
                self.pixel_unavailable_left = pixel - pixel_alien
                self.pixel_unavailable_right = pixel + pixel_alien
                if pixel not in self.x_unavailable:
                    self.x_unavailable.append(pixel)
                if self.pixel_unavailable_left not in self.x_unavailable:
                    self.x_unavailable.append(self.pixel_unavailable_left)
                if self.pixel_unavailable_right not in self.x_unavailable:
                    self.x_unavailable.append(self.pixel_unavailable_right)
        for pixel in x_all:
            if pixel not in self.x_unavailable:
                self.x_available.append(pixel)

        position_x = random.choice(self.x_available)

        return position_x

    def move_down(self, speed):
        self.bottom += speed
        self.rect.bottom = self.bottom
    
    def move_sideways(self):        
        
        if self.move == 0:
            self.move = random.choice(self.move_range)
            self.move -= self.position
            # self.position += self.move
            # self.centerx += self.move
            # self.rect.centerx = self.centerx
            # self.move = 0

            
        
        if self.move < 0:
            if self.move < (-self.single_step):
                self.position -= self.single_step
                self.centerx -= self.single_step
                self.rect.centerx = self.centerx
                self.move += self.single_step
            if self.move >= (-self.single_step):
                self.position += self.move
                self.centerx += self.move
                self.rect.centerx = self.centerx
                self.move = 0
        if self.move > 0:
            if self.move > (self.single_step):
                self.position += self.single_step
                self.centerx += self.single_step
                self.rect.centerx = self.centerx
                self.move -= self.single_step
            if self.move <= self.single_step:
                self.position += self.move
                self.centerx += self.move
                self.rect.centerx = self.centerx
                self.move = 0
        

        #Execute the moves until alien has travelled as much as he was meant to across several loops

    def death_animation(self):
        self.center = self.rect.center
        self.opacity -= self.settings.alien_opacity_decrease
        self.image.set_alpha(self.opacity)
        self.rect = self.image.get_rect()
        self.rect.center = self.center



        


    def update(self, speed):
        self.move_down(speed)
        self.move_sideways()

        




    def render(self):
        self.screen.blit(self.image, self.rect)


        


        

        
        
        
                
