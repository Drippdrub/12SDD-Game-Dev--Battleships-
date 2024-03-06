import pygame
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.mixer.init()
blip = pygame.mixer.Sound(resource_path("sounds\SFX\Blip2.wav"))
blip.set_volume(0.75)

def changeBlip(volume):
	blip.set_volume(volume)

#button class
class Image():
	def __init__(self, x, y, image, scale, *args):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = ((x-width*scale/2), (y-height*scale/2))
	
	def draw(self, surface, *args):
		alpha = 255
		try:
			alpha = args[0]
		except:
			pass
		self.image.set_alpha(alpha)
		surface.blit(self.image, (self.rect.x, self.rect.y))

class Button():
	def __init__(self, x, y, image, scale, *args):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.toggle_click = False
		try:
			click = args[0]
		except:
			click = None
		if click:
			self.toggle_click = True
			self.click = pygame.transform.scale(args[0], (int(width * scale), int(height * scale)))
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
		if self.hovering:
			if self.clicked == False:
				surface.blit(pygame.transform.scale_by(self.image, (1.1, 1.1)), (self.rect.x-self.image.get_width()*0.05, self.rect.y-self.image.get_height()*0.05))
			elif self.toggle_click == True:
				surface.blit(pygame.transform.scale_by(self.click, (1.1, 1.1)), (self.rect.x-self.image.get_width()*0.05, self.rect.y-self.image.get_height()*0.05))
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
				pygame.mixer.Sound.play(blip)
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