import pygame



class Settings():

    def __init__(self):

    #Display

        #Screen
        self.game_framerate = 45
        self.bg_colour = (10.5, 33.5, 48)
        self.screen_ratio = (16, 9)
        self.screen_size = 80
        self.screen_width = self.screen_ratio[0] * self.screen_size
        self.screen_height = self.screen_ratio[1] * self.screen_size
        self.bg_image_opacity = 80
        self.button_size_to_screen = 1/6
        self.lobby_colour = (0, 0, 0)
        self.button_animation_duration = 0.5
        self.button_text_colour = (35, 219, 243)
        self.button_text_size = int(self.screen_height/20)
        self.font = 'maiandragd'
        self.lobby_bg_opacity_max = 100
        self.lobby_bg_opacity_min = 20
        self.scoreboard_size_to_screen = 1/5
        self.scoreboard_opacity = 150
        self.lobby_scoreboard_font_size = int(self.screen_height/30)
        self.lobby_scoreboard_font_colour = (250, 250, 250)
        self.lobby_scoreboard_opacity = 200
        self.lobby_scoreboard_gap = (1/50) * self.screen_height

        #Spaceship
        self.spaceship_size_to_screen = 1/18
        self.spaceship_opacity = 200


        #Aliens
        self.alien_opacity = 250
        self.alien_death_duration = 0.5
        self.alien_opacity_decrease = self.alien_opacity/(self.alien_death_duration*self.game_framerate)
        self.alien_colours = ['red', 'green', 'blue', 'black']

        self.alien_red_size_to_screen = 1/15
        self.alien_green_size_to_screen = 1/20
        self.alien_blue_size_to_screen = 1/25
        self.alien_black_size_to_screen = 1/10
        self.alien_sizes = [self.alien_red_size_to_screen, self.alien_green_size_to_screen, self.alien_blue_size_to_screen, self.alien_black_size_to_screen]

        #Bullet
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_opacity = 250
        self.bullet_opacity_decrease = self.bullet_opacity/(self.alien_death_duration*self.game_framerate)

    #Game dynamics
        
        self.game_speed = 3
        self.break_time = 1
        self.alien_spawn_rate = 0.4
        self.difficulty_increase = 1/18

        self.time_for_spaceship = 3
        self.spaceship_alien_ratio = 2
        self.time_for_alien = self.spaceship_alien_ratio * self.time_for_spaceship
        self.time_for_bullet = 2
        self.time_for_alien_sideways = 1.5

        #Spaceship
        self.spaceship_speed = self.screen_width/(self.game_framerate*self.time_for_spaceship)

        #Bullet
        self.bullet_speed = self.screen_height/(self.game_framerate*self.time_for_bullet)
        self.bullets_allowed_on_screen = 5

        #Aliens
        self.alien_red_value = 10
        self.alien_green_value = 20
        self.alien_blue_value = 30
        self.alien_black_value = 30
        self.alien_values = [self.alien_red_value, self.alien_green_value, self.alien_blue_value, self.alien_black_value]

        self.alien_red_hp = 1
        self.alien_green_hp = 1
        self.alien_blue_hp = 1
        self.alien_black_hp = 5
        self.alien_hps = [self.alien_red_hp, self.alien_green_hp, self.alien_blue_hp, self.alien_black_hp]

        self.alien_speed = self.screen_height/(self.game_framerate*self.time_for_alien)
        self.alien_sideways_range = self.screen_width/12
        self.alien_sideways_speed = self.alien_sideways_range/(self.game_framerate*self.time_for_alien_sideways)
        



    def set_size(self, image, screen_size, image_size_to_screen):
        """Returns and image obj with a certain size, as per the ratio given (image to screen)"""
        image_size = image.get_size()
        size_factor = (screen_size[0] * image_size_to_screen)/image_size[0]
        width = image_size[0]*size_factor
        length = image_size[1]*size_factor
        dimentions = (width, length)
        image_new = pygame.transform.scale(image, dimentions)
        return image_new






        