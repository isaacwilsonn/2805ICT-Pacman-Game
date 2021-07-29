import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1080, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2805ICT - Pacman!")

font = "fonts/Emulogic.ttf"
# Text Renderer
def text_format(text, font, size, color):
    nFont=pygame.font.Font(font, size)
    nText=nFont.render(text, 0, color)
 
    return nText
 
 
# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Game Framerate
clock = pygame.time.Clock()
FPS=60

def menu():
	menu=True
	sel = "play"

	while menu:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_UP:
					if sel == "config":
						sel = "play"
					elif sel == "exit":
						sel = "config"
				if event.key==pygame.K_DOWN:
					if sel == "play":
						sel = "config"
					elif sel == "config":
						sel = "exit"
				if event.key==pygame.K_RETURN:
					if sel =="play":
						print("Play")
					elif sel == "config":
						print("config")
					elif sel =="exit":
						pygame.quit()
						quit()

		# Main Menu UI
		window.fill(black)
		title=text_format("Pacman", font, 65, yellow)
		if sel == "play":
		    text_start=text_format("Play", font, 45, yellow)
		else:
		    text_start = text_format("Play", font, 45, white)
		if sel =="config":
		    text_config = text_format("Configure", font, 45, yellow)
		else:
		    text_config = text_format("Configure", font, 45, white)
		if sel =="exit":
		    text_quit = text_format("Exit", font, 45, yellow)
		else:
		    text_quit = text_format("Exit", font, 45, white)

		title_rect=title.get_rect()
		start_rect=text_start.get_rect()
		config_rect=text_config.get_rect()
		quit_rect=text_quit.get_rect()

		# Menu Title
		window.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))

		# Menu Items
		window.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 240))
		window.blit(text_config, (WIDTH/2 - (config_rect[2]/2), 300))
		window.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))

		#Course and students
		text_course = text_format("2805ICT - 2021", font, 15, blue)
		text_student1 = text_format("Harry Rowe", font, 15, blue)
		text_student2 = text_format("Isaac Wilson", font, 15, blue)
		text_student3 = text_format("Isaac Wingate", font, 15, blue)
		text_student4 = text_format("Krittawat Auskulsuthi", font, 15, blue)

		course_rect=title.get_rect()
		student1_rect=title.get_rect()
		student2_rect=title.get_rect()
		student3_rect=title.get_rect()
		student4_rect=title.get_rect()

		window.blit(text_course, (10, 500))
		window.blit(text_student1, (10, 540))
		window.blit(text_student2, (10, 580))
		window.blit(text_student3, (10, 620))
		window.blit(text_student4, (10, 660))

		pygame.display.update()
		clock.tick(FPS)
		pygame.display.set_caption("2805ICT - Pacman")


if __name__ == "__main__":
	menu()
	quit()

