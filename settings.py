import pygame

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 620

PADDING = 20

GAME_WIDTH = SCREEN_WIDTH-2*PADDING
GAME_HEIGHT = GAME_WIDTH
GRID_CELL = 20
GRID_DIM = int(GAME_WIDTH/GRID_CELL)

PANEL_WIDTH = GAME_WIDTH
PANEL_HEIGHT = SCREEN_HEIGHT-3*PADDING-GAME_HEIGHT

BACKGROUND_COLOR = (30,30,30)
GAME_COLOR = (120,45,12)
PANEL_COLOR = (110,40,5)
SNAKE_BODY_COLOR = (0,100,0)
SNAKE_HEAD_COLOR = (0,200,0)
FONT_COLOR = (255,255,255)

FPS = 50

#global variables
SCORE = 0

def set_score(score):
    global SCORE
    SCORE = score

def get_score():
    return SCORE

POPULATION_SIZE = 1

def set_population(size):
    global POPULATION_SIZE
    POPULATION_SIZE = size

def get_population():
    return POPULATION_SIZE

GENERATION_COUNT = 0

def incr_gen():
    global GENERATION_COUNT
    GENERATION_COUNT += 1

def get_gen():
    return GENERATION_COUNT

MAX_SCORE = 0

def set_max_score(score):
    global MAX_SCORE    
    MAX_SCORE = score   

def get_max_score():
    return MAX_SCORE
