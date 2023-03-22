from pygame.sprite import Group
import random
import sys
import pygame
from bullet import Bullet
from alien import Alien
import time
from button import Button
from time import sleep
from scoreboard import Scoreboard
from lobby_scoreboard import LobbyScoreboard

class GameFunctions():
    def __init__(self, game_settings, screen, spaceship, bullets, aliens, bg_image):
    #Variables
        self.game_settings = game_settings
        self.screen = screen
        self.spaceship = spaceship
        self.bg_image = bg_image
        self.x_occupied = []
        self.x_all = list(range(screen.get_size()[0]+1))
        self.aliens_at_spawn = Group()
        self.pause_time = 0
        self.aliens_dying = Group()
        self.bullets_ending = Group()
        self.scoreboard = Scoreboard(screen)
        self.lobby_scoreboard = LobbyScoreboard(self.screen)
        self.one_game_played = False

    #Game speed and difficulty
        self.difficulty_level = 1
        self.alien_spawn_rate = self.game_settings.alien_spawn_rate
        self.alien_time_interval = 1/self.alien_spawn_rate
        self.alien_speed = self.game_settings.alien_speed
        self.score_prev_cent = 0
        self.spaceship_speed = self.game_settings.spaceship_speed
        self.bullet_speed = game_settings.bullet_speed
        # self.next_spawn = self.last_spawn + self.alien_time_interval

    #Game State
        self.game_lobby = True
        self.game_pause = False
        self.game_start = False

        self.lobby_transition = False
        self.lobby_fade_out = True
        self.slept = True

    #Buttons
        self.buttons = Group()
        self.play_button = Button(self.screen, self.game_settings, 0)
        self.play_again_button = Button(self.screen, self.game_settings, 1)
        self.quit_button = Button(self.screen, self.game_settings, 2)
        self.buttons.add(self.play_button)
        

    def check_events(self, bullets, aliens):
        """Watch for time, keyboard and mouse events and respong accordingly"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If the keyboard/mouse event asks pygame to quit...
                sys.exit()

        #Keyboard
            #Spaceship movement
            if event.type == pygame.KEYDOWN:
                self.keydown_events(event, bullets)
                                    
            if event.type == pygame.KEYUP:
                self.keyup_events(event)
            
        #Mouse
            if self.game_start is False and self.game_lobby:
                self.check_mouse_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons.sprites():
                        if button.hovered:
                            if button.text_index <= 1 :#i.e. if the button is a 'play' or 'play again' button
                                self.game_start = True
                            if button.text_index == 2:
                                sys.exit()

        #Lobby Transitions
        if self.game_start and self.game_lobby is True:
            self.lobby_transition = True
            self.lobby_fade_out = True 
            self.lobby_scoreboard.fade_flag = True

        if self.lobby_transition:
            self.transition_lobby(self.lobby_fade_out)
    
        #Time
        if self.game_lobby is False and self.game_start:
            #Creating an alien after some time interval
            self.current_time = time.time() 
            if self.game_pause is False:
                self.alien_spawns(aliens)

#Game States             
    #Lobby
    def transition_lobby(self, lobby_fade_out):
        if lobby_fade_out:
            for button in self.buttons.sprites():

                if button.image_rect.bottom <= 0:
                    self.game_lobby = False
                    self.last_spawn = time.time() + self.game_settings.break_time
                    self.next_spawn = self.last_spawn + self.alien_time_interval
                    self.lobby_transition = False
                    self.buttons.empty()
                else:
                    button.move_up()
            self.bg_image.lobby_decrease_opacity()
            if self.one_game_played:
                if self.lobby_scoreboard.fade_flag:
                    self.lobby_scoreboard.fade(True)
            
        if lobby_fade_out is False:
            if self.slept is False:
                sleep(1)
                self.slept = True
            for button in self.buttons.sprites():

                if button.image_rect.centery >= button.screen_rect.centery:
                    self.game_lobby = True
                    self.lobby_transition = False
                else:
                    button.move_down()
            self.bg_image.lobby_increase_opacity()
            if self.one_game_played:
                if self.lobby_scoreboard.fade_flag:
                    self.lobby_scoreboard.fade(False)



    #Game Pause
    def pause(self, Bool):
        self.game_pause = Bool

        if Bool:
            self.pause_time = self.current_time
        else:
            self.last_spawn += self.current_time - self.pause_time
            self.next_spawn = self.last_spawn + self.alien_time_interval
            self.pause_time = 0
    

    #Game Reset
    def reset(self, aliens, bullets):
        for alien in aliens:
            aliens.remove(alien)
            self.aliens_dying.add(alien)
        for bullet in bullets:
            bullets.remove(bullet)
            self.bullets_ending.add(bullet)
        self.scoreboard.empty()
        self.x_occupied.clear()
    #Reseting game diffuculty
        self.difficulty_level = 1
        self.alien_spawn_rate = self.game_settings.alien_spawn_rate
        self.alien_time_interval = 1/self.alien_spawn_rate
        self.alien_speed = self.game_settings.alien_speed
        self.score_prev_cent = 0
        self.spaceship_speed = self.game_settings.spaceship_speed
        self.bullet_speed = self.game_settings.bullet_speed


    #Game Difficulty
    def increase_difficulty(self):
        if self.difficulty_level < 12:
            if self.scoreboard.score >= (self.score_prev_cent + 100):
                self.score_prev_cent += 100
                self.difficulty_level += 1
                self.difficulty_factor = 1 + (self.game_settings.difficulty_increase*self.difficulty_level)
                self.alien_spawn_rate = self.game_settings.alien_spawn_rate * self.difficulty_factor
                self.alien_time_interval = 1/self.alien_spawn_rate
                self.alien_speed = self.game_settings.alien_speed * self.difficulty_factor
                if self.difficulty_level < 8:
                    self.spaceship_speed = self.game_settings.spaceship_speed * self.difficulty_factor
                    self.bullet_speed = self.game_settings.bullet_speed * self.difficulty_factor



#Events
    #Keyboard
    def keydown_events(self, event, bullets):
    #Keyboard shotcuts
        #Exiting
        if event.key == pygame.K_q:
            sys.exit()
        
        #Pausing
        if self.game_start and self.game_lobby is False:
            if event.key == pygame.K_p:
                if self.game_pause is False:
                    self.pause(True)
                elif self.game_pause is True:
                    self.pause(False)
            if self.game_pause is False:
                
    #Ship movement
                if event.key == pygame.K_RIGHT:
                    self.spaceship.moving_right = True
                if event.key == pygame.K_LEFT:
                    self.spaceship.moving_left = True
                #Firing a bullet
                if event.key == pygame.K_SPACE:
                    self.fire_bullet(bullets)
    
    def keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.spaceship.moving_left = False


    #Mouse
    def check_mouse_pos(self):
        """Check whether the mouse is hovering over a button or not"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in self.buttons.sprites():
            if button.image_rect.collidepoint(mouse_x, mouse_y):
                button.hovered = True
                button.grow()
            else:
                button.hovered = False
                button.shrink()



