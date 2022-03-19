
from socket import socket
import pygame, time, sys, random, socket, threading

from imgs import Imgs
from funks import Funks
from player import Player, OtherPlayer
from map import Map


class Client:
	
	def __init__(self, hosting, host, port, player_num = 2):
		if hosting:
			self.host_game(host, port, player_num)
		else:
			self.connect_to_game(host, port)
		
	
	def reload(self, player_id, numb_of_players, starting_player, client):
		pygame.init()
		pygame.display.set_caption("Multi4Row")
		self.client = client
		self.player_id = player_id
		self.number_of_players = numb_of_players
		
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.prev_time = time.time()
		self.dt = 0
		
		self.screen_size = (600, 600)
		self.screen = pygame.display.set_mode(self.screen_size)
		self.buffer_screen = pygame.Surface(self.screen_size)
		
		self.IMG = Imgs()
		self.FUNKS = Funks(self.screen_size)
  
		self.update_player_thread = threading.Thread(target = self.threaded_nothing, args=())

		
		self.MAP = Map()
		if numb_of_players == 2:
			self.game_map = self.MAP.game_map_2
			self.map_dimensions = self.MAP.map_dimensions_2
		elif numb_of_players == 3:
			self.game_map = self.MAP.game_map_3
			self.map_dimensions = self.MAP.map_dimensions_3
		else:
			self.game_map = self.MAP.game_map_4
			self.map_dimensions = self.MAP.map_dimensions_4
   
		self.FUNKS.createtext("fps_display", [int(self.screen_size[0]*(850/1920)), -self.screen_size[1]//2.05], int(self.screen_size[1]*(20/1080)), "FPS: "+str(round(self.clock.get_fps(), 2)), (255, 124, 0))
		
		
		pygame.display.set_icon(self.IMG.icon)
		
		self.colors = {"black": (0, 0, 0), "black2": (24, 27, 15), "yellow": (255,236,0), "blue": (0,85,255), "white": (255, 255, 255), "background": (59, 59, 59), "darker_background": (39, 39, 39), "red": (255, 0, 0), "light_blue": (0, 232, 255), "purple":(104, 0, 255), "pink":(247, 0, 255)}
		self.colors_to_id = {1: "light_blue", 2: "blue", 3: "pink", 4: "purple"}		
  
		self.screen.fill(self.colors["background"])
		self.buffer_screen.fill(self.colors["background"])
		
		self.running = True
		self.win = False
		
		self.offset_grid = 80
		self.gridsize = self.screen_size[0] - (2 * self.offset_grid)

		self.grid_border_thickness = 4
		self.cellsize = int(self.gridsize / self.map_dimensions[0])
		self.grid_surf = self.FUNKS.schachmuster(self.gridsize, self.cellsize, self.colors["background"], self.colors["darker_background"])
		self.grid_border_surf = pygame.Surface((self.gridsize + ( 2 * self.grid_border_thickness), self.gridsize + ( 2 * self.grid_border_thickness)))
		self.grid_border_surf.fill(self.colors["white"])
		
		
		
		
		self.start_pos = (self.offset_grid, self.offset_grid - self.cellsize - 10)        
		self.p0 = Player(self.player_id, self.start_pos, 0, self.colors[self.colors_to_id[self.player_id]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.game_map, self.map_dimensions, self.client)
		self.other_players = []
		for i in range(1, numb_of_players+1):
			if i != self.player_id:
				self.other_players.append(OtherPlayer(i, (self.offset_grid, self.offset_grid - self.cellsize - 10) , 0, self.colors[self.colors_to_id[i]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.game_map, self.map_dimensions, self.client))
		
		
		
		
		self.starting_player = starting_player
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
				self.win_particles(self.colors[self.colors_to_id[winner]])
	
				self.FUNKS.createtext("winner_text", [0, -int(self.screen_size[0]//24 //0.8)], self.screen_size[0]//24, "Player: "+str(winner)+" Won!", (187, 187, 187))
				self.win = True
	
			self.render()
   
		self.exitgame()
	
	def win_particles(self, color):
		for i in range(100):
			self.FUNKS.particles.append([[self.offset_grid + (self.gridsize/2), self.offset_grid + (self.gridsize/2)], [random.randint(-60, 60)/10, random.randint(-60, 60)/10 ], random.randint(30, 100), color])
	
			
	def clock_tick(self):
		self.clock.tick(self.FPS)
		now = time.time()
		self.dt = now - self.prev_time
		self.prev_time = now
		self.FUNKS.createtext("fps_display", [int(self.screen_size[0]*(850/1920)), -self.screen_size[1]//2.05], int(self.screen_size[1]*(20/1080)), "FPS: "+str(round(self.clock.get_fps(), 2)), (255, 124, 0))
	
	def players(self):
		if self.p0.ready_to_reset:
			self.p0 = Player(self.player_id, (self.p0.x, self.start_pos[1]), self.p0.gridpos_x, self.colors[self.colors_to_id[self.player_id]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.game_map, self.map_dimensions, self.client)
			self.FUNKS.shakes.append([[0,0],[random.randint(-5, 5), random.randint(-5, 5)], 0.5, 2, 2])
			self.player_turn += 1
	
		self.p0.move(self.dt, self.FPS)		
  		
		self.check_if_allready_listening()			
  
		ids_to_add = []
		for i, p in sorted(enumerate(self.other_players), reverse = True):			
			if p.ready_to_reset:
				ids_to_add.append([p.id, p.x, p.gridpos_x, p.client])
				self.other_players.pop(i)
				self.FUNKS.shakes.append([[0,0],[random.randint(-5, 5), random.randint(-5, 5)], 0.5, 2, 2])
				self.player_turn += 1
				
		for i in ids_to_add:
			self.other_players.append(OtherPlayer(i[0], (i[1], self.start_pos[1]), i[2], self.colors[self.colors_to_id[i[0]]], self.gridsize, self.cellsize, self.offset_grid, self.screen_size, self.FUNKS, self.game_map, self.map_dimensions, i[3]))
			
		if self.player_turn > len(self.other_players)+1:
			self.player_turn = 1

		self.turn_system()
  
	def check_if_allready_listening(self):
		if not self.update_player_thread.is_alive():
			self.update_player_thread = threading.Thread(target = self.threaded_update_data, args = ())
			self.update_player_thread.start()

	
	def threaded_update_data(self):
		data = self.recieve_data(self.client)
		if data:
			for i, p in sorted(enumerate(self.other_players), reverse = True):
				if len(data) == 3 and p.id == data[0]:
					if not p.lock_movement:
						p.x = data[1] * self.cellsize + self.offset_grid
						p.gridpos_x = data[1]
					if data[2] == 1:
						p.fall()
			sys.exit()
	
  
	def turn_system(self):
		if self.p0.id != self.player_turn:
			self.p0.lock_fall = True
		else:
			self.p0.lock_fall = False
		
		#important bc of color
		for p in self.other_players:
			if p.id != self.player_turn:
				p.lock_fall = True
			else:
				p.lock_fall = False

	
	def render_players(self):
		for p in self.other_players:
			p.render(self.buffer_screen, self.dt, self.FPS)
   
		self.p0.render(self.buffer_screen, self.dt, self.FPS)
		
	def window_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exitgame()
	
	def threaded_nothing(self):
		sys.exit()
 
	def render(self):
		self.buffer_screen.fill(self.colors["background"])
		self.screen.fill(self.colors["background"])
		self.render_grid()
		if len(self.FUNKS.particles) > 0:
			self.FUNKS.draw_particles(self.buffer_screen, 0.5, self.dt, self.FPS)
		
  		
		
		if self.win:
			self.render_win()
		else:
			self.render_players()

		self.FUNKS.draw_screenshake(self.screen, self.buffer_screen, self.dt, self.FPS)
		self.FUNKS.texthandler("fps_display", self.screen)
		pygame.display.flip()
	
	def render_grid(self):
		self.buffer_screen.blit(self.grid_border_surf, (self.offset_grid - self.grid_border_thickness, self.offset_grid - self.grid_border_thickness))
		self.buffer_screen.blit(self.grid_surf, (self.offset_grid, self.offset_grid))
		
		
		for y, line in enumerate(self.game_map):
			for x, chip in enumerate(line):
				if chip != 0.0:
					pygame.draw.circle(self.buffer_screen, self.colors[self.colors_to_id[chip]], (x * self.cellsize + self.offset_grid + (self.cellsize/2) , y * self.cellsize + self.offset_grid + (self.cellsize /2)), self.cellsize/2)
		
		
	 
	def render_win(self):
		if self.winning_screen_timer_var > 0:
			self.buffer_screen.blit(self.winner_darker, (0, 0))
			self.FUNKS.texthandler("winner_text", self.buffer_screen)

		self.winning_screen_timer_var += 1 *self.dt*self.FPS
		if self.winning_screen_timer_var >= self.winning_screen_timer_val:
			self.win = False
			self.running = False
	
	
	def check_win(self):
		for y, line in sorted(enumerate(self.game_map), reverse = True): #starting bottom left
			for x, chip in enumerate(line):
				if chip != 0:
					try:
						if chip == self.game_map[y-1][x] and self.game_map[y-2][x] == chip and self.game_map[y-3][x] == chip:
							return chip
					except IndexError:
						pass
						
					try:
						if chip == self.game_map[y][x+1] and self.game_map[y][x+2] == chip and self.game_map[y][x+3] == chip:
							return chip
					except IndexError:
						pass
					try:
						if chip == self.game_map[y-1][x+1] and self.game_map[y-2][x+2] == chip and self.game_map[y-3][x+3] == chip:
							return chip
					except IndexError:
						pass
  
					try:
						if chip == self.game_map[y][x-1] and self.game_map[y][x-2] == chip and self.game_map[y][x-3] == chip:
							return chip
					except IndexError:
						pass
					try:
						if chip == self.game_map[y-1][x-1] and self.game_map[y-2][x-2] == chip and self.game_map[y-3][x-3] == chip:
							return chip
					except IndexError:
						pass
		return 0

	
	def exitgame(self):
		self.client.close()
		pygame.quit()
		sys.exit()
		
	### SERVER FUNCTIONS ###
	'''
	
	[ , ] -> [" , "]
	0. -> id
	1. -> pos_gridx
	2. -> dropping (True/False)(1/0)
	
	["0.", "1.", "2."]
	["id", "pos_gridx", "dropping"]
	example: ["1, 0, 0]
 
	from list to str use: make_str(list)
	from str to list use: list = read_str(str)
	
	'''
	def host_game(self, host, port, numb_players):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			server.bind((host, port))
		except socket.error as e:
			pass
			#print(e)

		listeners = numb_players -1
		server.listen(listeners)
		#print("Waiting for connection.. Server started")
		player_id = 2
		starting_player = random.randint(1, numb_players)		
  
		while True:
			client, addr = server.accept()
			#print("Connected to: "+ str(addr))
			self.send_data([player_id, numb_players, starting_player], client)
			
			
			player_id += 1
			if player_id >= numb_players:
				break
		threading.Thread(target=self.reload, args=(1, numb_players, starting_player, client, )).start()
		server.close()
		sys.exit()

	def connect_to_game(self, host, port):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((host, port))
		#must get its own id, numb_of_players, starting_player
		data = self.recieve_data(client)

		threading.Thread(target=self.reload, args=(data[0], data[1], data[2], client, )).start()
		sys.exit()
 
	
	def send_data(self, data, client, encoding = 'utf-8'):
		st = self.make_str(data)
		try:
			client.sendall(st.encode(encoding))
		except:
			pass
			#print("Error sending data")
   
		#print("Sent data.. "+st)
	

	def recieve_data(self, client, buff_size = 1024, decoding = 'utf-8'):
		try:
			data = client.recv(buff_size).decode(decoding)
			if data:
				#print("Received: "+data)
				return self.read_str(data)

		except:
			#print("Error while waiting for data")
			return []
   
	
	def read_str(self, st):
		st = st.split(",")
		ret = []
		for i in st:
			ret.append(int(i))
		return ret
			
	
	def make_str(self, data):
		ret = ""
		for i in range(len(data)):
			ret += str(data[i]) + ","
		ret = ret.removesuffix(",")
		return ret

	
