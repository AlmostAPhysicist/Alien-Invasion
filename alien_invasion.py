import pygame
from settings import Settings
from spaceship import Spaceship
from game_functions import *
from bg_image import BG_Image
from pygame.sprite import Group


def run_game():

    #Initialize background settings and create screen
    pygame.init()
    game_settings = Settings()

    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    spaceship = Spaceship(game_settings, screen)
    bg_image = BG_Image(screen)
    bullets = Group()
    aliens = Group()

    gf = GameFunctions(game_settings, screen, spaceship, bullets, aliens, bg_image)
    clock = pygame.time.Clock()

    #Start t he main loop for the game
    while True:
        gf.check_events(bullets, aliens)
        clock.tick(game_settings.game_framerate)
        if gf.game_pause is False:
            gf.update_and_render_screen(bullets, aliens)
        
        

        
        


run_game()
  