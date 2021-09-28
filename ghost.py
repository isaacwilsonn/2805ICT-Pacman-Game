from ghost_template import *


#########################	Dumb Ghost 	#########################

class dGhost(Ghost_Template):

	def move(self):
		dirs = self.getAvailDirs(self.direction)
		if dirs:
			self.direction = random.choice(dirs)

	def update(self):
		self.move()
		self.update_essential()




#########################	New Smart Ghost 	#########################

class sGhost(Ghost_Template):
	def move(self):
		dirs = []
		u,d,l,r = INF,INF,INF,INF


		dirs = self.getAvailDirs(self.direction)

		if dirs:
			#dumb move
			if self.smartMoveCount >= 5:
				self.direction = random.choice(dirs)
				self.dumbMoveCount += 1
				if self.dumbMoveCount >= 2:
					self.smartMoveCount = 0
			#smart move
			else:
				self.dumbMoveCount = 0
				for x in dirs:
					#up
					if x == vec(0,-1):
						#u = math.sqrt(abs(pow(self.posGrid.x - self.app.player.posGrid.x,2) + pow(self.posGrid.y -1 - self.app.player.posGrid.y,2)))
						u = abs(self.posGrid.x - self.app.player.posGrid.x) + abs((self.posGrid.y-1) - self.app.player.posGrid.y)
					#down
					elif x == vec(0,1):
						#d = math.sqrt(abs(pow(self.posGrid.x - self.app.player.posGrid.x,2) + pow(self.posGrid.y +1 - self.app.player.posGrid.y,2)))
						d = abs(self.posGrid.x - self.app.player.posGrid.x) + abs((self.posGrid.y+1) - self.app.player.posGrid.y)
						#left
					elif x == vec(-1,0):
						#l = math.sqrt(abs(pow(self.posGrid.x-1 - self.app.player.posGrid.x,2) + pow(self.posGrid.y - self.app.player.posGrid.y,2)))
						l = abs((self.posGrid.x-1) - self.app.player.posGrid.x) + abs(self.posGrid.y - self.app.player.posGrid.y)
						#right
					elif x == vec(1,0):
						#r = math.sqrt(abs(pow(self.posGrid.x+1 - self.app.player.posGrid.x,2) + pow(self.posGrid.y - self.app.player.posGrid.y,2)))
						r = abs((self.posGrid.x+1) - self.app.player.posGrid.x) + abs(self.posGrid.y - self.app.player.posGrid.y)

				distances = (u,d,l,r)
				best = distances.index(min(distances))

				if best == 0:
					self.direction = vec(0,-1)
				elif best == 1:
					self.direction = vec(0,1)
				elif best == 2:
					self.direction = vec(-1,0)
				else:
					self.direction = vec(1,0)
				self.smartMoveCount += 1	

		

	def update(self):
		self.move()
		self.update_essential()