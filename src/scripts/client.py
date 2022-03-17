import pygame, time, sys, random

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
		self.buffer_screen = pygame.Surface(self.screen_size)
		
		self.IMG = Imgs()
		self.FUNKS = Funks(self.screen_size)
		
		self.MAP = Map()
		
		self.FUNKS.createtext("fps_display", [int(self.screen_size[0]*(850/1920)), -self.screen_size[1]//2.05], int(self.screen_size[1]*(20/1080)), "FPS: "+str(round(self.clock.get_fps(), 2)), (255, 124, 0))
		
		
		pygame.display.set_icon(self.IMG.icon)
		
		self.colors = {"black": (0, 0, 0), "black2": (24, 27, 15), "yellow": (255,236,0), "blue": (22,127,243), "white": (255, 255, 255), "background": (59, 59, 59), "darker_background": (39, 39, 39), "red": (255, 0, 0)}
		self.colors_to_id = {1: "yellow", 2: "blue", 3: "red", 4: "green"}		
  
		self.screen.fill(self.colors["background"])
		self.buffer_screen.fill(self.colors["background"])
		
		self.running = True
		self.win = False
		
		self.offset_grid = 80
		self.gridsize = self.screen_size[0] - (2 * self.offset_grid)

		self.grid_border_thickness = 4
		self.cellsize = int(self.gridsize / self.MAP.map_dimensions[0])
		self.grid_surf = self.FUNKS.schachmuster(self.gridsize, self.cellsize, self.colors["background"], self.colors["darker_background"])
		self.grid_border_surf = pygame.Surface((self.gridsize + ( 2 * self.grid_border_thickness), self.gridsize + ( 2 * self.grid_border_thickness)))
		self.grid_border_surf.fill(self.colors["white"])
		
		
		#self.N = Network()
		self.client_id = 1
		

		

		#self.start_pos = self.read_pos(self.N.get_pos())
		self.start_pos = (self.offset_grid, self.offset_grid - self.cellsize - 10)        
		self.p1 = Player(self.client_id, self.start_pos, 0, self.colors[self.colors_to_id[self.client_id]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.MAP)
		
		self.other_players = []
		self.other_players.append(OtherPlayer(2, self.start_pos, 0, self.colors[self.colors_to_id[2]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.MAP))
		self.starting_player = random.randint(1, len(self.other_players))
		self.player_turn = self.starting_player
		
		
		self.winner_darker = pygame.Surface((self.screen_size[0], self.screen_size[1]), pygame.SRCALPHA)
		self.winner_darker.fill((0, 0, 0, 200))
		self.winning_screen_timer_val = 100
		self.winning_screen_timer_var = 0
		
		self.main_loop()
	
	
	def main_loop(self):
		while self.running:
			self.clock_tick()
			self.window_events()
   
			if not self.win:
				self.players()

			winner = self.check_win()
			if winner != 0.0:
				self.FUNKS.createtext("winner_text", [0, -int(self.screen_size[0]//24 //0.8)], self.screen_size[0]//24, "Player: "+str(winner)+" Won!", (187, 187, 187))
				self.win = True
   
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
			self.player_turn += 1
			self.FUNKS.shakes.append([[0,0],[random.randint(-5, 5), random.randint(-5, 5)], 0.5, 2, 2])
			if self.player_turn > len(self.other_players)+1:
				self.player_turn = 1
    
		self.p1.move(self.dt, self.FPS)		

		ids_to_add = []
		for i, p in sorted(enumerate(self.other_players), reverse = True):
			p.move(self.dt, self.FPS)
			if p.ready_to_reset:
				ids_to_add.append(p.id)
				self.other_players.pop(i)
				self.FUNKS.shakes.append([[0,0],[random.randint(-5, 5), random.randint(-5, 5)], 0.5, 2, 2])
				self.player_turn += 1
				if self.player_turn > len(self.other_players)+1:
					self.player_turn = 1
		for i in ids_to_add:
			self.other_players.append(OtherPlayer(i, self.start_pos, 0, self.colors[self.colors_to_id[i]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.MAP))

		

		self.turn_system()
		
  
	def turn_system(self):
		if self.p1.id != self.player_turn:
			self.p1.lock_fall = True
		else:
			self.p1.lock_fall = False
		
		for p in self.other_players:
			if p.id != self.player_turn:
				p.lock_fall = True
			else:
				p.lock_fall = False

	
	def render_players(self):
		for p in self.other_players:
			p.render(self.buffer_screen, self.dt, self.FPS)
   
		self.p1.render(self.buffer_screen, self.dt, self.FPS)
		
	def window_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitgame()
		
	def render(self):
		self.buffer_screen.fill(self.colors["background"])
		self.screen.fill(self.colors["background"])
		self.render_grid()
		if len(self.FUNKS.particles) > 0:
			self.FUNKS.draw_particles(self.buffer_screen, 0.5, self.dt, self.FPS)
		self.render_players()
		
		if self.win:
			self.render_win()
		

		self.FUNKS.draw_screenshake(self.screen, self.buffer_screen, self.dt, self.FPS)
		self.FUNKS.texthandler("fps_display", self.screen)
		pygame.display.flip()
	
	def render_grid(self):
		self.buffer_screen.blit(self.grid_border_surf, (self.offset_grid - self.grid_border_thickness, self.offset_grid - self.grid_border_thickness))
		self.buffer_screen.blit(self.grid_surf, (self.offset_grid, self.offset_grid))
		
		
		for y, line in enumerate(self.MAP.game_map):
			for x, chip in enumerate(line):
				if chip != 0.0:
					rect = (x * self.cellsize + self.offset_grid, y * self.cellsize + self.offset_grid, self.cellsize, self.cellsize)
					pygame.draw.rect(self.buffer_screen, self.colors[self.colors_to_id[chip]], rect)
	 
	def render_win(self):
		if self.winning_screen_timer_var > 0:
			self.buffer_screen.blit(self.winner_darker, (0, 0))
			self.FUNKS.texthandler("winner_text", self.buffer_screen)

		self.winning_screen_timer_var += 1 *self.dt*self.FPS
		if self.winning_screen_timer_var >= self.winning_screen_timer_val:
			self.win = False
			self.reload()
	
	def check_win(self):
		
		for y, line in sorted(enumerate(self.MAP.game_map), reverse = True): #starting bottom left
			for x, chip in enumerate(line):
				if chip != 0:
					if y >= 4:
						if chip == self.MAP.game_map[y-1][x] and self.MAP.game_map[y-2][x] == chip and self.MAP.game_map[y-3][x] == chip:
							return chip
					if x <= self.MAP.map_dimensions[0]-1 -4:
						if chip == self.MAP.game_map[y][x+1] and self.MAP.game_map[y][x+2] == chip and self.MAP.game_map[y][x+3] == chip:
							return chip
					if y >= 4 and x <= self.MAP.map_dimensions[0]-1 -4:
						if chip == self.MAP.game_map[y-1][x+1] and self.MAP.game_map[y-2][x+2] == chip and self.MAP.game_map[y-3][x+3] == chip:
							return chip
					if x >= 4:
						if chip == self.MAP.game_map[y][x-1] and self.MAP.game_map[y][x-2] == chip and self.MAP.game_map[y][x-3] == chip:
							return chip
					if x >= 4 and y >= 4:
						if chip == self.MAP.game_map[y-1][x-1] and self.MAP.game_map[y-2][x-2] == chip and self.MAP.game_map[y-3][x-3] == chip:
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