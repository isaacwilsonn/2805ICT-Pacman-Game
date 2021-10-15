import pygame
import sys
from player import *
from maze_walls import *
from settings import *
from sprites import Spritesheet
from ghost import *
from food import *

pygame.init()
vec = pygame.math.Vector2


class App:
	def __init__(self):
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
		self.state = 'mMenu'
		self.sel = 'play'
		self.cellWidth = mWIDTH//28
		self.cellHeight = mHEIGHT//30
		self.spriteSheet = Spritesheet()
		self.canWallCollide = True
		self.randomMaze = False
		self.config = False
		self.score = 0

		self.player = None
		self.sGhosts = []
		self.dGhosts = []
		self.walls = []
		self.mWalls = []
		self.food = []
		self.mfood = []

		#spawn ghosts hardcode
		self.spawnGhosts(vec(11,11),"yellow", "smart")
		self.spawnGhosts(vec(14,11),"red", "smart")
		self.spawnGhosts(vec(13,18),"blue")
		self.spawnGhosts(vec(15,18),"pink")

		#sounds
		self.snd_mainMenu = pygame.mixer.Sound('assets/sound_effects/pacman_mainMenu.wav')
		self.snd_powerPellet = pygame.mixer.Sound('assets/sound_effects/pacman_powerpellet.wav')
		self.snd_chomp = pygame.mixer.Sound('assets/sound_effects/pacman_chomp.wav')
		self.snd_eatGhost = pygame.mixer.Sound('assets/sound_effects/pacman_eatghost.wav')
		self.snd_pacmanDeath = pygame.mixer.Sound('assets/sound_effects/pacman_death.wav')
		self.snd_ghostSiren = pygame.mixer.Sound('assets/sound_effects/pacman_ghostSiren.wav')


		self.load()

		pygame.display.set_caption('Pacman')

		pygame.display.set_icon(self.icon)

	def run(self):
		self.snd_mainMenu.play(0,0)
		while self.running:
			if self.state == 'mMenu':
				self.mMenu_events()
				self.mMenu_update()
				self.mMenu_draw()
			elif self.state == 'playing':
				self.game_events()
				self.game_update()
				self.game_draw()
			else:
				self.running = True
			self.clock.tick(FPS)
		pygame.quit()
		sys.exit()

