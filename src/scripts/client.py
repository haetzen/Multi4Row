import pygame, time, sys
from imgs import Imgs
from funks import Funks
from player import Player
from map import Map



class Client:
    
    def __init__(self):
        self.reload()
    
    def reload(self):
        pygame.init()
        pygame.display.set_caption("Multi4Row")
        
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.prev_time = time.time()
        self.dt = 0
        
        self.screen_size = (600, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        
        
        self.IMG = Imgs()
        self.FUNKS = Funks(self.screen_size)
        
        self.MAP = Map()
        
        self.FUNKS.createtext("fps_display", [int(self.screen_size[0]*(850/1920)), -self.screen_size[1]//2.05], int(self.screen_size[1]*(20/1080)), "FPS: "+str(round(self.clock.get_fps(), 2)), (255, 124, 0))
		
        
        pygame.display.set_icon(self.IMG.icon)
        
        self.colors = {"black": (0, 0, 0), "black2": (24, 27, 15), "yellow": (255,236,0), "blue": (22,127,243), "white": (255, 255, 255), "background": (59, 59, 59), "red": (255, 0, 0)}
        
        self.screen.fill(self.colors["background"])
        
        self.running = True
        
        
        self.offset_grid = 50
        self.gridsize = self.screen_size[0] - 2 * self.offset_grid
        self.offset_chips = 2
        self.cellsize = self.screen_size[0]/ self.offset_chips * self.MAP.map_dimensions[0]
        
        
        
        
        
        self.main_loop()
    
    
    def main_loop(self):
        while self.running:
            self.clock_tick()
            self.window_events()
            self.render()
            
    def clock_tick(self):
        self.clock.tick(self.FPS)
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now
        self.FUNKS.createtext("fps_display", [int(self.screen_size[0]*(850/1920)), -self.screen_size[1]//2.05], int(self.screen_size[1]*(20/1080)), "FPS: "+str(round(self.clock.get_fps(), 2)), (255, 124, 0))
		
        
    def window_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exitgame()
        
    def render(self):
        self.screen.fill(self.colors["background"])
        
        
        
        self.FUNKS.texthandler("fps_display", self.screen)
        pygame.display.flip()
    
    def render_grid(self):
        for i in range(self.MAP.map_dimensions[0]):
            pygame.draw.line(self.screen, self.colors["black2"], (j*self.cellsize + j*self.offset_chps,self.offset_grid))
        for j in range(self.MAP.map_dimensions[1]):      
            pass
    
    
    
    def check_win(self):
        '''
        check anzahl an verschiedenen chips..
        wenn chips von 1 farbe < 4 skip
        sonst prüfe überall wo chip liegt ob win
        '''
        pass
    
    def exitgame(self):
        pygame.exit()
        sys.exit()
        
        
        
        
if __name__ =='__main__':
    Client()