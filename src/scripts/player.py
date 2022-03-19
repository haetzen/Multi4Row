from asyncio.windows_events import NULL
import pygame, random, threading
from funks import Funks



class Player:
	def __init__(self, id, startpos, startpos_x_grid, color, gridsize, cellsize, offset_grid, screen_size, funks, map, map_dimensions, client):
		self.id = id
		self.gridpos_x = startpos_x_grid
		self.gridpos_y = -1
		self.x = startpos[0]
		self.y = startpos[1]
		self.width = cellsize 
		self.height = cellsize
		self.color = color
		self.game_map = map
		self.map_dimensions = map_dimensions
		self.client = client
		self.rect = (self.x, self.y, self.width, self.height)
		

		self.lock_movement = False
		self.lock_fall = True
		self.dropping = False
		self.target = (-1, -1)
		self.ready_to_reset = False
		self.velocity = 10
		
		self.click_cooldown_var = self.click_cooldown_val = 5
		
		self.gridsize = gridsize
		self.cellsize = cellsize
		self.offset_grid = offset_grid
		self.screen_size = screen_size
		
		self.FUNKS = funks
				
	def render(self, screen, dt, target_fps):
		if self.dropping:
			self.fall_particles()
			if self.y + (self.velocity * dt * target_fps) < self.target[1] * self.cellsize + self.offset_grid:
				self.y += (self.velocity * dt * target_fps)
    
			elif self.y + (self.velocity * dt * target_fps) > self.target[1] * self.cellsize + self.offset_grid:
				self.y = self.target[1] * self.cellsize + self.offset_grid
				self.game_map[self.target[1]][self.target[0]] = self.id
				self.smash_particles()
				self.ready_to_reset = True
				
    
			elif self.target[1] * self.cellsize + self.offset_grid == self.y:
				self.game_map[self.target[1]][self.target[0]] = self.id
				self.smash_particles()
				self.ready_to_reset = True
				
		
		surf = pygame.Surface((self.width, self.height))
		surf.fill((0, 0, 0))
		pygame.draw.circle(surf, self.color, (self.width/2, self.height/2), self.width/2)
		surf.set_colorkey((0, 0, 0))
		self.FUNKS.outline(surf, (self.x, self.y), screen, 4, self.lock_fall and (255, 255, 255) or (0, 255, 0))
		screen.blit(surf, (self.x, self.y))
			
	def fall_particles(self):
		self.FUNKS.particles.append([[self.x + (self.cellsize/2), self.y], [random.randint(-10, 10)/10, random.randint(-10, 1)/10 ], random.randint(2, (int) (self.cellsize/2)), self.color])
	
	def smash_particles(self):
		for i in range(10):
			self.FUNKS.particles.append([[self.x + (self.cellsize/2), self.y + self.cellsize], [random.randint(-20, 20)/10, random.randint(-1, 1)/10 ], random.randint(2, (int) (self.cellsize/3)), self.color])
	

	def win_particles(self):
		for i in range(100):
			self.FUNKS.particles.append([[self.offset_grid + (self.gridsize/2), self.offset_grid + (self.gridsize/2)], [random.randint(-60, 60)/10, random.randint(-60, 60)/10 ], random.randint(30, 100), self.color])
	
	
	def move(self, dt, target_fps):
		e = pygame.key.get_pressed()
		if (e[pygame.K_LEFT] or e[pygame.K_a]) and self.click_cooldown_var >= self.click_cooldown_val and not self.lock_movement:
			self.x -= self.cellsize 
			self.gridpos_x -= 1 
			if self.x < self.offset_grid:
				self.x = self.offset_grid
				self.gridpos_x = 0
			self.click_cooldown_var = 0
			self.send_move()
		
		if (e[pygame.K_RIGHT] or e[pygame.K_d]) and self.click_cooldown_var >= self.click_cooldown_val and not self.lock_movement: 
			self.x += self.cellsize
			self.gridpos_x += 1
			if self.x >= self.screen_size[0] - self.offset_grid - self.cellsize:
				self.x = self.screen_size[0] - self.offset_grid - self.cellsize
				self.gridpos_x = self.map_dimensions[0] -1
			self.click_cooldown_var = 0
			self.send_move()
		
		if (e[pygame.K_DOWN] or e[pygame.K_SPACE]) and self.check_droppable_column() and not self.lock_fall:
			self.fall()
   
		if self.click_cooldown_var < self.click_cooldown_val:
			self.click_cooldown_var += 1*dt*target_fps
   
	def check_droppable_column(self):
		return self.game_map[0][self.gridpos_x] == 0.0
	
	def check_where_landing(self):
		for x, line in sorted(enumerate(self.game_map), reverse = True):
			if line[self.gridpos_x] == 0.0:
				return (self.gridpos_x, x)
			
	def fall(self):
		self.lock_movement = True
		self.lock_fall = True
		self.dropping = True
		self.target = self.check_where_landing()
		self.send_dropping()
	
	def send_move(self):
		self.send_data([self.id, self.gridpos_x, 0], self.client)
	
	def send_dropping(self):
		self.send_data([self.id, self.gridpos_x, 1], self.client)

	def send_data(self, data, client, encoding = 'utf-8'):
		st = self.make_str(data)
		try:
			client.send(st.encode(encoding))
		except:
			print("Error sending data")
   
		print("Sent data.. "+st)
	

	def recieve_data(self, client, buff_size = 1024, decoding = 'utf-8'):
		try:
			data = client.recv(buff_size).decode(decoding)
			if not data:
				#client.close()
				print("Disconnected.. no data received")
			else:
				print("Received: "+data)
				return self.read_str(data)

		except:
			print("Error while waiting for data")
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
	
	  
class OtherPlayer:
	def __init__(self, id, startpos, startpos_x_grid, color, gridsize, cellsize, offset_grid, screen_size, funks, map, map_dimensions, client):
		self.id = id
		self.gridpos_x = startpos_x_grid
		self.gridpos_y = -1
		self.x = startpos[0]
		self.y = startpos[1]
		self.width = cellsize 
		self.height = cellsize
		self.color = color
		self.game_map = map
		self.map_dimensions = map_dimensions
		self.client = client
		self.rect = (self.x, self.y, self.width, self.height)
		
		self.lock_fall = True
		self.dropping = False
		self.target = (-1, -1)
		self.ready_to_reset = False
		self.velocity = 10
		
		self.click_cooldown_var = self.click_cooldown_val = 5
		
		self.gridsize = gridsize
		self.cellsize = cellsize
		self.offset_grid = offset_grid
		self.screen_size = screen_size
		
		self.FUNKS = funks
				
	def render(self, screen, dt, target_fps):
		t1 = threading.Thread(target = self.update_data, args = ())

		if not t1.is_alive():
			t1.start()
		
  
		if self.dropping:
			self.fall_particles()
			if self.y + (self.velocity * dt * target_fps) < self.target[1] * self.cellsize + self.offset_grid:
				self.y += (self.velocity * dt * target_fps)
    
			elif self.y + (self.velocity * dt * target_fps) > self.target[1] * self.cellsize + self.offset_grid:
				self.y = self.target[1] * self.cellsize + self.offset_grid
				self.game_map[self.target[1]][self.target[0]] = self.id
				self.smash_particles()
				self.ready_to_reset = True
				
    
			elif self.target[1] * self.cellsize + self.offset_grid == self.y:
				self.game_map[self.target[1]][self.target[0]] = self.id
				self.smash_particles()
				self.ready_to_reset = True
				
		
		surf = pygame.Surface((self.width, self.height))
		surf.fill((0, 0, 0))
		pygame.draw.circle(surf, self.color, (self.width/2, self.height/2), self.width/2)
		surf.set_colorkey((0, 0, 0))
		self.FUNKS.outline(surf, (self.x, self.y), screen, 4, self.lock_fall and (255, 255, 255) or (0, 255, 0))
		screen.blit(surf, (self.x, self.y))
	
	def update_data(self):
		data = self.recieve_data(self.client)
		if data != []:
			if data[0] == self.id:
				self.gridpos_x = data[1]
				self.x = self.gridpos_x * self.cellsize + self.offset_grid
				if data[2] == 1:
					self.dropping = True

 	
	def fall_particles(self):
		self.FUNKS.particles.append([[self.x + (self.cellsize/2), self.y], [random.randint(-10, 10)/10, random.randint(-10, 1)/10 ], random.randint(2, (int) (self.cellsize/2)), self.color])
	
	def smash_particles(self):
		for i in range(10):
			self.FUNKS.particles.append([[self.x + (self.cellsize/2), self.y + self.cellsize], [random.randint(-20, 20)/10, random.randint(-1, 1)/10 ], random.randint(2, (int) (self.cellsize/3)), self.color])
	
	def win_particles(self):
		for i in range(100):
			self.FUNKS.particles.append([[self.offset_grid + (self.gridsize/2), self.offset_grid + (self.gridsize/2)], [random.randint(-60, 60)/10, random.randint(-60, 60)/10 ], random.randint(30, 100), self.color])
	
	def check_where_landing(self):
		for x, line in sorted(enumerate(self.game_map), reverse = True):
			if line[self.gridpos_x] == 0.0:
				return (self.gridpos_x, x)
			
	def fall(self):
		self.dropping = True
		self.target = self.check_where_landing()
	
	def send_data(self, data, client, encoding = 'utf-8'):
		st = self.make_str(data)
		try:
			client.send(st.encode(encoding))
		except:
			print("Error sending data")
   
		print("Sent data.. "+st)
	

	def recieve_data(self, client, buff_size = 1024, decoding = 'utf-8'):
		try:
			data = client.recv(buff_size).decode(decoding)
			if not data:
				#client.close()
				print("Disconnected.. no data received")
			else:
				print("Received: "+data)
				return self.read_str(data)

		except:
			print("Error while waiting for data")
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