#########################	Helper Functions 	#########################
	# Text Renderer
	def drawText (self, text, screen, pos, font, size, color, center = False):
		nFont=pygame.font.Font(font, size)
		nText=nFont.render(text, 0, color)
		textSize = nText.get_size()
		if center:
			pos[0] = pos[0]-textSize[0]//2
			pos[1] = pos[1]-textSize[1]//2
		screen.blit(nText, pos)

	def load(self):
		self.mazeBG = pygame.image.load('assets/img/maze.png')
		self.mazeBG = pygame.transform.scale(self.mazeBG, (mWIDTH, mHEIGHT))

		self.title = pygame.image.load('assets/img/pacman-title.png')
		self.icon = pygame.image.load('assets/img/pacman-icon.png')

	def spawnGhosts(self, pos, color = "red", ai="dumb"):
		if ai == "smart":
			self.sGhosts.append(sGhost(self, pos, self.spriteSheet, color))
		else:
			self.dGhosts.append(dGhost(self, pos, self.spriteSheet, color))


	def createWalls(self, default=True):
		if default:
			self.createDefaultWalls()
		else:
			self.createDefaultWalls(False)
		self.mirrorMaze()

	def spawnFood(self):
		#self.spawnPowerPellets()
		self.spawnPellet()
		self.mirrorFood()
	
	#draw grid for debugging 
	def drawGrid(self):
		for i in range(WIDTH//self.cellWidth):
			pygame.draw.line(self.screen, gray, (i*self.cellWidth,0),(i*self.cellWidth,HEIGHT))
		for i in range(HEIGHT//self.cellHeight):
			pygame.draw.line(self.screen, gray, (0, i*self.cellHeight),(WIDTH, i*self.cellHeight))

	#########################	Main Menu State 	#########################

	def mMenu_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type==pygame.KEYDOWN:
				if not self.config:
					if event.key==pygame.K_UP:
						if self.sel == "config":
							self.sel = "play"
						elif self.sel == "exit":
							self.sel = "config"
					if event.key==pygame.K_DOWN:
						if self.sel == "play":
							self.sel = "config"
						elif self.sel == "config":
							self.sel = "exit"
					if event.key==pygame.K_RETURN:
						if self.sel =="play":
							#create walls
							self.snd_mainMenu.stop()
							if self.randomMaze:
								self.player = Player(self, START_POS_PLAYER_RAND, self.spriteSheet)
								self.player.get_posPx()
								self.createWalls(False)
							else:
								self.createWalls()
								self.player = Player(self, START_POS_PLAYER, self.spriteSheet)
							self.spawnFood()
							self.state = 'playing'
						elif self.sel == "config":
							self.config = True
							if self.randomMaze == True:
								self.sel='config-random'
							else:
								self.sel='config-standard'
						elif self.sel =="exit":
							self.running = False
				else:
					if event.key==pygame.K_UP:
						if self.sel == "config-random":
							self.sel = "config-standard"
						elif self.sel == "config-back":
							self.sel = "config-random"
					if event.key==pygame.K_DOWN:
						if self.sel == "config-standard":
							self.sel = "config-random"
						elif self.sel == "config-random":
							self.sel = "config-back"
					if event.key==pygame.K_RETURN:
						if self.sel =="config-random":
							self.randomMaze = True;
						elif self.sel == "config-standard":
							self.randomMaze = False
						self.sel = 'config'
						self.config = False

	def mMenu_update(self):
		pass

	def mMenu_draw(self):
		self.screen.fill(black)

		self.screen.blit(self.title, (WIDTH/2-300, 120))

		if self.config:
			if self.sel == 'config-standard':
				self.drawText('Standard',self.screen, [WIDTH//2, HEIGHT//2], MENU_FONT, MENU_FONT_LARGE, yellow, True)
			else:
				self.drawText('Standard',self.screen, [WIDTH//2, HEIGHT//2], MENU_FONT, MENU_FONT_LARGE, white, True)
			if self.sel == 'config-random':
				self.drawText('Random',self.screen, [WIDTH//2, HEIGHT//2+65], MENU_FONT, MENU_FONT_LARGE, yellow, True)
			else:
				self.drawText('Random',self.screen, [WIDTH//2, HEIGHT//2+65], MENU_FONT, MENU_FONT_LARGE, white, True)
			if self.sel == 'config-back':
				self.drawText('Back',self.screen, [WIDTH//2, HEIGHT//2+130], MENU_FONT, MENU_FONT_LARGE, yellow, True)
			else:
				self.drawText('Back',self.screen, [WIDTH//2, HEIGHT//2+130], MENU_FONT, MENU_FONT_LARGE, white, True)
		else:
			if self.sel == 'play':
				self.drawText('Play',self.screen, [WIDTH//2, HEIGHT//2], MENU_FONT, MENU_FONT_LARGE, yellow, True)
			else:
				self.drawText('Play',self.screen, [WIDTH//2, HEIGHT//2], MENU_FONT, MENU_FONT_LARGE, white, True)
			if self.sel == 'config':
				self.drawText('Configure',self.screen, [WIDTH//2, HEIGHT//2+65], MENU_FONT, MENU_FONT_LARGE, yellow, True)
			else:
				self.drawText('Configure',self.screen, [WIDTH//2, HEIGHT//2+65], MENU_FONT, MENU_FONT_LARGE, white, True)
			if self.sel == 'exit':
				self.drawText('Exit',self.screen, [WIDTH//2, HEIGHT//2+130], MENU_FONT, MENU_FONT_LARGE, yellow, True)
			else:
				self.drawText('Exit',self.screen, [WIDTH//2, HEIGHT//2+130], MENU_FONT, MENU_FONT_LARGE, white, True)


		#Course and students
		self.drawText("2805ICT - 2021", self.screen, [0,680], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Harry Rowe", self.screen, [0,710], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Isaac Wilson",self.screen, [0,740], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Isaac Wingate", self.screen, [0,770], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Krittawat Auskulsuthi", self.screen, [0,800], MENU_FONT, MENU_FONT_SMALL, blue)

		#high score
		self.drawText('HIGH SCORE:', self.screen, [4,0], MENU_FONT, 14, white)

		pygame.display.update()

	#########################	Playing State 	#########################

	def game_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.player.move(vec(0,-self.player.speed))
				if event.key == pygame.K_DOWN:
					self.player.move(vec(0,self.player.speed))
				if event.key == pygame.K_LEFT:
					self.player.move(vec(-self.player.speed,0))
				if event.key == pygame.K_RIGHT:
					self.player.move(vec(self.player.speed,0))

	def game_update(self):
		self.drawText('Score:' + str(self.score),  self.screen, [10,2.5], MENU_FONT, 15, white)

		self.player.update()
		self.player.wallCollide()

		#smart ghosts
		for ghost in self.sGhosts:
			ghost.update()

		#dumb ghosts
		for ghost in self.dGhosts:
			ghost.update()
		
		#update food (check collision)
		for food in self.food:
			food.update()


	def game_draw(self):
		self.screen.fill(black)
		
		self.drawText('Score:' + str(self.score),  self.screen, [10,2.5], MENU_FONT, 15, white)
		self.drawText('HIGH SCORE: 0', self.screen, [WIDTH-250,2.5], MENU_FONT, 15, white)
		self.drawText("Lives: " + str(self.player.lives), self.screen, [WIDTH//2-50, HEIGHT-30], MENU_FONT, 15, white)
		
		
		self.player.draw()

		for ghost in self.sGhosts:
			ghost.draw()
		for ghost in self.dGhosts:
			ghost.draw()

		for wall in self.walls:
			wall.draw()

		#draw grid for debug purposes
		#self.drawGrid()

		# draw food
		for food in self.food:
				food.draw(food.foodType)

		pygame.display.update()


############################## MAZE CREATION

	def createDefaultWalls(self, default=True):
		ignores = ['BLANK','NONE','PP']
		if default:
			fname = 'def_maze_layout.txt'
		else:
			self.randomiseMaze()
			fname = 'rand_maze.txt'
		x = 0
		y = 0
		with open(fname,'r') as file:
			for line in file:
				x = 0
				for word in line.split():
					if word not in ignores:
						self.walls.append(Wall(self,vec(x,y),word))
					x+=1
				y+=1

	def randomiseMaze(self):
		maze = []
		accepted =['VERT','HORI','BLANK','PP','NONE','TOP_LEFT','BOT_LEFT','TOP_RIGHT','BOT_RIGHT']
		#read maze into a 2d array
		with open('rand_maze_template.txt','r') as file:
			for line in file:
				temp = []
				for word in line.split():
					if word in accepted:
						temp.append(word)
				maze.append(temp)


		########################## VERT GATES ############################
		# possible gateways
		v1 = random.randint(2,4)
		v2 = random.randint(1,3)
		print(v1,v2)
		vert1x = [3,4]	#min and max's
		vert1y = [6,23]
		vert2x = [6,7]
		vert2y = [9,20]

		#vert 1
		vert1_gates = []
		vert1_gates.append(random.randint(vert1y[0],vert1y[1]))
		while len(vert1_gates) < v1:
			accept = True
			y = random.randint(vert1y[0],vert1y[1])
			for x in vert1_gates:
				if abs(x-y) < 3:
					accept = False
			if accept:
				vert1_gates.append(y)

		
		vert2_gates = []
		vert2_gates.append(random.randint(vert2y[0],vert2y[1]))
		while len(vert2_gates) < v2:
			accept = True
			y = random.randint(vert2y[0],vert2y[1])
			for x in vert2_gates:
				if abs(x-y) < 3:
					accept = False
			if accept:
				vert2_gates.append(y)

		for y in vert1_gates:
			maze[y][vert1x[0]] = 'BLANK'
			maze[y][vert1x[1]] = 'BLANK'
			# set corners above
			maze[y-1][vert1x[0]] = 'BOT_LEFT'
			maze[y-1][vert1x[1]] = 'BOT_RIGHT'
			# set corners below
			maze[y+1][vert1x[0]] = 'TOP_LEFT'
			maze[y+1][vert1x[1]] = 'TOP_RIGHT'


		for y in vert2_gates:
			maze[y][vert2x[0]] = 'BLANK'
			maze[y][vert2x[1]] = 'BLANK'
			# set corners above
			maze[y-1][vert2x[0]] = 'BOT_LEFT'
			maze[y-1][vert2x[1]] = 'BOT_RIGHT'
			# set corners below
			maze[y+1][vert2x[0]] = 'TOP_LEFT'
			maze[y+1][vert2x[1]] = 'TOP_RIGHT'

		########################## HORI BOTTOM GATES ############################
		h1 = random.randint(1,2)
		h2 = random.randint(0,1)


		hori1x = [6,12]	#min and max's
		hori1y = [25,26]
		hori2x = [9,12]
		hori2y = [22,23]


		#hori 1
		hori1_gates = []
		hori1_gates.append(random.randint(hori1x[0],hori1x[1]))
		while len(hori1_gates) < h1:
			accept = True
			x = random.randint(hori1x[0],hori1x[1])
			for y in hori1_gates:
				if abs(x-y) < 3:
					accept = False
			if accept:
				hori1_gates.append(x)
		
		hori2_gates = []
		hori2_gates.append(random.randint(hori2x[0],hori2x[1]))
		while len(hori2_gates) < h2:
			accept = True
			x = random.randint(hori2x[0],hori2x[1])
			for y in hori2_gates:
				if abs(x-y) < 3:
					accept = False
			if accept:
				hori2_gates.append(x)


		for x in hori1_gates:
			maze[hori1y[0]][x] = 'BLANK'
			maze[hori1y[1]][x] = 'BLANK'
			# set corners above
			maze[hori1y[0]][x-1] = 'TOP_RIGHT'
			maze[hori1y[1]][x-1] = 'BOT_RIGHT'
			# set corners below
			maze[hori1y[0]][x+1] = 'TOP_LEFT'
			maze[hori1y[1]][x+1] = 'BOT_LEFT'


		for x in hori2_gates:
			maze[hori2y[0]][x] = 'BLANK'
			maze[hori2y[1]][x] = 'BLANK'
			# set corners above
			maze[hori2y[0]][x-1] = 'TOP_RIGHT'
			maze[hori2y[1]][x-1] = 'BOT_RIGHT'
			# set corners below
			maze[hori2y[0]][x+1] = 'TOP_LEFT'
			maze[hori2y[1]][x+1] = 'BOT_LEFT'


		########################## HORI TOP GATES ############################
		h3 = random.randint(1,2)
		h4 = random.randint(0,1)

		hori3x = [6,12]	#min and max's
		hori3y = [3,4]
		hori4x = [9,12]
		hori4y = [6,7]


		#hori 1
		hori3_gates = []
		hori3_gates.append(random.randint(hori3x[0],hori3x[1]))
		while len(hori3_gates) < h3:
			accept = True
			x = random.randint(hori3x[0],hori3x[1])
			for y in hori3_gates:
				if abs(x-y) < 3:
					accept = False
			if accept:
				hori3_gates.append(x)
		
		hori4_gates = []
		hori4_gates.append(random.randint(hori4x[0],hori4x[1]))
		while len(hori4_gates) < h2:
			accept = True
			x = random.randint(hori4x[0],hori4x[1])
			for y in hori4_gates:
				if abs(x-y) < 3:
					accept = False
			if accept:
				hori4_gates.append(x)


		for x in hori3_gates:
			maze[hori3y[0]][x] = 'BLANK'
			maze[hori3y[1]][x] = 'BLANK'
			# set corners above
			maze[hori3y[0]][x-1] = 'TOP_RIGHT'
			maze[hori3y[1]][x-1] = 'BOT_RIGHT'
			# set corners below
			maze[hori3y[0]][x+1] = 'TOP_LEFT'
			maze[hori3y[1]][x+1] = 'BOT_LEFT'


		for x in hori4_gates:
			maze[hori4y[0]][x] = 'BLANK'
			maze[hori4y[1]][x] = 'BLANK'
			# set corners above
			maze[hori4y[0]][x-1] = 'TOP_RIGHT'
			maze[hori4y[1]][x-1] = 'BOT_RIGHT'
			# set corners below
			maze[hori4y[0]][x+1] = 'TOP_LEFT'
			maze[hori4y[1]][x+1] = 'BOT_LEFT'

		#make edits to the maze
		x = 0
		y = 0
		for line in maze:
			x = 0
			for word in line:
				#change walls based on conditions and rands
				x+=1
			y+=1



		#print edited maze to file		
		with open ('rand_maze.txt','w') as file:
			for line in maze:
				for wall in line:
					file.write(wall+' ')
				file.write('\n')




				


	def mirrorMaze(self):
		print("len walls: ", len(self.walls))
		for w in self.walls:
			x = 27-w.posGrid[0]
			y = w.posGrid[1]
			wType = w.wType

			if wType == 'BOT_LEFT':
				wType = 'BOT_RIGHT'
			elif wType == 'BOT_RIGHT':
				wType = 'BOT_LEFT'
			elif wType == 'TOP_LEFT':
				wType = 'TOP_RIGHT'
			elif wType == 'TOP_RIGHT':
				wType = 'TOP_LEFT'
			
			self.mWalls.append(Wall(self,vec(x,y),wType))
		for w in self.mWalls:
			self.walls.append(w)

	def spawnPowerPellets(self):
		'''only spawn the power pellets in here.'''
		#how to approach this when doing random generation?
		#get a random x,y coord. check if position in walls list, check if positon is blank, put a food object?
		#else new random number?
		#self.food.append(Food(self, vec(1, 5), True)) #top left
		#self.food.append(Food(self, vec(1, 23), True)) #bottom left

	def spawnPellet(self):
		if self.randomMaze:
			fname = 'rand_maze.txt'
		else:
			fname = 'def_maze_layout.txt'

		with open(fname,'r') as file:
			y = 0
			for line in file:
				x = 0
				for word in line.split():
					if word == 'BLANK': 
							self.food.append(Food(self, vec(x, y), False))
					elif word == 'PP':
						self.food.append(Food(self, vec(x, y), True))
					x+=1
				y+=1
		
		#potentially use something like this to check for power pellets.
		#for food in self.food:
		#	if food.posGrid == [1, 5]:
		#		print("in")

	def mirrorFood(self):
		for food in self.food:
			x = 27-food.posGrid[0]
			y = food.posGrid[1]
			self.mfood.append(Food(self,vec(x,y),food.foodType))
		
		for food in self.mfood:
			self.food.append(food)
	
	def resetGhosts(self):
		for g in self.dGhosts:
			if g.color == 'blue':
				g.posGrid = vec(12,14)
				g.posPx = g.get_posPx()
			if g.color == 'pink':
				g.posGrid = vec(15,14)
				g.posPx = g.get_posPx()

		for g in self.sGhosts:
			if g.color == 'red':
				g.posGrid = vec(14,11)
				g.posPx = g.get_posPx()
			if g.color == 'yellow':
				g.posGrid = vec(13,14)
				g.posPx = g.get_posPx()
