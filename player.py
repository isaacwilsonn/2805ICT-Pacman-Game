import pygame
from settings import *
vec = pygame.math.Vector2

class Player:
	def __init__(self, app, pos, spriteSheet):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()
		self.direction = vec(1,0)
		self.nextDirection = None
		#self.img = None
		self.spriteSheet = spriteSheet
		self.img = self.spriteSheet.grabImage(0, 0, 16, 16)
		self.img = pygame.transform.smoothscale(self.img, (self.app.cellWidth-1, self.app.cellHeight-1)) 

	def update(self):
		self.posPx += self.direction
		self.canChangeDirection()

		#grid position
		self.posGrid[0] = (self.posPx[0]-BORDER_BUFFER +self.app.cellWidth//2)//self.app.cellWidth+1
		self.posGrid[1] = (self.posPx[1]-BORDER_BUFFER +self.app.cellHeight//2)//self.app.cellHeight+1

		#change player img
		if self.direction == (-1,0):	#left
			self.img = self.spriteSheet.grabImage(0, 1, 16, 16)
			self.img = pygame.transform.smoothscale(self.img, (self.app.cellWidth-1, self.app.cellHeight-1))
		elif self.direction == (1,0):	#Right
			self.img = self.spriteSheet.grabImage(0, 0, 16, 16)
			self.img = pygame.transform.smoothscale(self.img, (self.app.cellWidth-1, self.app.cellHeight-1))
		elif self.direction == (0,1):	#Up
			self.img = self.spriteSheet.grabImage(0, 3, 16, 16)
			self.img = pygame.transform.smoothscale(self.img, (self.app.cellWidth-1, self.app.cellHeight-1))
		elif self.direction == (0,-1):	#Down
			self.img = self.spriteSheet.grabImage(0, 2, 16, 16)
			self.img = pygame.transform.smoothscale(self.img, (self.app.cellWidth-1, self.app.cellHeight-1)) 

	def draw(self):
		self.drawPlayer()
	
	def drawPlayer(self):
		if self.img != None:
			self.app.screen.blit(self.img, (int(self.posPx.x),int(self.posPx.y)))
		else:
			pygame.draw.circle(self.app.screen, yellow, (int(self.posPx.x),int(self.posPx.y)), self.app.cellWidth//2-2)

		#draw player rect for debugging
		#pygame.draw.rect(self.app.screen, red, (self.posGrid[0]*self.app.cellWidth+BORDER_BUFFER//2, self.posGrid[1]*self.app.cellHeight+BORDER_BUFFER//2, self.app.cellWidth, self.app.cellHeight),1)
	
	def move(self, direction):
		self.nextDirection = direction

	def get_posPx(self):
		return vec(self.posGrid.x * self.app.cellWidth + BORDER_BUFFER//2, self.posGrid.y * self.app.cellHeight + BORDER_BUFFER//2)

	def canChangeDirection(self, dir = 0):
		#Check if inline with X grid
		if int(self.posPx.x-BORDER_BUFFER//2) % self.app.cellWidth == 0:
			if self.direction == vec(1,0) or self.direction == (-1,0):
				if self.nextDirection != None:
					self.direction = self.nextDirection
		#Check if inline with Y grid
		if int(self.posPx.y-BORDER_BUFFER//2) % self.app.cellHeight == 0:
			if self.direction == vec(0,1) or self.direction == (0,-1):
				if self.nextDirection != None:
					self.direction = self.nextDirection