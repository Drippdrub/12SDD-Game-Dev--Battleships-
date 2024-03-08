import pygame
import sys
import os

# pyinstaller compatability
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# init pygame + button sound
pygame.mixer.init()
blip = pygame.mixer.Sound(resource_path("sounds\SFX\Blip2.wav"))
blip.set_volume(0.75)

# change button volume
def changeBlip(volume):
	blip.set_volume(volume)

#Image Object
class Image():
	# Initialise image object + object vars
	def __init__(self, x, y, image, scale, tiptext=""):
		#get coordinates
		width = image.get_width()
		height = image.get_height()
		#set image
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		#set hitbox
		self.rect = self.image.get_rect()
		self.rect.topleft = ((x-width*scale/2), (y-height*scale/2)) #coordinates corespond to center of image
		self.buttonf = pygame.font.SysFont(resource_path("fonts\CompassPro.ttf"), 18)
		self.tiptextsurface = self.buttonf.render(tiptext, False, (0, 0, 0), (255, 255, 0))
	
	# Draw Image on screen
	def draw(self, surface, *args):
		alpha = 255 #default alpha, full opacity
		try:
			alpha = args[0] #if alpha value is passed, then set alpha to that
		except:
			pass #if no alpha value passed, ignore
		self.image.set_alpha(alpha) #set alpha value
		surface.blit(self.image, (self.rect.x, self.rect.y)) #blit image to screen

	def showTip(self, surface):
		if self.current:
			mouse_pos = pygame.mouse.get_pos()
			surface.blit(self.tiptextsurface, (mouse_pos[0]+16, mouse_pos[1]))

	def focusCheck(self, mousepos, mouseclick):
		self.current = self.rect.collidepoint(mousepos)
		return mouseclick if self.current else True

class Button():
	# Initialise button object + object vars
	def __init__(self, x, y, image, scale, *args):
		#get coordinates
		width = image.get_width()
		height = image.get_height()
		#set image
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		#set click image if a second image has been passed
		self.toggle_click = False
		try:
			click = args[0]
		except:
			click = None
			self.click = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		if click != None:
			self.toggle_click = True
			self.click = pygame.transform.scale(args[0], (int(width * scale), int(height * scale)))
		#set hitbox
		self.rect = self.image.get_rect()
		self.rect.topleft = ((x-width*scale/2), (y-height*scale/2))
		#initialise button states
		self.clicked = False
		self.hovering = False

	# Draw Button on screen and retrieve button states
	def draw(self, surface, alpha=255):
		# save past click state
		past_click = self.clicked
		#initialise return value
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

		self.image.set_alpha(alpha)
		self.click.set_alpha(alpha)

		#draw button on screen
		if self.hovering:
			if self.clicked == False:
				surface.blit(pygame.transform.scale_by(self.image, (1.1, 1.1)), (self.rect.x-self.image.get_width()*0.05, self.rect.y-self.image.get_height()*0.05))
			elif self.toggle_click == True:
				surface.blit(pygame.transform.scale_by(self.click, (1.1, 1.1)), (self.rect.x-self.image.get_width()*0.05, self.rect.y-self.image.get_height()*0.05))
			else:
				surface.blit(pygame.transform.scale_by(self.image, (1.1, 1.1)), (self.rect.x-self.image.get_width()*0.05, self.rect.y-self.image.get_height()*0.05))
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