#Game Elements
    #Alien Spawing
    def alien_spawns(self, aliens):
        """Spawing an alien based on time"""
        if self.current_time > (self.next_spawn):
            try:

                self.last_spawn = self.current_time
                self.next_spawn = self.last_spawn + self.alien_time_interval
                self.create_alien(aliens)
            except:
                self.pause(True)

    def create_alien(self, aliens):
        alien_colour = random.choice(self.game_settings.alien_colours)
        new_alien = Alien(self.game_settings, self.screen, alien_colour)
        new_alien.set_meanx(new_alien.choose_alien_position(self.x_occupied, self.x_all))

        aliens.add(new_alien)
        for pixel in new_alien.occupied:
            self.x_occupied.append(pixel)


    #Bullet Firing
    def fire_bullet(self, bullets):
        """Shoot out a new bullet, if the maximum number of bullets allowed have not been reached"""
        if len(bullets) < self.game_settings.bullets_allowed_on_screen:
            new_bullet = Bullet(self.game_settings, self.screen, self.spaceship)
            bullets.add(new_bullet)



#Updating and rendering elements
    #Checking Collisions
    def check_alien_collisions(self, bullets, aliens):
        """Check collisions of aliens with objects such as bullets, spaceship and screen bottom, deciding the death of aliens and ending of the game"""
        for alien in aliens.copy():
            #Check Bullet hits
            for bullet in bullets.copy():
                if pygame.sprite.collide_rect(bullet, alien):
                    bullets.remove(bullet)
                    alien.alien_hp -= 1
                    if alien.alien_hp == 0:
                        aliens.remove(alien)
                        self.aliens_dying.add(alien)
                        self.scoreboard.update(alien.alien_value)
                        if alien.at_spawn:
                            for pixel in alien.occupied :
                                self.x_occupied.remove(pixel)
            #Check collision with spaceship
            if pygame.sprite.collide_rect(alien, self.spaceship) or alien.rect.bottom > self.spaceship.screen_rect.bottom :
                self.game_start = False
                self.lobby_transition = True
                self.lobby_fade_out = False  
                self.buttons.add(self.play_again_button, self.quit_button)  
                for button in self.buttons.sprites():
                    button.shrink()
                self.slept = False 
                self.lobby_scoreboard.update_prev_score(self.scoreboard.score)
                self.one_game_played = True
                self.lobby_scoreboard.fade_flag = True
                if self.lobby_scoreboard.prev_score > self.lobby_scoreboard.high_score:
                    self.lobby_scoreboard.high_score = self.lobby_scoreboard.prev_score
                    self.lobby_scoreboard.update_high_score()
                self.reset(aliens, bullets)
                


    #Spaceship And Bullets
    def update_and_render_spaceship(self):
        self.spaceship.update(self.spaceship_speed)
        self.spaceship.render()

    def update_and_render_bullets(self, bullets):
        """Render bullets and get rid of old bullets. Also, updating the position of each bullet"""
        bullets.update(self.bullet_speed)
        for bullet in bullets.copy():
            if bullet.rect.bottom > 0:
                bullet.render()
            else:
                bullets.remove(bullet)

    def update_and_render_bullets_ending(self):
        for bullet in self.bullets_ending.copy():
            bullet.death_animation()
            if bullet.opacity <= 0:
                self.bullets_ending.remove(bullet)
            else:
                bullet.render()

