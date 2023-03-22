import pygame
from pygame.sprite import Sprite


class Button(Sprite):

    def __init__(self, screen, settings, text_index):
        super(Button, self).__init__()
        buttons = ['Play', 'Play Again', 'Quit']
        self.text_index = text_index
        self.text = buttons[self.text_index]
        self.image = pygame.image.load('images/button.png')
        self.settings = settings
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.screen_rect = self.screen.get_rect()
        

        self.grow_ratio = 6/5
        self.grow_flag = True
        self.shrink_flag = False

        self.normal_image = self.settings.set_size(self.image, self.screen_size, self.settings.button_size_to_screen)
        self.grown_image = pygame.transform.rotozoom(self.normal_image, 0, self.grow_ratio)

        self.image = self.normal_image
        self.image_rect = self.image.get_rect()
        self.button_pos = {'Play': 0, 'Play Again': (self.grown_image.get_rect().width*(2/3)), 'Quit':(-(self.grown_image.get_rect().width*(2/3)))}
        self.image_rect.center = self.screen_rect.center
        self.image_rect.x += self.button_pos[self.text]
        if self.text_index > 0:
            self.image_rect.bottom = 0
        
        self.animation_duration = self.settings.button_animation_duration
        self.speed = self.screen_size[1]/(2*self.settings.game_framerate*self.animation_duration)

        #Text
        self.colour = self.settings.button_text_colour
        self.normal_text_size = self.settings.button_text_size
        self.grown_text_size = int(self.grow_ratio * self.normal_text_size)
        self.font = pygame.font.SysFont('maiandragd', self.normal_text_size)
        self.text_image = self.font.render(self.text, True, self.colour)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.image_rect.center

        self.hovered = False
        self.clicked = False

        


    def size(self):
        self.button_size = self.image.get_size()
        self.width = self.button_size[0]
        self.length = self.button_size[1]

    def grow(self):
        if self.grow_flag:
            #Button
            self.center = self.image_rect.center
            self.image = self.grown_image
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.center  
            
            #Text
            self.font = pygame.font.SysFont('maiandragd', self.grown_text_size)
            self.text_image = self.font.render(self.text, True, self.colour)
            self.text_image_rect = self.text_image.get_rect()
            self.text_image_rect.center = self.image_rect.center

            self.grow_flag = False
            self.shrink_flag = True

    def move_up(self):
        self.image_rect.y -= self.speed
        self.text_image_rect.center = self.image_rect.center
    
    def move_down(self):
        if (self.screen_rect.centery-self.image_rect.centery) > self.speed:
            self.image_rect.y += self.speed
        else:
            self.image_rect.centery = self.screen_rect.centery

        self.text_image_rect.center = self.image_rect.center




    def shrink(self):#rework
        if self.shrink_flag:
            #Button
            self.center = self.image_rect.center
            self.image = self.normal_image
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.center 
            #Text
            self.font = pygame.font.SysFont(self.settings.font, self.normal_text_size)
            self.text_image = self.font.render(self.text, True, self.colour)
            self.text_image_rect = self.text_image.get_rect()
            self.text_image_rect.center = self.image_rect.center

            self.shrink_flag = False
            self.grow_flag = True
        
        


        
    def render(self):
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.text_image, self.text_image_rect)