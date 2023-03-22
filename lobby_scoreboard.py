import pygame
from settings import Settings
import json


class LobbyScoreboard():
    
    def __init__(self, screen):
        self.settings = Settings()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.font_name = self.settings.font
        self.font_size = self.settings.lobby_scoreboard_font_size
        self.font_colour = self.settings.lobby_scoreboard_font_colour
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.max_opacity = self.settings.lobby_scoreboard_opacity
        self.opacity = 0
        self.gap = self.settings.lobby_scoreboard_gap
        self.fade_flag = False

        #Colons ':'
        self.colons_list = self.make_image(':')
        self.colons_image = self.colons_list[0]
        self.colons_rect = self.colons_list[1]
        self.colons_rect.centerx = self.screen_rect.centerx
        


        #High Score obj
        self.high_score_title_list = self.make_image('High Scrore')
        self.high_score_title_image = self.high_score_title_list[0]
        self.high_score_title_rect = self.high_score_title_list[1]
        self.high_score_title_rect.right = self.colons_rect.left
#...
        self.title_centerx = self.high_score_title_rect.centerx
        self.high_score_centery = self.screen_rect.centery + (5*self.gap)
#...
        self.high_score_title_rect.centery = self.high_score_centery

        self.get_high_score()


        #Prev Score obj
        self.prev_score_title_list = self.make_image('Previous Scrore')
        self.prev_score_title_image = self.prev_score_title_list[0]
        self.prev_score_title_rect = self.prev_score_title_list[1]

        self.prev_score_title_rect.top = self.high_score_title_rect.bottom + self.gap
        self.prev_score_centery = self.prev_score_title_rect.centery

        self.prev_score_title_rect.centerx = self.title_centerx





    def make_image(self, text):
        self.text = '    ' + str(text) + '     '
        image = self.font.render(self.text, True, self.font_colour)
        image.set_alpha(self.opacity)
        image_rect = image.get_rect()

        return [image, image_rect]
    
    def get_high_score(self):
        with open('high_score.json') as obj:
            self.high_score = int(json.load(obj))
        self.high_score_value = '     ' + str(self.high_score) + '     '
        self.high_score_value_list = self.make_image(self.high_score_value)
        self.high_score_value_image = self.high_score_value_list[0]
        self.high_score_value_rect = self.high_score_value_list[1]
        self.high_score_value_rect.left = self.colons_rect.right
        self.score_value_centerx = self.high_score_value_rect.centerx
        self.high_score_value_rect.centery = self.high_score_centery
    
    def update_high_score(self):
        with open('high_score.json', 'w') as obj:
            json.dump(self.high_score, obj)
    
    def update_prev_score(self, prev_score):
        self.prev_score = prev_score
        self.prev_score_value_list = self.make_image(self.prev_score)
        self.prev_score_value_image = self.prev_score_value_list[0]
        self.prev_score_value_rect = self.prev_score_value_list[1]
        self.prev_score_value_rect.centerx = self.score_value_centerx
        self.prev_score_value_rect.centery = self.prev_score_centery
    
    def fade(self, out):
        if out:
            if self.opacity <= 0:
                self.fade_flag = False
            else:
                self.opacity -= 10
        else:
            if self.opacity >= self.max_opacity:
                self.fade_flag = False
            else:
                self.opacity += 10

        #Colons ':'
        self.colons_list = self.make_image(':')
        self.colons_image = self.colons_list[0]
        


        #High Score obj
        self.high_score_title_list = self.make_image('High Scrore')
        self.high_score_title_image = self.high_score_title_list[0]

        self.get_high_score()
        


        #Prev Score obj
        self.prev_score_title_list = self.make_image('Previous Scrore')
        self.prev_score_title_image = self.prev_score_title_list[0]

        self.prev_score_value_list = self.make_image(self.prev_score)
        self.prev_score_value_image = self.prev_score_value_list[0]





    def render(self):
        #High score
        self.colons_rect.centery = self.high_score_centery
        self.screen.blit(self.high_score_title_image, self.high_score_title_rect)
        self.screen.blit(self.colons_image, self.colons_rect)
        self.screen.blit(self.high_score_value_image, self.high_score_value_rect)
        #Prev score
        self.colons_rect.centery = self.prev_score_centery
        self.screen.blit(self.prev_score_title_image, self.prev_score_title_rect)
        self.screen.blit(self.colons_image, self.colons_rect)
        self.screen.blit(self.prev_score_value_image, self.prev_score_value_rect)




