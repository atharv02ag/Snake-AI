from settings import *
from random import randint

#Food sprite class
class Food(pygame.sprite.Sprite):
    
    def __init__(self, group):

        super().__init__(group)

        self.image = pygame.surface.Surface((GRID_CELL,GRID_CELL))
        self.image.fill(FOOD_COLOR)
        self.rect = self.image.get_rect()
        self.x = GRID_CELL*randint(0,GRID_DIM-1) 
        self.y = GRID_CELL*randint(0,GRID_DIM-1)
        self.rect.topleft = (self.x,self.y)

        