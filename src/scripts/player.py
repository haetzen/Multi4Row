import pygame
from funks import Funks


class Player:
	def __init__(self, id, startpos, startpos_x_grid, color, gridsize, cellsize, offset_grid, screen_size, funks, map):
		self.id = id
		self.gridpos_x = startpos_x_grid
		self.gridpos_y = -1
		self.x = startpos[0]
		self.y = startpos[1]
		self.width = cellsize 
		self.height = cellsize
		self.color = color
		self.MAP = map
		self.rect = (self.x, self.y, self.width, self.height)

		self.lock_movement = False
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
			if self.y < self.target[1] * self.cellsize + self.offset_grid:
				self.y += (self.velocity * dt * target_fps)
    
			elif self.y > self.target[1] * self.cellsize + self.offset_grid:
				self.y = self.target[1] * self.cellsize + self.offset_grid
				self.MAP.game_map[self.target[1]][self.target[0]] = self.id
				self.ready_to_reset = True
    
			elif self.target[1] * self.cellsize + self.offset_grid == self.y:
				self.MAP.game_map[self.target[1]][self.target[0]] = self.id
				self.ready_to_reset = True
		
		surf = pygame.Surface((self.width, self.height))
		surf.fill(self.color)
		self.FUNKS.outline(surf, (self.x, self.y), screen, 2)
		screen.blit(surf, (self.x, self.y))
			
	
	def move(self):
		e = pygame.key.get_pressed()
		if e[pygame.K_LEFT] or e[pygame.K_a] and self.click_cooldown_var >= self.click_cooldown_val and not self.lock_movement:
			self.x -= self.cellsize
			self.gridpos_x -= 1
			if self.x < self.offset_grid:
				self.x = self.offset_grid
				self.gridpos_x = 0
			self.click_cooldown_var = 0
		
		if e[pygame.K_RIGHT] or e[pygame.K_d] and self.click_cooldown_var >= self.click_cooldown_val and not self.lock_movement: 
			self.x += self.cellsize
			self.gridpos_x += 1
			if self.x > self.screen_size[0] - self.offset_grid - self.cellsize:
				self.x = self.screen_size[0] - self.offset_grid - self.cellsize
				self.gridpos_x = self.MAP.map_dimensions[0] -1
			self.click_cooldown_var = 0

		
		if e[pygame.K_DOWN] or e[pygame.K_SPACE] and self.check_droppable_column() and not self.lock_movement:
			self.fall()
   
		if self.click_cooldown_var < self.click_cooldown_val:
			self.click_cooldown_var += 1
   
	def check_droppable_column(self):
		return self.MAP.game_map[0][self.gridpos_x] == 0.0
	
	def check_where_landing(self):
		for x, line in sorted(enumerate(self.MAP.game_map), reverse = True):
			if line[self.gridpos_x] == 0.0:
				return (self.gridpos_x, x)
			
	def fall(self):
		self.lock_movement = True
		self.dropping = True
		self.target = self.check_where_landing()
	
				
	  
class OtherPlayer:
	def __init__(self, startpos, color, gridsize, cellsize, offset_grid, screen_size):
		self.x = startpos[0]
		self.y = startpos[1]
		self.width = cellsize
		self.height = cellsize
		self.color = color
		self.rect = (self.x, self.y, self.width, self.height)
		
		self.gridsize = gridsize
		self.cellsize = cellsize
		self.offset_grid = offset_grid
		self.screen_size = screen_size
		
	def render(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)