#.....
    def render_ending_bullets_and_aliens(self):
        for alien in self.aliens_dying:
            alien.render()
        for bullet in self.bullets_ending:
            bullet.render()
        
            # print(self.alien_spawn_rate, self.alien_speed, self.spaceship_speed, self.bullet_speed)
#.....


    #Aliens
    def update_and_render_aliens(self, aliens):
        for alien in aliens.copy():
            alien.update(self.alien_speed)        
            alien.render()
            if alien.at_spawn:
                if alien.rect.top >= 0:
                    for pixel in alien.occupied :
                        self.x_occupied.remove(pixel)
                    alien.at_spawn = False
        self.update_and_render_aliens_dying()

        
    def update_and_render_aliens_dying(self):
        for alien in self.aliens_dying.copy():
            alien.death_animation()
            if alien.opacity <= 0:
                self.aliens_dying.remove(alien)
            else:
                alien.render()    


    #Scoreboard
    def update_and_render_scoreboard(self):
        self.scoreboard.update()
        self.scoreboard.render()
        self.increase_difficulty()


    #Entire Screen
    def update_and_render_screen(self, bullets, aliens): 
        self.screen.fill(self.game_settings.bg_colour) 
        self.bg_image.render()

        if self.game_lobby or self.game_start is False:
            self.spaceship.reset(self.spaceship_speed)
            self.spaceship.render()
            if self.game_lobby:
                self.update_and_render_aliens_dying()
                self.update_and_render_bullets_ending()
            else:
                self.render_ending_bullets_and_aliens()
            self.update_and_render_scoreboard()
            
            self.bg_image.render_lobby_bg()

            for button in self.buttons.sprites():
                button.render()
            if self.one_game_played:
                self.lobby_scoreboard.render()
                

        if self.game_start and self.game_lobby is False:
            self.update_and_render_bullets(bullets)
            self.update_and_render_spaceship()
            self.update_and_render_aliens(aliens)
            self.update_and_render_scoreboard()
            # collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
            self.check_alien_collisions(bullets, aliens)
            self.bg_image.render_lobby_bg()
                        
        # #            spaceship bg_image bullets    aliens
        # objects_on_screen = 1 + 1 + len(bullets) + len(aliens) + len(self.aliens_dying)
        # print(objects_on_screen)
        pygame.display.flip() #render everything