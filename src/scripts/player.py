import pygame


class Player:
    def __init__(self, gridsize, cellsize, offset_chips, offset_grid, screen_size):
        self.x = 0
        self.y = 0
        self.width = cellsize
        self.height = cellsize
        self.color = "black"
        self.rect = (self.x, self.y, self.width, self.height)
        
        self.gridsize = gridsize
        self.cellsize = cellsize
        self.offset_chips = offset_chips
        self.offset_grid = offset_grid
        self.screen_size = screen_size
        
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    
    def move(self):
        e = pygame.key.get_pressed()
        if e[pygame.K_LEFT]:
            self.x -= self.cellsize + self.offset_chips
            if self.x < self.offset_grid:
                self.x = self.offset_grid
            
        if e[pygame.K_RIGHT]:
            self.x += self.cellsize + self.offset_chips
            if self.x > self.screen_size[0] - self.offset_grid - self.cellsize:
                self.x = self.screen_size[0] - self.offset_grid - self.cellsize
    
    