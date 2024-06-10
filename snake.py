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

    def __init__(self,group,x_init,y_init):
        self.head = Part(group,SNAKE_HEAD_COLOR,x_init,y_init,(1,0))
        self.parts = [self.head]
        self.v_x = 1*GRID_CELL
        self.v_y = 0
        self.visited = [[0 for i in range(0,GRID_DIM+1)] for j in range(0,GRID_DIM+1)]
        self.closer_to_food = 0

    #if move() went closer to x,y returns 1 else 0
    def move(self,x,y):
        prev_pos = (self.head.x,self.head.y)
        prev_dir = self.head.dir

        dist1 = abs(self.head.x-x) + abs(self.head.y-y)

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
        
        dist2 = abs(self.head.x-x) + abs(self.head.y-y)

        self.closer_to_food = 1 if(dist2<dist1) else 0
        
        self.update_visited()
 
    def append_part(self, group):
        last_part = self.parts[len(self.parts)-1]
        pos = (int(last_part.x)-int(last_part.dir[0]*GRID_CELL), int(last_part.y)-int(last_part.dir[1]*GRID_CELL))
        new_part = Part(group,SNAKE_BODY_COLOR,pos[0],pos[1],last_part.dir)
        self.parts.append(new_part)

    def update_visited(self):
        vis_x = int(self.head.x/GRID_CELL)
        vis_y = int(self.head.y/GRID_CELL)
        if(vis_x >=0 and vis_y >= 0 and vis_x <= GRID_DIM and vis_y <= GRID_DIM):
            #print(f"{vis_x}, {vis_y}")
            self.visited[vis_x][vis_y] += 1
        #print(self.visited)