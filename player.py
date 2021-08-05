import pygame
from settings import *
vec = pygame.math.Vector2

class Player:
	def __init__(self, app, pos):
		self.app = app
		self.posGrid = pos
		self.posPx = vec(self.posGrid.x * self.app.cellWidth + BORDER_BUFFER/2 + self.app.cellWidth/2, self.posGrid.y * self.app.cellHeight + BORDER_BUFFER/2 + self.app.cellHeight/2)
		print(self.posGrid, "\t", self.posPx)

	def update(self):
		pass

	def draw(self):
		pygame.draw.circle(self.app.screen, yellow, (int(self.posPx.x),int(self.posPx.y)), self.app.cellWidth/2-2)