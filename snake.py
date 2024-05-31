from settings import *

class Part(pygame.sprite.Sprite):

    def __init__(self,group,color):
        super().__init__(group)
        self.image = pygame.surface.Surface((GRID_CELL,GRID_CELL))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.rect.topleft = (self.x,self.y)

    def update(self):
        self.rect.topleft = (self.x,self.y)

class Snake(pygame.sprite.Sprite):

    def __init__(self,group):
        self.head = Part(group,SNAKE_HEAD_COLOR)
        self.parts = [self.head]
        self.v_x = 1*GRID_CELL
        self.v_y = 0

    def move(self):
        for part in self.parts:
            part.x += self.v_x
            part.y += self.v_y