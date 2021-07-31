from globalVariables import *
import menus

def play():
	window.fill(gray)
	pygame.display.update()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					if(menus.pause_menu() == 1):
						window.fill(gray)
						pygame.display.update()
						clock.tick(FPS)
					else:
						return