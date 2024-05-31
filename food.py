from settings import *
from random import randint

class Food(pygame.sprite.Sprite):
    
    def __init__(self, group):

        super().__init__(group)

        self.image = pygame.surface.Surface((PADDING,PADDING))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.x = randint(0,GAME_WIDTH-PADDING) #have to fix, spawn location not aligned with grid pattern
        self.y = randint(0,GAME_HEIGHT-PADDING)
        self.rect.topleft = (self.x,self.y)
        self.eaten = False

        