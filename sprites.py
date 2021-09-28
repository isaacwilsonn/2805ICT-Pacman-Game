import pygame
from settings import *

class Spritesheet(object):
	def __init__(self, shtNum=1):
		self.shtNum = shtNum
		if self.shtNum == 1:
			self.sheet = pygame.image.load("assets/sprites/spritesheet3.png").convert()
			self.sheet.set_colorkey(TRANSPARENT)
		elif self.shtNum == 2:
			self.sheet = pygame.image.load("assets/sprites/spritesheet2.png").convert()
			self.sheet.set_colorkey(TRANSPARENT)

	def grabImage(self, x, y, width, height):
		x *= width
		y *= height
		self.sheet.set_clip(pygame.Rect(x, y, width, height))
		return self.sheet.subsurface(self.sheet.get_clip())
