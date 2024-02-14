import pygame

#button class
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
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			self.hovering = True
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		else:
			self.hovering = False

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if self.hovering and self.toggle_hover:
			surface.blit(self.hover, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))

		return action