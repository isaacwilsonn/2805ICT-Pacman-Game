import pygame
import math
from settings import *

vec = pygame.math.Vector2

class Ghost:
	def __init__(self, app, pos, spriteSheet, color = "red"):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()
		self.color = color
		self.direction = vec(1,0)
		self.nextDirection = None

		self.spriteSheet = spriteSheet
		self.img = self.getSprite()
		self.img = pygame.transform.smoothscale(self.img, (self.app.cellWidth-1, self.app.cellHeight-1))
		self.rect=pygame.Rect(0,0,self.app.cellWidth,self.app.cellHeight)
		self.rect.x = self.posGrid[0]
		self.rect.y = self.posGrid[1]

	def update(self):
		self.posPx += self.direction
		self.canChangeDirection()
		self.move()
		self.img = self.getSprite()
		self.img = pygame.transform.smoothscale(self.img, (self.app.cellWidth-1, self.app.cellHeight-1))

		#grid position
		self.posGrid[0] = (self.posPx[0]-BORDER_BUFFER +self.app.cellWidth//2)//self.app.cellWidth+1
		self.posGrid[1] = (self.posPx[1]-BORDER_BUFFER +self.app.cellHeight//2)//self.app.cellHeight+1
		self.rect.x = self.posPx.x
		self.rect.y = self.posPx.y

	def draw(self):
		#pygame.draw.circle(self.app.screen, white, (int(self.posPx.x), int(self.posPx.y)), self.app.cellWidth//2-2)
		self.app.screen.blit(self.img, (int(self.posPx.x),int(self.posPx.y)))

	######################################################

	def get_posPx(self):
		return vec(self.posGrid.x * self.app.cellWidth + BORDER_BUFFER//2, self.posGrid.y * self.app.cellHeight + BORDER_BUFFER//2)

	def move(self):
		#self.nextDirection = vec(0,1)
		u = math.sqrt(abs(pow(self.posGrid.x - self.app.player.posGrid.x,2) + pow(self.posGrid.y -1 - self.app.player.posGrid.y,2)))
		d = math.sqrt(abs(pow(self.posGrid.x - self.app.player.posGrid.x,2) + pow(self.posGrid.y +1 - self.app.player.posGrid.y,2)))
		l = math.sqrt(abs(pow(self.posGrid.x-1 - self.app.player.posGrid.x,2) + pow(self.posGrid.y - self.app.player.posGrid.y,2)))
		r = math.sqrt(abs(pow(self.posGrid.x+1 - self.app.player.posGrid.x,2) + pow(self.posGrid.y - self.app.player.posGrid.y,2)))

		#get index of shortest path
		dirs = (u,d,l,r)
		best = dirs.index(min(dirs))

		if best == 0:
			self.nextDirection = vec(0,-1)
		elif best == 1:
			self.nextDirection = vec(0,1)
		elif best == 2:
			self.nextDirection = vec(-1,0)
		else:
			self.nextDirection = vec(1,0)

	def getSprite(self):
		#used to offset sprite sheet selection -> depending on direction
		x = 0
		if self.direction == vec(1,0):
			x=0
		elif self.direction == vec(-1,0):
			x=2
		elif self.direction == vec(0,-1):
			x=4
		else:
			x=6

		if self.color == "yellow":
			return self.spriteSheet.grabImage(0+x, 7, 16, 16)	#yellow
		elif self.color == "pink":
			return self.spriteSheet.grabImage(0+x, 5, 16, 16)	#pink
		elif self.color == "blue":
			return self.spriteSheet.grabImage(0+x, 6, 16, 16)	#blue
		return self.spriteSheet.grabImage(0+x, 4, 16, 16)		#red

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

	def wallCollide(self, walls):
		for w in walls:
			if self.rect.colliderect(w.rect):
				if self.direction == vec(0,1):
					self.direction = vec(0,-1)
					return
				elif self.direction == vec(0,-1):
					self.direction = vec(0,1)
					return
				elif self.direction == vec(1,0):
					self.direction = vec(-1,0)
					return
				elif self.direction == vec(-1,0):
					self.direction = vec(1,0)
					return

	def ghostCollide(self):
		for g in self.app.ghosts:
			if self == g:
				continue
			if self.rect.colliderect(g.rect):
				if self.direction == vec(0,1):
					self.direction = vec(0,-1)
					return
				elif self.direction == vec(0,-1):
					self.direction = vec(0,1)
					return
				elif self.direction == vec(1,0):
					self.direction = vec(-1,0)
					return
				elif self.direction == vec(-1,0):
					self.direction = vec(1,0)
					return
