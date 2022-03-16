import pygame, sys, random




class Funks:
	def __init__(self, currentres):
		#ELEMENTE DICTs:
		self.buttons = {}
		self.imgbuttons = {}
		self.anzeigen = {}
		self.texts = {}
		self.sliders = {}
		self.switches = {}
		self.particles = []
		self.shakes = []
  
		self.font_path = "Multi4Row/src/fonts/Hack-Bold.ttf"
  
		self.switch_on_path = "./data/imgs/switch_on.png"
		self.switch_off_path = "./data/imgs/switch_off.png"
  
		self.currentres = currentres


	#################################################################################################################################################################
	#################################################################################################################################################################
	###########################################FUNCTIONS#############################################################################################################
	#################################################################################################################################################################
	#################################################################################################################################################################

	#normal Buttons
	def createbtn(self, name, pos, size, text, colorbtn, colorbtnpressed, colortext, colortextpressed, funktionname, funktionübergame = ""): 
		rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
		font = pygame.font.Font(self.font_path, size[1])

		textobj = font.render(text, 1, colortext)
		textobj1 = font.render(text, 1, colortextpressed)
		textrect = textobj.get_rect(center=(pos[0] + size[0]/2, pos[1] + size[1]/2))
		i = 1
		while textrect.width > size[0]:
			i += 1
			font = pygame.font.Font(self.font_path, size[1]-i)
			textobj = font.render(text, 1, colortext)
			textobj1 = font.render(text, 1, colortextpressed)
			textrect = textobj.get_rect(center=(pos[0] + size[0]/2, pos[1] + size[1]/2))

		self.buttons[name] = [rect, [textobj, textobj1, textrect], False, colorbtn, colorbtnpressed, colortext, colortextpressed, funktionname, 0, funktionübergame] #btn rect, text zeug, hover, colorbtn, color2btn, colortext, color2text, funktion -> machblabla(), sound timer

	
	def buttonhandler(self, name, mx, my, click, screen): 
		if self.buttons[name][0].collidepoint((mx, my)):
			pygame.draw.rect(screen, self.buttons[name][4], self.buttons[name][0])
			screen.blit(self.buttons[name][1][1], self.buttons[name][1][2])
			if not self.buttons[name][2]:
				if self.buttons[name][8] == 30:
					self.buttons[name][8] = 0
				self.buttons[name][2] = True
				self.buttons[name][8] += 1
			if click:
				if self.buttons[name][9] == "":
					self.buttons[name][7]()
				else: 
					self.buttons[name][7](self.buttons[name][9])
		else:
			self.buttons[name][2] = False
			self.buttons[name][8] = 0
			pygame.draw.rect(screen, self.buttons[name][3], self.buttons[name][0])
			screen.blit(self.buttons[name][1][0], self.buttons[name][1][2])
		
	def checkallowrender(self, name, posxmin, posxmax, posymin, posymax, checkX, checkY, mx, my, click, screen):
		if checkX and checkY:
			if self.buttons[name][0].x >= posxmin and self.buttons[name][0].x <= posxmax and self.buttons[name][0].y >= posymin and self.buttons[name][0].y <= posymax:
				self.buttonhandler(name, mx, my, click, screen)
				
		elif checkX and not checkY:
			if self.buttons[name][0].x >= posxmin and self.buttons[name][0].x <= posxmax:
				self.buttonhandler(name, mx, my, click, screen)
				
		else:
			if self.buttons[name][0].y >= posymin and self.buttons[name][0].y <= posymax:
				self.buttonhandler(name, mx, my, click, screen)
				

	def checksliderallowrender(self, name, posxmin, posxmax, posymin, posymax, checkX, checkY, mouse, clickhold, screen):
		if checkX and checkY:
			if self.sliders[name][1][0].x >= posxmin and self.sliders[name][1][0].x <= posxmax and self.sliders[name][1][0].y >= posymin and self.sliders[name][1][0].y <= posymax:
				self.sliderhandler(name, screen, clickhold, mouse)
				
		elif checkX and not checkY:
			if self.sliders[name][1][0].x >= posxmin and self.sliders[name][1][0].x <= posxmax:
				self.sliderhandler(name, screen, clickhold, mouse)
				
		else:
			if self.sliders[name][1][0].y >= posymin and self.sliders[name][1][0].y <= posymax:
				self.sliderhandler(name, screen, clickhold, mouse)
				
		

	def recentertext(self, name):
		self.buttons[name][1][2] = self.buttons[name][1][0].get_rect(center=(self.buttons[name][0].x + self.buttons[name][0].width/2, self.buttons[name][0].y + self.buttons[name][0].height/2))

	def changetext(self, name, text):
		font = pygame.font.Font(self.font_path, self.buttons[name][0].height)

		textobj = font.render(text, 1, self.buttons[name][5])
		textobj1 = font.render(text, 1, self.buttons[name][6])
		textrect = textobj.get_rect(center=(self.buttons[name][0].x + self.buttons[name][0].width/2, self.buttons[name][0].y + self.buttons[name][0].height/2))
		i = 1
		while textrect.width > self.buttons[name][0].width:
			i += 1
			font = pygame.font.Font(self.font_path, self.buttons[name][0].height-i)
			textobj = font.render(text, 1, self.buttons[name][5])
			textobj1 = font.render(text, 1, self.buttons[name][6])
			textrect = textobj.get_rect(center=(self.buttons[name][0].x + self.buttons[name][0].width/2, self.buttons[name][0].y + self.buttons[name][0].height/2))

		self.buttons[name][1][0] = textobj
		self.buttons[name][1][1] = textobj1
		self.buttons[name][1][2] = textrect 

	#Img buttons
	def createimgbtn(self, name, pos, img, imgpressed, scale, funktionname): 
		self.imgbuttons[name] = [pos, [img, imgpressed], scale, 0, False, funktionname] #pos, image, scale, sound timer, hover, funktion
	
	def flipimgbuttonimg(self, name):
		img = self.imgbuttons[name][1][0]
		img2 = self.imgbuttons[name][1][1]

		self.imgbuttons[name][1][0] = img2
		self.imgbuttons[name][1][1] = img

	def changeimgbuttonimg(self, name, img1, img2):
		self.imgbuttons[name][1][0] = img1
		self.imgbuttons[name][1][1] = img2
	
	def imgbuttonhandler(self, name, mx, my, click, screen, colorkey = (255, 255, 255)): 
		img = self.imgbuttons[name][1][0]
		img2 = self.imgbuttons[name][1][1]
		img.set_colorkey(colorkey)
		img2.set_colorkey(colorkey)
		if self.imgbuttons[name][2] != [0, 0]:
			img = pygame.transform.scale(img, self.imgbuttons[name][2])
			img2 = pygame.transform.scale(img2, self.imgbuttons[name][2])
		img = img.convert_alpha()
		img2 = img2.convert_alpha()
		rect = img.get_rect()
		rect.x = self.imgbuttons[name][0][0]
		rect.y = self.imgbuttons[name][0][1]
		if rect.collidepoint((mx, my)):
			screen.blit(img2, self.imgbuttons[name][0])
			if not self.imgbuttons[name][4]:
				if self.imgbuttons[name][3] == 30:
					self.imgbuttons[name][3] = 0
				self.imgbuttons[name][4] = True
				self.imgbuttons[name][3] += 1
			if click:
				self.imgbuttons[name][5]()
		else:
			self.imgbuttons[name][4] = False
			self.imgbuttons[name][3] = 0
			screen.blit(img, self.imgbuttons[name][0])

	
	def createanzeige(self, name, pos, img, scale, wert, textcolor, colorkey = (255, 255, 255)):
		if scale != [0, 0]:
			img = pygame.transform.scale(img, scale)
		img.set_colorkey(colorkey)
		img = img.convert_alpha()
		font = pygame.font.Font(self.font_path, int(img.get_rect().height //1.2))
		textobj = font.render(str(wert), 1, textcolor)
		textrect = textobj.get_rect(center = (pos[0], pos[1] + img.get_rect().height //2))
		textrect.right = pos[0]
		wert_before = wert
		self.anzeigen[name] = [pos, img, [wert, textobj, textrect, textcolor], wert_before]

	def anzeigenhandler(self, name, screen, wert):
		self.anzeigen[name][2][0] = wert
		if self.anzeigen[name][3] != self.anzeigen[name][2][0]:
			self.anzeigen[name][3] = self.anzeigen[name][2][0]
			self.changeanzeige(name, self.anzeigen[name][2][0])

		screen.blit(self.anzeigen[name][2][1], self.anzeigen[name][2][2])
		screen.blit(self.anzeigen[name][1], [self.anzeigen[name][0][0], self.anzeigen[name][0][1]])

	def changeanzeige(self, name, changewert):
		font = pygame.font.Font(self.font_path, int(self.anzeigen[name][1].get_rect().height //1.2))
		self.anzeigen[name][2][1] = font.render(str(self.anzeigen[name][2][0]), 1, self.anzeigen[name][2][3])
		
		self.anzeigen[name][2][2] = self.anzeigen[name][2][1].get_rect(center = (self.anzeigen[name][0][0], self.anzeigen[name][0][1] + self.anzeigen[name][1].get_rect().height //2))
		self.anzeigen[name][2][2].right = self.anzeigen[name][0][0]

	#TEXT FUNCTION (TEXT ALLWAYS CENTER ON SCREEN, MOVE WITH OFFSET)
	def createtext(self, name, offset, size, text, textcolor):
		font = pygame.font.Font(self.font_path, size)
		textobj = font.render(text, 1, textcolor)
		textrect = textobj.get_rect(center = (self.currentres[0]//2 + offset[0], self.currentres[1]//2 + offset[1]))
		self.texts[name] = [textobj, textrect]

	def texthandler(self, name, screen):
		screen.blit(self.texts[name][0], self.texts[name][1])

	def createslider(self, name, pos, barsize, radius, colorbar, colorslider, colorsliderpress):
		bar_rect = pygame.Rect(pos[0], pos[1], barsize[0], barsize[1])
		slider_circlerect = pygame.Rect(pos[0], pos[1] - radius//4, radius, radius)
		self.sliders[name] = [pos, [bar_rect, slider_circlerect], colorbar, colorslider, colorsliderpress, 0, False]

	def sliderhandler(self, name, screen, clickhold, mouse):
		pygame.draw.rect(screen, self.sliders[name][2], self.sliders[name][1][0])
		
		if clickhold[0]:
			if self.sliders[name][1][0].collidepoint(mouse):
				self.sliders[name][1][1].x = mouse[0] - self.sliders[name][1][1].width//2 + 2
				self.sliders[name][6] = True
			elif self.sliders[name][1][1].collidepoint(mouse):
				self.sliders[name][6] = True
			else:
				self.sliders[name][6] = False
		else:
			self.sliders[name][6] = False

		if self.sliders[name][6]:
			self.sliders[name][1][1].x = mouse[0] - self.sliders[name][1][1].width//2 + 2
			if self.sliders[name][1][1].x < self.sliders[name][1][0].x - self.sliders[name][1][1].width//2:
				self.sliders[name][1][1].x = self.sliders[name][1][0].x - self.sliders[name][1][1].width//2
			elif self.sliders[name][1][1].x > self.sliders[name][1][0].x + self.sliders[name][1][0].width - self.sliders[name][1][1].width//2:
				self.sliders[name][1][1].x = self.sliders[name][1][0].x + self.sliders[name][1][0].width - self.sliders[name][1][1].width//2

			pygame.draw.circle(screen, self.sliders[name][4], [self.sliders[name][1][1].x + self.sliders[name][1][1].width//2, self.sliders[name][1][0].y + self.sliders[name][1][1].height//4], self.sliders[name][1][1].width//2)
		else:
			if self.sliders[name][1][1].x < self.sliders[name][1][0].x - self.sliders[name][1][1].width//2:
				self.sliders[name][1][1].x = self.sliders[name][1][0].x - self.sliders[name][1][1].width//2
			elif self.sliders[name][1][1].x > self.sliders[name][1][0].x + self.sliders[name][1][0].width - self.sliders[name][1][1].width//2:
				self.sliders[name][1][1].x = self.sliders[name][1][0].x + self.sliders[name][1][0].width - self.sliders[name][1][1].width//2
			pygame.draw.circle(screen, self.sliders[name][3], [self.sliders[name][1][1].x + self.sliders[name][1][1].width//2, self.sliders[name][1][0].y + self.sliders[name][1][1].height//4], self.sliders[name][1][1].width//2)
			
	def setsliderwert(self, name, wert):
		self.sliders[name][5] = wert
		self.sliders[name][1][1].x = (wert*self.sliders[name][1][0].width - wert*self.sliders[name][1][1].width)*100 - self.sliders[name][1][1].width//4 + self.sliders[name][1][0].x

	def getsliderwert(self, name):
		return self.sliders[name][5]


	def createswitch(self, name, pos, text, textcolor, size, img1, img2, func, state):
		on_img = pygame.image.load(img1).convert()
		on_img = pygame.transform.scale(on_img, (size, size))
		on_img.set_colorkey((255, 255, 255))
		off_img = pygame.image.load(img2).convert()
		off_img = pygame.transform.scale(off_img, (size, size))
		off_img.set_colorkey((255, 255, 255))
		font = pygame.font.Font(self.font_path, int(on_img.get_rect().height //2))
		textobj = font.render(text, 1, textcolor)
		textrect = textobj.get_rect(center = (pos[0] - size//2, pos[1] + on_img.get_rect().height //2))
		switchpos = (pos[0] + textrect.width//2 - size//2, pos[1])
		swtichrect = pygame.Rect(pos[0] + textrect.width//2 - size//2, switchpos[1], size, size)
		self.switches[name] = [pos, textobj, textrect, on_img, off_img, switchpos, swtichrect, func, state]


	def switchcheckallowrender(self, name, posxmin, posxmax, posymin, posymax, checkX, checkY, mouse_pos, click, screen):
		if checkX and checkY:
			if self.switches[name][0][0] >= posxmin and self.switches[name][0][0] <= posxmax and self.switches[name][0][1] >= posymin and self.switches[name][0][1]<= posymax:
				self.switchhandler(name, mouse_pos, click, screen)
				
		elif checkX and not checkY:
			if self.switches[name][0][0] >= posxmin and self.switches[name][0][0] <= posxmax:
				self.switchhandler(name, mouse_pos, click, screen)
				
		else:
			if self.switches[name][0][1] >= posymin and self.switches[name][0][1] <= posymax:
				self.switchhandler(name, mouse_pos, click, screen)

	def switchhandler(self, name, mouse_pos, click, screen):
		if self.switches[name][6].collidepoint(mouse_pos) and click:
			if self.switches[name][7] == None:
				self.flipswitchstate(name)
			else:
				self.switches[name][7]()
				self.flipswitchstate(name)
					

		if self.switches[name][-1]:
			screen.blit(self.switches[name][3], self.switches[name][5])
			screen.blit(self.switches[name][1], self.switches[name][2])
		else:
			screen.blit(self.switches[name][4], self.switches[name][5])
			screen.blit(self.switches[name][1], self.switches[name][2])

	def flipswitchstate(self, name):
		self.switches[name][-1] = not self.switches[name][-1]
  
	def outline(self, img, loc, surf, thickness = 1, u = True, d = True, l = True, r = True):
		mask = pygame.mask.from_surface(img)
		mask_outline = mask.outline()
		mask_surf = pygame.Surface(img.get_size())
		for pixel in mask_outline:
			mask_surf.set_at(pixel, (255, 255, 255))
		mask_surf.set_colorkey((0, 0, 0))
		if l:
			surf.blit(mask_surf, (loc[0]-thickness, loc[1]))
		if r:
			surf.blit(mask_surf, (loc[0]+thickness, loc[1]))
		if u:
			surf.blit(mask_surf, (loc[0], loc[1]-thickness))
		if d:
			surf.blit(mask_surf, (loc[0], loc[1]+thickness))
		
	def fill_img_with_color(self, img, color):
		#goes through every pixel in image, and fills in the new color with the same alpha value
		w, h = img.get_size()
		r, g, b, _ = color
		for x in range(w):
			for y in range(h):
				a = img.get_at((x, y))[3]
				img.set_at((x, y), pygame.Color(r, g, b, a))
			
		return img
	 
