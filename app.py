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

		self.player = Player(self, START_POS_PLAYER, self.spriteSheet)
		self.sGhosts = []
		self.dGhosts = []
		self.walls = []
		self.mWalls = []
		self.food = []

		#spawn ghosts hardcode
		self.spawnGhosts(vec(11,11),"yellow", "smart")
		self.spawnGhosts(vec(26,29),"red", "smart")
		self.spawnGhosts(vec(15,11),"blue")
		self.spawnGhosts(vec(15,17),"pink")

		self.spawnFood();

		#sounds
		self.snd_mainMenu = pygame.mixer.Sound('assets/sound_effects/pacman_mainMenu.wav')
		self.snd_powerPellet = pygame.mixer.Sound('assets/sound_effects/pacman_powerpellet.mp3')
		self.snd_chomp = pygame.mixer.Sound('assets/sound_effects/pacman_chomp.wav')
		self.snd_eatGhost = pygame.mixer.Sound('assets/sound_effects/pacman_eatghost.wav')
		self.snd_pacmanDeath = pygame.mixer.Sound('assets/sound_effects/pacman_death.wav')
		self.snd_ghostSiren = pygame.mixer.Sound('assets/sound_effects/pacman_ghostSiren.mp3')


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

	def spawnFood(self):
		pos = vec(1,1)
		self.food.append(food(self, pos))

	def createWalls(self):
		self.createDefaultWalls()
		self.mirrorMaze()

	#draw grid for debugging 
	def drawGrid(self):
		for i in range(WIDTH//self.cellWidth):
			pygame.draw.line(self.mazeBG, gray, (i*self.cellWidth,0),(i*self.cellWidth,HEIGHT))
		for i in range(HEIGHT//self.cellHeight):
			pygame.draw.line(self.mazeBG, gray, (0, i*self.cellHeight),(WIDTH, i*self.cellHeight))

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
							self.createWalls()
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

		#draw grid for debug purposes
		#self.drawGrid()
		
		self.drawText('SCORE: 0', self.screen, [10,2.5], MENU_FONT, 15, white)
		self.drawText('HIGH SCORE: 0', self.screen, [WIDTH-250,2.5], MENU_FONT, 15, white)
		#add lives to game screen
		self.drawText("Lives: " + str(self.player.lives), self.screen, [WIDTH//2-50, HEIGHT-30], MENU_FONT, 15, white)
		
		
		self.player.draw()

		for ghost in self.sGhosts:
			ghost.draw()
		for ghost in self.dGhosts:
			ghost.draw()

		if self.randomMaze:
			pass
		else:
			for wall in self.walls:
				wall.draw()

		# draw food
		for food in self.food:
			food.draw()

		pygame.display.update()


############################## MAZE CREATION

	def createDefaultWalls(self):

		x = 0
		y = 0
		with open('def_maze_layout.txt','r') as file:
			for line in file:
				x = 0
				for word in line.split():
					if word != 'BLANK':
						self.walls.append(Wall(self,vec(x,y),word))
					x+=1
				y+=1



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
