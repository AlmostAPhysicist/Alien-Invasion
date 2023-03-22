import pygame
from settings import Settings


class BG_Image():

    def __init__(self, screen):
        """creating a rect surface for the backgorund"""
        self.settings = Settings()
        self.bg_image = pygame.image.load('images/space_bg.jpg')
        self.bg_image.set_alpha(self.settings.bg_image_opacity)
        self.bg_image_dimentions = (self.settings.screen_width, self.settings.screen_height)
        self.bg_image = pygame.transform.scale(self.bg_image, self.bg_image_dimentions)
        self.rect = self.bg_image.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect.left = self.screen_rect.left
        self.rect.top = self.screen_rect.top

        self.lobby_bg = pygame.Surface(self.bg_image_dimentions)
        self.lobby_bg.fill(self.settings.lobby_colour)
        self.lobby_bg_rect = self.lobby_bg.get_rect()
        self.lobby_opacity_max = self.settings.lobby_bg_opacity_max
        self.lobby_opacity_min = self.settings.lobby_bg_opacity_min
        self.lobby_opacity = self.lobby_opacity_max
        self.lobby_bg.set_alpha(self.lobby_opacity)
        self.lobby_opacity_decrease = (self.lobby_opacity_max-self.lobby_opacity_min)/(self.settings.button_animation_duration*self.settings.game_framerate)

    def lobby_decrease_opacity(self):
        if self.lobby_opacity > self.lobby_opacity_decrease:
            self.lobby_opacity -= self.lobby_opacity_decrease
            self.lobby_bg.set_alpha(self.lobby_opacity)

    def lobby_increase_opacity(self):
        if self.lobby_opacity < self.lobby_opacity_max:
            self.lobby_opacity += self.lobby_opacity_decrease
            self.lobby_bg.set_alpha(self.lobby_opacity)
        
    def render(self):
        """rednering the background"""
        self.screen.blit(self.bg_image, self.rect)
    
    def render_lobby_bg(self):
        self.screen.blit(self.lobby_bg, self.lobby_bg_rect)