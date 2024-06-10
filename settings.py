import pygame
pygame.mixer.init()

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 800

PADDING = 20

GAME_WIDTH = SCREEN_WIDTH-2*PADDING
GAME_HEIGHT = GAME_WIDTH
GRID_CELL = 20
GRID_DIM = int(GAME_WIDTH/GRID_CELL)

#time in ms between movements of snake. Speed would be 1/SNAKE_TIME
SNAKE_TIME = 120
INPUT_TIME = 50

PANEL_WIDTH = GAME_WIDTH
PANEL_HEIGHT = SCREEN_HEIGHT-3*PADDING-GAME_HEIGHT

BACKGROUND_COLOR = (30,30,30)
GAME_COLOR = (126,217,87)
PANEL_COLOR = (29, 194, 84)
SNAKE_BODY_COLOR = (0,100,0)
SNAKE_HEAD_COLOR = (0,200,0)
FONT_COLOR = (255,255,255)
EATSOUND=pygame.mixer.Sound(".\yaudio\munch.mp3")
TURNSOUND=pygame.mixer.Sound(".\yaudio\Turning.mp3")
FPS = 300

#global variables
SCORE = 0

def set_score(score):
    global SCORE
    SCORE = score

def get_score():
    return SCORE