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
		self.imgArr= []
		#self.img = None

		#sort sprites into list
		self.spriteSheet = spriteSheet
		#left
		self.imgArr.append(self.spriteSheet.grabImage(0, 1, 16, 16))
		self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1)) 
		#right
		self.imgArr.append(self.spriteSheet.grabImage(0, 0, 16, 16))
		self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1)) 
		#up
		self.imgArr.append(self.spriteSheet.grabImage(0, 3, 16, 16))
		self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1)) 
		#down
		self.imgArr.append(self.spriteSheet.grabImage(0, 2, 16, 16))
		self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1)) 

		self.img = self.imgArr[0]
		self.rect=pygame.Rect(self.posGrid[0],self.posGrid[1],self.app.cellWidth,self.app.cellHeight)


	def update(self):
		self.posPx += self.direction
		self.canChangeDirection()

		#grid position
		self.posGrid[0] = (self.posPx[0]-BORDER_BUFFER +self.app.cellWidth//2)//self.app.cellWidth+1
		self.posGrid[1] = (self.posPx[1]-BORDER_BUFFER +self.app.cellHeight//2)//self.app.cellHeight+1
		self.rect.x = self.posPx.x
		self.rect.y = self.posPx.y

		#change player img
		if self.direction == (-1,0):	#left
			self.img = self.imgArr[0]
		elif self.direction == (1,0):	#Right
			self.img = self.imgArr[1]
		elif self.direction == (0,1):	#Up
			self.img = self.imgArr[2]
		elif self.direction == (0,-1):	#Down
			self.img = self.imgArr[3]

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

	def canChangeDirection(self):
		#Check if inline with X grid
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

	def checkCollide(self,x,y):
		rec = pygame.Rect(x,y,self.app.cellWidth,self.app.cellHeight)
		for w in self.app.walls:
			if rec.colliderect(w.rect):
				return True
		return False
					
