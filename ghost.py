import pygame
import math
from settings import *

INF = 9999999
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

		self.imgArr = []
		self.getSprite()
		self.img = self.imgArr[0]
		self.rect=pygame.Rect(self.posGrid[0],self.posGrid[1],self.app.cellWidth-1,self.app.cellHeight-1)

	def update(self):
		self.posPx += self.direction
		self.canChangeDirection()
		self.move()

		#grid position
		self.posGrid[0] = (self.posPx[0]-BORDER_BUFFER +self.app.cellWidth//2)//self.app.cellWidth+1
		self.posGrid[1] = (self.posPx[1]-BORDER_BUFFER +self.app.cellHeight//2)//self.app.cellHeight+1
		self.rect.x = self.posPx.x
		self.rect.y = self.posPx.y

		if self.direction == (0,1):	#down
			self.img = self.imgArr[3]
		elif self.direction == (0,-1):	#up
			self.img = self.imgArr[2]
		elif self.direction == (-1,0):	#left
			self.img = self.imgArr[1]
		elif self.direction == (1,0):	#right
			self.img = self.imgArr[0]

	def draw(self):
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

		#down
		if self.checkCollide(self.posPx.x,self.posPx.y + self.app.cellHeight):
			d = INF
		#up
		elif self.checkCollide(self.posPx.x,self.posPx.y - self.app.cellHeight):
			u = INF
		#left
		elif self.checkCollide(self.posPx.x+self.app.cellWidth,self.posPx.y):
			r = INF
		#right
		elif self.checkCollide(self.posPx.x-self.app.cellWidth,self.posPx.y):
			l = INF
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

		if self.color == "yellow":
			self.imgArr.append(self.spriteSheet.grabImage(0, 7, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 7, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 7, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 7, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))
		elif self.color == "pink":
			self.imgArr.append(self.spriteSheet.grabImage(0, 5, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 5, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 5, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 5, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))
		elif self.color == "blue":
			self.imgArr.append(self.spriteSheet.grabImage(0, 6, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 6, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 6, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 6, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))	#blue
		else:
			self.imgArr.append(self.spriteSheet.grabImage(0, 4, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 4, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 4, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 4, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))	#red

	def canChangeDirection(self, dir = 0):
		if self.nextDirection == vec(0,1) and not self.checkCollide(self.posPx.x,self.posPx.y + self.app.cellHeight):
			self.direction = self.nextDirection

		elif self.nextDirection == vec(0,-1) and not self.checkCollide(self.posPx.x,self.posPx.y - self.app.cellHeight):
			self.direction = self.nextDirection

		elif self.nextDirection == vec(1,0) and not self.checkCollide(self.posPx.x+self.app.cellWidth,self.posPx.y):
			self.direction = self.nextDirection

		elif self.nextDirection == vec(-1,0) and not self.checkCollide(self.posPx.x-self.app.cellWidth,self.posPx.y):
			self.direction = self.nextDirection

	def wallCollide(self):
		for w in self.app.walls:
			if self.rect.colliderect(w.rect):
				if self.direction == vec(0,1):
					self.direction = vec(0,0)
					self.posPx.y = w.rect.top - self.app.cellHeight
					
				elif self.direction == vec(0,-1):
					self.direction = vec(0,0)
					self.posPx.y = w.rect.bottom
					
				elif self.direction == vec(1,0):
					self.direction = vec(0,0)
					self.posPx.x = w.rect.left - self.app.cellWidth
					
				elif self.direction == vec(-1,0):
					self.direction = vec(0,0)
					self.posPx.x = w.rect.right
					

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

	def checkCollide(self,x,y):
		rec = pygame.Rect(x,y,self.app.cellWidth-1,self.app.cellHeight-1)
		for w in self.app.walls:
			if rec.colliderect(w.rect):
				return True
		return False
					
