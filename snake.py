from settings import *

class Part(pygame.sprite.Sprite):

    def __init__(self,group,color,x,y,dir):
        super().__init__(group)
        self.image = pygame.surface.Surface((GRID_CELL,GRID_CELL))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (self.x,self.y)
        self.dir = dir #direction of motion - (1,0), (-1,0), (0,1), (0,-1)

    def update(self):
        self.rect.topleft = (self.x,self.y)

class Snake(pygame.sprite.Sprite):

    def __init__(self,group):
        self.head = Part(group,SNAKE_HEAD_COLOR,0,0,(1,0))
        self.parts = [self.head]
        self.v_x = 1*GRID_CELL
        self.v_y = 0

    def move(self):
        prev_pos = (self.head.x,self.head.y)
        prev_dir = self.head.dir
    
        for part in self.parts:
            if(part == self.head):
                part.x += self.v_x
                part.y += self.v_y
            else:
                temp_pos = (part.x,part.y)
                (part.x,part.y) = prev_pos
                prev_pos = temp_pos

                temp_dir = part.dir
                part.dir = prev_dir
                prev_dir = temp_dir
    
    def append_part(self, group):
        last_part = self.parts[len(self.parts)-1]
        pos = (last_part.x-last_part.dir[0]*GRID_CELL, last_part.y-last_part.dir[1]*GRID_CELL)
        new_part = Part(group,SNAKE_BODY_COLOR,pos[0],pos[1],last_part.dir)
        self.parts.append(new_part)