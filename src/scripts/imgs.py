import pygame, os

class Imgs():
    def __init__(self):
        self.load()
    
    def load(self):
        print(os.getcwd())
        self.icon = pygame.image.load("Multi4Row/src/img/icon.png").convert_alpha()