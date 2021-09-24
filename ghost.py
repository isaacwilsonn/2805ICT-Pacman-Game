from ghost_template import *

#########################	Smart Ghost 	#########################
class sGhost(Ghost_Template):
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
				print(w.wType)
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

	def move(self):
		#self.nextDirection = vec(0,1)
		u = math.sqrt(abs(pow(self.posGrid.x - self.app.player.posGrid.x,2) + pow(self.posGrid.y -2 - self.app.player.posGrid.y,2)))
		d = math.sqrt(abs(pow(self.posGrid.x - self.app.player.posGrid.x,2) + pow(self.posGrid.y +2 - self.app.player.posGrid.y,2)))
		l = math.sqrt(abs(pow(self.posGrid.x-2 - self.app.player.posGrid.x,2) + pow(self.posGrid.y - self.app.player.posGrid.y,2)))
		r = math.sqrt(abs(pow(self.posGrid.x+2 - self.app.player.posGrid.x,2) + pow(self.posGrid.y - self.app.player.posGrid.y,2)))

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

	def update(self):
		self.update_essential()
		self.canChangeDirection()
		self.move()


#########################	Dumb Ghost 	#########################

class dGhost(Ghost_Template):
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

	def move(self):
		#up
		if self.direction == vec(0,-1):
			dirs = self.getAvailDirs(vec(0,-1))
			if dirs:
				self.direction = random.choice(dirs)
		#down
		elif self.direction == vec(0,1):
			dirs = self.getAvailDirs(vec(0,1))
			if dirs:
				self.direction = random.choice(dirs)
		#left
		elif self.direction == vec(-1,0):
			dirs = self.getAvailDirs(vec(-1,0))
			if dirs:
				self.direction = random.choice(dirs)
		#right
		elif self.direction == vec(1,0):
			dirs = self.getAvailDirs(vec(1,0))
			if dirs:
				self.direction = random.choice(dirs)

	def update(self):
		self.move()
		self.update_essential()