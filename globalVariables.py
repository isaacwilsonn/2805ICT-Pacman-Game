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