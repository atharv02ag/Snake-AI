from settings import *
from random import randint

class Food(pygame.sprite.Sprite):
    
    def __init__(self, group):

        super().__init__(group)

        self.image = pygame.transform.scale(pygame.image.load(".\images\gameapple.png"),(20,20))
        
        self.rect = self.image.get_rect()
        self.x = GRID_CELL*randint(0,GRID_DIM-1) 
        self.y = GRID_CELL*randint(0,GRID_DIM-1)
        self.rect.topleft = (self.x,self.y)

        