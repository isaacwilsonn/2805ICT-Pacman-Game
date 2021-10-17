from pygame.math import Vector2 as vec

# display settings
BORDER_BUFFER = 63
WIDTH, HEIGHT = 763, 838#610, 670
mWIDTH, mHEIGHT = WIDTH - BORDER_BUFFER, HEIGHT - BORDER_BUFFER
FPS = 60

# color settings
white=(255, 255, 255)
black=(0, 0, 0)
black_trans = (0,0,0,40)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
TRANSPARENT = (0, 0, 0)

MENU_FONT = "assets/fonts/Emulogic.ttf"
MENU_FONT_LARGE = 35
MENU_FONT_SMALL = 17

# player settings
START_POS_PLAYER = vec(14,23)
START_POS_PLAYER_RAND = vec(14,21)

# mob settings