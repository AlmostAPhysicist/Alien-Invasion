import pygame
from settings import Settings

class Scoreboard():
    
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('images/scoreboard.png')
        self.image = pygame.transform.scale(self.image, (900, 300))
        self.settings = Settings()
        self.screen_rect = screen.get_rect()
        self.screen_size = screen.get_size()
        self.image = self.settings.set_size(self.image, self.screen_size, self.settings.scoreboard_size_to_screen)
        self.image.set_alpha(self.settings.scoreboard_opacity)

        self.rect = self.image.get_rect()
        self.rect.topright = self.screen_rect.topright

        self.score = 0
        self.rendered_score = 0
        self.text = str(self.rendered_score)
        self.font = self.settings.font
        self.colour = self.settings.button_text_colour
        self.text_size = self.settings.button_text_size        
        self.font = pygame.font.SysFont(self.font, self.text_size)
        self.text_image = self.font.render(self.text, True, self.colour)
        self.text_image.set_alpha(self.settings.scoreboard_opacity)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.rect.center
    

    def update(self, added_score=0):
        self.score += added_score
        if self.rendered_score < self.score:
            self.rendered_score += 1
            self.text = str(self.rendered_score)
            self.text_image = self.font.render(self.text, True, self.colour)
            self.text_image.set_alpha(self.settings.scoreboard_opacity)
            self.text_rect = self.text_image.get_rect()
            self.text_rect.center = self.rect.center
        if self.rendered_score > self.score:
            if self.rendered_score > 100:
                self.rendered_score -= int(self.rendered_score/13)
            elif self.rendered_score > 10:
                self.rendered_score -= 13
            else:
                self.rendered_score -= 1
            self.text = str(self.rendered_score)
            self.text_image = self.font.render(self.text, True, self.colour)
            self.text_image.set_alpha(self.settings.scoreboard_opacity)
            self.text_rect = self.text_image.get_rect()
            self.text_rect.center = self.rect.center
        

    def empty(self):
        self.score = 0
        

    def render(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_image, self.text_rect)

