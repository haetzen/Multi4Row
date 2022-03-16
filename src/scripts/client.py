import pygame, time, sys
from imgs import Imgs
from funks import Funks
from player import Player, OtherPlayer
from map import Map
from network import Network



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
		
		self.colors = {"black": (0, 0, 0), "black2": (24, 27, 15), "yellow": (255,236,0), "blue": (22,127,243), "white": (255, 255, 255), "background": (59, 59, 59), "darker_background": (39, 39, 39), "red": (255, 0, 0)}
		self.colors_to_id = {1: "yellow", 2: "blue", 3: "red", 4: "green"}		
  
		self.screen.fill(self.colors["background"])
		
		self.running = True
		
		
		self.offset_grid = 80
		self.gridsize = self.screen_size[0] - (2 * self.offset_grid)
	
		self.cellsize = self.gridsize / self.MAP.map_dimensions[0]
		self.grid_surf = self.FUNKS.schachmuster(self.gridsize, self.cellsize, self.colors["background"], self.colors["darker_background"])
		self.FUNKS.outline(self.grid_surf, (0, 0), self.grid_surf)		
  
		self.N = Network()
		self.client_id = 1
		#self.start_pos = self.read_pos(self.N.get_pos())
		self.start_pos = (self.offset_grid, self.offset_grid - self.cellsize - 10)        
		self.p1 = Player(self.client_id, self.start_pos, 0, self.colors[self.colors_to_id[self.client_id]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.MAP)
		
		self.p2 = OtherPlayer((5,5), self.colors["blue"], self.gridsize, self.cellsize, self.offset_grid, self.gridsize)
		
		self.main_loop()
	
	
	def main_loop(self):
		while self.running:
			self.clock_tick()
			self.window_events()
			self.players()
			self.check_win()
   
			self.render()
			
	def clock_tick(self):
		self.clock.tick(self.FPS)
		now = time.time()
		self.dt = now - self.prev_time
		self.prev_time = now
		self.FUNKS.createtext("fps_display", [int(self.screen_size[0]*(850/1920)), -self.screen_size[1]//2.05], int(self.screen_size[1]*(20/1080)), "FPS: "+str(round(self.clock.get_fps(), 2)), (255, 124, 0))
	
	def players(self):
		if self.p1.ready_to_reset:
			self.p1 = Player(self.client_id, self.start_pos, 0, self.colors["yellow"], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.MAP)

		self.p1.move()
		
	def window_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitgame()
		
	def render(self):
		self.screen.fill(self.colors["background"])
		self.render_grid()
		self.p1.render(self.screen, self.dt, self.FPS)
		
		self.FUNKS.texthandler("fps_display", self.screen)
		pygame.display.flip()
	
	def render_grid(self):
		self.screen.blit(self.grid_surf, (self.offset_grid, self.offset_grid))
		for y, line in enumerate(self.MAP.game_map):
			for x, chip in enumerate(line):
				if chip != 0.0:
					rect = (x * self.cellsize + self.offset_grid, y * self.cellsize + self.offset_grid, self.cellsize, self.cellsize)
					pygame.draw.rect(self.screen, self.colors[self.colors_to_id[chip]], rect)
	 
	
	
	def check_win(self):
		
		for y, line in sorted(enumerate(self.MAP.game_map), reverse = True): #starting bottom left
			for x, chip in enumerate(line):
				if (chip != 0) and ((chip == self.MAP.game_map[y-1][x] and self.MAP.game_map[y-2][x] == chip and self.MAP.game_map[y-3][x] == chip) or (chip == self.MAP.game_map[y][x+1] and self.MAP.game_map[y][x+2] == chip and self.MAP.game_map[y][x+3] == chip) or (chip == self.MAP.game_map[y-1][x+1] and self.MAP.game_map[y-2][x+2] == chip and self.MAP.game_map[y-3][x+3] == chip) or (chip == self.MAP.game_map[y][x-1] and self.MAP.game_map[y][x-2] == chip and self.MAP.game_map[y][x-3] == chip) or (chip == self.MAP.game_map[y-1][x-1] and self.MAP.game_map[y-2][x-2] == chip and self.MAP.game_map[y-3][x-3] == chip)):
					
					return chip
		return 0

	
	def exitgame(self):
		pygame.quit()
		sys.exit()
		
	### SERVER FUNCTIONS ###
	def read_pos(self, st):
		st = st.split(",")
		return (int(st[0]), int(st[1]))  
	   
	def make_pos(self, tup):
		return str(tup[0]) + "," + str(tup[1]) 
		
if __name__ =='__main__':
	Client()