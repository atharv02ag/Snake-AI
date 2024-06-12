from settings import *
from food import Food
from snake import Snake
from timer import Timer

class Game():

    def __init__(self):
        self.game_screen = pygame.surface.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.game_rect = self.game_screen.get_rect(bottomleft=(PADDING,(SCREEN_HEIGHT-PADDING)))
        self.screen = pygame.display.get_surface()

        self.food = pygame.sprite.GroupSingle()
        food = Food(self.food)
        self.snake_sprites = pygame.sprite.Group()
        self.snake = Snake(self.snake_sprites) 
    
    def take_action(self,action):
        #actions - left = [1,0,0], straight = [0,1,0], right = [0,0,1]
        clockwise = [(0,-1), (1,0), (0,1), (-1,0)] #up right down left
        index = clockwise.index(self.snake.head.dir)
        if(action[0]==1):
            self.snake.head.dir = clockwise[(index-1)%4]
        elif(action[1]==1):
            self.snake.head.dir = clockwise[index]
        elif(action[2]==1):
            self.snake.head.dir = clockwise[(index+1)%4]
        (self.snake.v_x, self.snake.v_y) = (self.snake.head.dir[0]*GRID_CELL,self.snake.head.dir[1]*GRID_CELL)

    def check_boundary(self):
        reward = 0
        game_over = False
        if(self.snake.head.x < 0 or self.snake.head.x >= GAME_WIDTH or
           self.snake.head.y < 0 or self.snake.head.y >= GAME_HEIGHT): 
            reward = -10
            game_over = True      
        return reward, game_over

    def respawn_food(self):
        self.food.sprite = Food(self.food)

    def check_food(self): #TODO adding part somehow causing collision with self
        reward = 0
        if(pygame.sprite.groupcollide(self.food,self.snake_sprites,False,False)):
            self.respawn_food()
            self.snake.append_part(self.snake_sprites)
            reward = 10
            set_score(len(self.snake.parts)-1)
        return reward

    def check_self_collision(self):
        reward = 0
        game_over = False
        for part in self.snake.parts:
            if(part != self.snake.head and pygame.sprite.collide_rect(part,self.snake.head)):
                #self.reset()
                reward = -10
                game_over = True
                break
        return reward, game_over

    def reset(self):
        set_score(0)
        self.respawn_food()
        self.snake_sprites.empty()
        self.snake = Snake(self.snake_sprites)

    def get_state(self):
        dir = [0,0,0,0] #up right down left
        if(self.snake.head.dir == (0,-1)):
            dir[0] = 1
        elif(self.snake.head.dir == (1,0)):
            dir[1] = 1
        elif(self.snake.head.dir == (0,1)):
            dir[2] = 1
        elif(self.snake.head.dir == (-1,0)):
            dir[3] = 1
        
        food_pos = [0,0,0,0] #up right down left
        if(self.snake.head.x < self.food.sprite.x):
            food_pos[1] = 1
        elif(self.snake.head.x > self.food.sprite.x):
            food_pos[3] = 1
        if(self.snake.head.y < self.food.sprite.y):
            food_pos[2] = 1
        elif(self.snake.head.y > self.food.sprite.y):
            food_pos[0] = 1

        boundary = [0,0,0] #left straight right
        (x,y) = (self.snake.head.x,self.snake.head.y)

        if(dir[0]): #if moving up
            boundary[0] = 1 if(x-GRID_CELL<0) else 0
            boundary[1] = 1 if(y-GRID_CELL<0) else 0
            boundary[2] = 1 if(x+GRID_CELL>=GAME_WIDTH) else 0
        elif(dir[1]): #if moving right
            boundary[0] = 1 if(y-GRID_CELL<0) else 0
            boundary[1] = 1 if(x+GRID_CELL>=GAME_WIDTH) else 0
            boundary[2] = 1 if(y+GRID_CELL>=GAME_HEIGHT) else 0
        elif(dir[2]): #if moving down
            boundary[0] = 1 if(x+GRID_CELL>=GAME_WIDTH) else 0
            boundary[1] = 1 if(y+GRID_CELL>=GAME_HEIGHT) else 0
            boundary[2] = 1 if(x-GRID_CELL<0) else 0
        elif(dir[3]): #if moving left
            boundary[0] = 1 if(y+GRID_CELL>=GAME_HEIGHT) else 0
            boundary[1] = 1 if(x-GRID_CELL<0) else 0
            boundary[2] = 1 if(y-GRID_CELL<0) else 0
        
        state = dir + food_pos + boundary
        return state
        
    def take_step(self,action):
        self.take_action(action)
        self.snake.move()

        boundary_reward,boundary_game_over = self.check_boundary()
        food_reward = self.check_food()
        collision_reward = 0
        collision_game_over = False

        if(food_reward != 0):
            collision_reward, collision_game_over = self.check_self_collision()
        
        reward = boundary_reward + food_reward + collision_reward
        game_over = boundary_game_over or collision_game_over
        return reward, game_over
        
        
    def render_ui(self):
        self.screen.blit(self.game_screen, self.game_rect)
        self.game_screen.fill(GAME_COLOR) #VERY IMPORTANT : TO FILL OVER (CLEAR) CONTENTS OF PREVIOUS FRAME
   
        self.snake_sprites.update()

        self.snake_sprites.draw(self.game_screen)
        self.food.draw(self.game_screen)