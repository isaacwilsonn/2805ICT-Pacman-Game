import pygame
import math
import random
from settings import *

INF = 9999999
vec = pygame.math.Vector2

class Ghost_Template:
	def __init__(self, app, pos, spriteSheet, color = "red"):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()
		self.color = color
		self.direction = vec(1,0)
		self.nextDirection = None
		self.spriteSheet = spriteSheet
		self.smartMoveCount = 0
		self.dumbMoveCount = 0

		self.imgArr = []
		self.getSprite()
		self.img = self.imgArr[0]
		self.rect=pygame.Rect(self.posGrid[0],self.posGrid[1],self.app.cellWidth,self.app.cellHeight)

	def update_essential(self):
		self.posPx += self.direction

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

	def checkCollide(self,x,y):
		rec = pygame.Rect(x,y,self.app.cellWidth,self.app.cellHeight)
		for w in self.app.walls:
			if rec.colliderect(w.rect):
				return True
		return False

	def getAvailDirs(self, curDir):
		dirs = []

		#Current direction is up or down
		if curDir == vec(0,-1) or curDir == vec(0,1):
			#if curDir is up and no collision ahead -> append curdir
			if curDir == vec(0,-1) and not self.checkCollide(self.posPx.x,self.posPx.y - self.app.cellHeight):
				dirs.append(curDir)
			#if curDir is down and no collision ahead -> append curdir
			elif curDir == vec(0,1) and not self.checkCollide(self.posPx.x,self.posPx.y + self.app.cellHeight):
				dirs.append(curDir)
			if not self.checkCollide(self.posPx.x - self.app.cellWidth,self.posPx.y):
				dirs.append(vec(-1,0))
			if not self.checkCollide(self.posPx.x + self.app.cellWidth,self.posPx.y):
				dirs.append(vec(1,0))
		#left
		elif curDir == vec(-1,0) or curDir == vec(1,0):
			#if curDir is left and no collision ahead -> append curdir
			if curDir == vec(-1,0) and not self.checkCollide(self.posPx.x - self.app.cellWidth,self.posPx.y):
				dirs.append(curDir)
			#if curDir is right and no collision ahead -> append curdir
			elif curDir == vec(1,0) and not self.checkCollide(self.posPx.x + self.app.cellWidth, self.posPx.y):
				dirs.append(curDir)

			if not self.checkCollide(self.posPx.x,self.posPx.y - self.app.cellHeight):
				dirs.append(vec(0,-1))
			if not self.checkCollide(self.posPx.x,self.posPx.y + self.app.cellHeight):
				dirs.append(vec(0,1))
		return dirs