import pygame, os

class Imgs():
    def __init__(self):
        self.load()
        
    
    def load(self):
        #print(os.getcwd())
        try:
            self.icon = pygame.image.load("src/img/icon.png").convert_alpha()

        except:
           print("Error loading imgs")