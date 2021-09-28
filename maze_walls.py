import pygame
from settings import *
vec = pygame.math.Vector2

class Wall:
	def __init__(self, app, pos, wType):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()
		self.wType = wType

		self.imgPath = "assets/sprites/maze/" + self.wType +".png"
		self.img = pygame.image.load(self.imgPath).convert()
		self.rect = self.rect=pygame.Rect(self.posPx.x,self.posPx.y,self.app.cellWidth,self.app.cellHeight)

	def draw(self):
		self.app.screen.blit(self.img, (int(self.posPx.x),int(self.posPx.y)))

	def get_posPx(self):
		return vec(self.posGrid.x * self.app.cellWidth + BORDER_BUFFER//2, self.posGrid.y * self.app.cellHeight + BORDER_BUFFER//2)

