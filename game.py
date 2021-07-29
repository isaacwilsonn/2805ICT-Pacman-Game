from globalVariables import *

def play():
	window.fill(black)
	pygame.display.update()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False