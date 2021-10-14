import pygame
import math
import random
from settings import *

INF = 9999999
vec = pygame.math.Vector2

class food:
	def __init__(self, app, pos):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()

		self.rect=pygame.Rect(self.posGrid[0],self.posGrid[1],self.app.cellWidth,self.app.cellHeight)

	def update(self):
		self.pacmanCollision()

	def draw(self):
		#self.app.screen.blit(self.img, (int(self.posPx.x),int(self.posPx.y)))
		pygame.draw.circle(self.app.screen, yellow, (self.posPx.x+self.app.cellWidth//2,self.posPx.y+self.app.cellHeight//2), 5)

	######################################################

	def get_posPx(self):
		return vec(self.posGrid.x * self.app.cellWidth + BORDER_BUFFER//2, self.posGrid.y * self.app.cellHeight + BORDER_BUFFER//2)

	def pacmanCollision(self):
		if self.rect.colliderect(self.app.player.rect):
			print("pacman ate the food ")