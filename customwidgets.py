import pygame

#button class
class Image():
	def __init__(self, x, y, image, scale, *args):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = ((x-width*scale/2), (y-height*scale/2))
	
	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))

class Button():
	def __init__(self, x, y, image, scale, *args):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.toggle_hover = False
		try:
			hover = args[0]
		except:
			hover = None
		if hover:
			self.toggle_hover = True
			self.hover = pygame.transform.scale(args[0], (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = ((x-width*scale/2), (y-height*scale/2))
		self.clicked = False
		self.hovering = False

	def draw(self, surface):
		past_click = self.clicked
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			self.hovering = True
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
		else:
			self.hovering = False

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		if past_click == True and self.rect.collidepoint(pos) and self.clicked == False:
			action = True

		#draw button on screen
		if self.hovering and self.toggle_hover:
			surface.blit(self.hover, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Toggle():
	def __init__(self, x, y, image_off, image_on, scale):
		width = image_off.get_width()
		height = image_off.get_height()
		self.image_on = pygame.transform.scale(image_off, (int(width * scale), int(height * scale)))
		self.image_off = pygame.transform.scale(image_on, (int(width * scale), int(height * scale)))
		self.rect = self.image_on.get_rect()
		self.rect.topleft = ((x-width*scale/2), (y-height*scale/2))
		self.clicked = False
		self.state = False

	def draw(self, surface, **kwargs):
		self.output_mode = kwargs.get('output', 0)
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				if self.state == False:
					self.state = True
				else:
					self.state = False

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if self.state == True:
			surface.blit(self.image_off, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.image_on, (self.rect.x, self.rect.y))

		if self.output_mode == 0:
			return self.state
		elif self.output_mode == 1:
			return int(self.state)
		else:
			raise ValueError(f"Expected 0 or 1 as output mode, {self.output_mode} was given instead.")