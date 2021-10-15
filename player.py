import pygame
import time
import threading

from settings import *
vec = pygame.math.Vector2

INF = 9999999

class Player:
	def __init__(self, app, pos, spriteSheet):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()
		self.direction = vec(0,0)
		self.nextDirection = None
		self.imgArr= []
		self.lives = 3
		self.deadAnimation = False
		self.speed = 1.25
		self.imgIndex = 0
		self.score = 0
		self.poweredUp = False

		#sort sprites into list
		self.spriteSheet = spriteSheet
		#left
		x = pygame.transform.smoothscale((self.spriteSheet.grabImage(0, 1, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		y = pygame.transform.smoothscale((self.spriteSheet.grabImage(1, 1, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		self.imgArr.append((x,x,x,x,x,x,y,y,y,y,y,y))
		#right
		x = pygame.transform.smoothscale((self.spriteSheet.grabImage(0, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		y = pygame.transform.smoothscale((self.spriteSheet.grabImage(1, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		self.imgArr.append((x,x,x,x,x,x,y,y,y,y,y,y))
		#up
		x = pygame.transform.smoothscale((self.spriteSheet.grabImage(0, 3, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		y = pygame.transform.smoothscale((self.spriteSheet.grabImage(1, 3, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		self.imgArr.append((x,x,x,x,x,x,y,y,y,y,y,y))
		#down
		x = pygame.transform.smoothscale((self.spriteSheet.grabImage(0, 2, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		y = pygame.transform.smoothscale((self.spriteSheet.grabImage(1, 2, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		self.imgArr.append((x,x,x,x,x,x,y,y,y,y,y,y))
		#stationary
		self.imgArr.append(pygame.transform.smoothscale((self.spriteSheet.grabImage(2, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1)))

		#def animation sprites
		self.deathAnimation = []
		x1 = pygame.transform.smoothscale((self.spriteSheet.grabImage(2, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x2 = pygame.transform.smoothscale((self.spriteSheet.grabImage(3, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x3 = pygame.transform.smoothscale((self.spriteSheet.grabImage(4, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x4 = pygame.transform.smoothscale((self.spriteSheet.grabImage(5, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x5 = pygame.transform.smoothscale((self.spriteSheet.grabImage(6, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x6 = pygame.transform.smoothscale((self.spriteSheet.grabImage(7, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x7 = pygame.transform.smoothscale((self.spriteSheet.grabImage(8, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x8 = pygame.transform.smoothscale((self.spriteSheet.grabImage(9, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x9 = pygame.transform.smoothscale((self.spriteSheet.grabImage(10, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x10 = pygame.transform.smoothscale((self.spriteSheet.grabImage(11, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x11 = pygame.transform.smoothscale((self.spriteSheet.grabImage(12, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		x12 = pygame.transform.smoothscale((self.spriteSheet.grabImage(13, 0, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		self.imgArr.append((x1,x1,x1,x1,x1,x2,x2,x2,x2,x2,x3,x3,x3,x3,x3,x4,x4,x4,x4,x4,x5,x5,x5,x5,x5,x6,x6,x6,x6,x6,x7,x7,x7,x7,x7,x8,x8,x8,x8,x8,x9,x9,x9,x9,x9,x10,x10,x10,x10,x10,x11,x11,x11,x11,x11,x12,x12,x12,x12,x12))


		


		self.img = self.imgArr[0][0]
		self.rect=pygame.Rect(self.posGrid[0],self.posGrid[1],self.app.cellWidth,self.app.cellHeight)


	def update(self):

		self.posPx += self.direction
		self.canChangeDirection()
		self.teleportPlayer()


		#grid position
		self.posGrid[0] = (self.posPx[0]-BORDER_BUFFER +self.app.cellWidth//2)//self.app.cellWidth+1
		self.posGrid[1] = (self.posPx[1]-BORDER_BUFFER +self.app.cellHeight//2)//self.app.cellHeight+1
		self.rect.x = self.posPx.x
		self.rect.y = self.posPx.y


		#change player img
		if self.direction == (-self.speed,0):	#left
			self.img = self.imgArr[0][self.imgIndex]
		elif self.direction == (self.speed,0):	#Right
			self.img = self.imgArr[1][self.imgIndex]
		elif self.direction == (0,self.speed):	#Up
			self.img = self.imgArr[2][self.imgIndex]
		elif self.direction == (0,-self.speed):	#Down
			self.img = self.imgArr[3][self.imgIndex]
		elif self.deadAnimation:
			self.img = self.imgArr[5][self.imgIndex]
		else:									#stationary
			self.img = self.imgArr[4]
		self.imgIndex +=1

		if self.deadAnimation:
			if self.imgIndex >= 59:
				self.deadAnimation = False
				self.posGrid = vec(14,23)
				self.posPx = self.get_posPx()
				time.sleep(1)
				self.lives -= 1
				
				self.imgIndex = 0

		else:
			if self.imgIndex >= 12:
				self.imgIndex = 0
		
		self.eatFood()

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
		if self.nextDirection == vec(0,self.speed) and not self.checkCollide(self.posPx.x,self.posPx.y + self.app.cellHeight):
			self.direction = self.nextDirection

		elif self.nextDirection == vec(0,-self.speed) and not self.checkCollide(self.posPx.x,self.posPx.y - self.app.cellHeight):
			self.direction = self.nextDirection

		elif self.nextDirection == vec(self.speed,0) and not self.checkCollide(self.posPx.x+self.app.cellWidth,self.posPx.y):
			self.direction = self.nextDirection

		elif self.nextDirection == vec(-self.speed,0) and not self.checkCollide(self.posPx.x-self.app.cellWidth,self.posPx.y):
			self.direction = self.nextDirection

	def wallCollide(self):
		for w in self.app.walls:
			if self.rect.colliderect(w.rect):
				if self.direction == vec(0,self.speed):
					self.direction = vec(0,0)
					self.posPx.y = w.rect.top - self.app.cellHeight
					
				elif self.direction == vec(0,-self.speed):
					self.direction = vec(0,0)
					self.posPx.y = w.rect.bottom
					
				elif self.direction == vec(self.speed,0):
					self.direction = vec(0,0)
					self.posPx.x = w.rect.left - self.app.cellWidth
					
				elif self.direction == vec(-self.speed,0):
					self.direction = vec(0,0)
					self.posPx.x = w.rect.right

	def checkCollide(self,x,y, obj='wall'):
		if obj == 'wall':
			rec = pygame.Rect(x,y,self.app.cellWidth,self.app.cellHeight)
			for w in self.app.walls:
				if rec.colliderect(w.rect):
					return True
			return False

	def die(self):
		#time.sleep(0.5)
		self.nextDirection = vec(0,0)
		self.direction = vec(0,0)
		#for g in self.app.dGhosts:
			#g.direction = vec(0,0)
		#for g in self.app.sGhosts:
			#g.direction = vec(0,0)
		self.app.snd_pacmanDeath.play(0,0)
		self.deadAnimation = True
		
		
	def eatFood(self):
		for food in self.app.food:
			if self.posGrid == food.posGrid:
				if food.foodType == True:
					self.app.food.pop(self.app.food.index(food))
					self.app.score += 100
					self.poweredUp = True
					timer = threading.Timer(10, self.powerPelletTimer)
					timer.start() #after 10 seconds pacman will go back to normal state
				else:
					self.app.food.pop(self.app.food.index(food))
					self.app.score += 10

	def teleportPlayer(self):
		if self.posGrid == [0, 14]: #left side teleporter
			self.posGrid[0] = 26
			self.posGrid[1] = 14
			self.posPx = self.get_posPx()

		elif self.posGrid == [27, 14]: #right side teleporter
			self.posGrid[0] = 1
			self.posGrid[1] = 14
			self.posPx = self.get_posPx()


	def powerPelletTimer(self):
		self.poweredUp = False

