import time
from typing import Set
import pygame
from pygame import mouse
from pygame.rect import Rect
from pygame import mixer_music
from pygame.version import PygameVersion
import os
import random

pygame.font.init()

class Settings:         #Klasse die Werte einspeichert
    (window_width, window_height) = (1800, 1080)
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "Images")
    fps = 60
    caption = "Tankbuster" 
    max_nof_tanks = 15 
    timer_spawn = 0 
    game_score = 0 
    spawn_delay = 1
    max_size = 150
    delay_spawn = 1
    tank_size = 5
    Tankgewehr_scaleH = 200
    Tankgewehr_scaleV = 600
    Vergrößern_1 = 0
    Vergrößern_2 = 1

    #Farben
    color_white = (255,255,255)
    color_black = (0,50,200)
    #Schrift
    font = pygame.font.SysFont('', 30)
    game_font = pygame.font.SysFont('', 90)

class Background(object): # Hintergrund
    def __init__(self, filename="bg.jpg"):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

  

class Tank(pygame.sprite.Sprite): # Die Panzer die reinspawnen 
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, "Tank.png")).convert_alpha()
        self.scale = Settings.tank_size
        self.image = pygame.transform.scale(self.image_original, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, Settings.window_width - 25)
        self.rect.top = random.randint(0, Settings.window_height - 25)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def update(self):
        old_center = self.rect.center
        self.image = pygame.transform.scale(self.image_original, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        Settings.Vergrößern_1 += 0.2
        if Settings.Vergrößern_1 >= Settings.Vergrößern_2 and self.scale <= Settings.max_size:
            self.scale += random.randint(2,3)
            Settings.Vergrößern_1 = 0
        if self.rect.bottom > Settings.window_height:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.right > Settings.window_width:
            self.kill()
        if self.rect.left < 0:
            self.kill()
            


        


class Mouse(pygame.sprite.Sprite):    #Die Maus  
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, "Tankgewehr.png")).convert_alpha()
        self.scaleH = Settings.Tankgewehr_scaleH
        self.scaleV = Settings.Tankgewehr_scaleV
        self.image = pygame.transform.scale(self.image_original, (self.scaleV, self.scaleH))
        self.rect = pygame.Rect(0, 0, -10, 170)
    def draw(self, screen):
        self.screen.blit(self.image, self.rect)
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Game(object):
    def __init__(self):
        super().__init__()


        # PyGame-Setup
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.tanks = pygame.sprite.Group()
        self.Tank = Tank()
        self.mous = Mouse()
        self.mouse = pygame.sprite.Group()



    def run(self):
        self.start()
        self.gametext = Settings.game_font.render(f'', False, Settings.color_black)
        # Hauptschleife
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.update()
            self.watch_for_events()
            self.draw()

        # schließt das Spiel
        pygame.quit()

    def draw(self): # erstellt alles aif dem Bildschirm
        self.background.draw(self.screen)
        self.tanks.draw(self.screen)
        self.mouse.draw(self.screen)
        self.screen.blit(self.scoretext,(0, 0))
        self.screen.blit(self.gametext,( Settings.window_width//2-240 ,Settings.window_height//2))
        pygame.display.flip()

    def update(self): # Kontrolliert die Sachen hier jeden Frame
        self.tanks.update()
        self.mouse.update()
        self.Kollision()
        Settings.timer_spawn += 0.02
        if Settings.timer_spawn >= Settings.delay_spawn and len(self.tanks.sprites()) <= Settings.max_nof_tanks:
            pygame.mixer.music.load('lol.mp3')
            pygame.mixer.music.set_volume(.2)
            pygame.mixer.music.play(0,0.2)
            self.tanks.add(Tank())
            Settings.timer_spawn = 0
            

        self.scoretext = Settings.font.render(f'Score = {Settings.game_score}', False, Settings.color_black)    #Text
        
    def pause(self):
        paused = True 
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False



    def Kollision(self):
      tanks = self.tanks.sprites()
      for i, tank1 in enumerate(tanks):
          for tank2 in tanks[i+1:]:
            if pygame.sprite.collide_rect(tank1, tank2):
                self.gameover()
    

    def Maus_Kollision(self):
        if pygame.sprite.groupcollide(self.mouse, self.tanks, False, True):
            Settings.game_score += 10
            sound_effect = pygame.mixer.Sound("Tankgewehr.mp3")
            sound_effect.play()
            
    
        
    def gameover(self): # Spielende
        print('Verloren')
        self.gametext = Settings.game_font.render(f'GAME OVER', False, Settings.color_black)
        self.running = False
        

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN: 
                # Button events
                match event.key:

                    case pygame.K_ESCAPE:
                        self.running = False

                    case pygame.K_p:
                        self.pause()

                    case _:
                        print("Keine Bekannte Taste!")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.Maus_Kollision()


    def start(self): # Wird bei dem Start des spiels einal ausgeführt
        pygame.mouse.set_visible(False)
        self.background = Background()
        self.tanks.add(Tank())
        self.mouse.add(Mouse())
        sound_effect_1 = pygame.mixer.Sound("Sneaky Snitch.mp3")
        sound_effect_1.play()






if __name__ == "__main__":

    game = Game()
    game.run()
