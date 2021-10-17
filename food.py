import pygame
import math
import random
from settings import *

INF = 9999999
vec = pygame.math.Vector2

class Food:
	def __init__(self, app, pos, foodType):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()
		self.foodType = foodType
		self.rect=pygame.Rect(self.posGrid[0],self.posGrid[1],self.app.cellWidth,self.app.cellHeight)

	def update(self):
		pass

	def draw(self, powerpellet = False):
		#self.app.screen.blit(self.img, (int(self.posPx.x),int(self.posPx.y)))
		if powerpellet:
			pygame.draw.circle(self.app.screen, yellow, (self.posPx.x+self.app.cellWidth//2,self.posPx.y+self.app.cellHeight//2), 5)
		else:
			pygame.draw.circle(self.app.screen, white, (self.posPx.x+self.app.cellWidth//2,self.posPx.y+self.app.cellHeight//2), 3)
	######################################################

	def get_posPx(self):
		return vec(self.posGrid.x * self.app.cellWidth + BORDER_BUFFER//2, self.posGrid.y * self.app.cellHeight + BORDER_BUFFER//2)