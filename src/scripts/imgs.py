import pygame, os

class Imgs():
    def __init__(self):
        self.load()
        
    
    def load(self):
        #print(os.getcwd())
        try:
            self.icon = pygame.image.load("src/img/icon.png").convert_alpha()
            
        except:
            self.icon = pygame.image.load("H:/GitRepos/Multi4Row/src/img/icon.png").convert_alpha()
            print("Error loading imgs")