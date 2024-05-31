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

        self.timers = {"MOVE" : Timer(SNAKE_TIME,self.snake.move),
                       "INPUT" : Timer(INPUT_TIME,self.input)}
    
    def input(self):
        keys = pygame.key.get_pressed()

        if(keys[pygame.K_UP]):
            self.snake.v_x = 0
            self.snake.v_y = (-1)*GRID_CELL
            self.snake.head.dir = (0,-1)
        elif(keys[pygame.K_DOWN]):
            self.snake.v_x = 0
            self.snake.v_y = 1*GRID_CELL
            self.snake.head.dir = (0,1)
        elif(keys[pygame.K_RIGHT]):
            self.snake.v_x = 1*GRID_CELL
            self.snake.v_y = 0
            self.snake.head.dir = (1,0)
        elif(keys[pygame.K_LEFT]):
            self.snake.v_x = (-1)*GRID_CELL
            self.snake.v_y = 0
            self.snake.head.dir = (-1,0)

    def check_boundary(self):
        if(self.snake.head.x < 0): #left boundary 
            self.snake.head.x = GAME_WIDTH-GRID_CELL

        elif(self.snake.head.x > GAME_WIDTH): #right boundary
            self.snake.head.x = 0
        
        elif(self.snake.head.y < 0): #top boundary
            self.snake.head.y = GAME_HEIGHT-GRID_CELL
        
        elif(self.snake.head.y > GAME_HEIGHT): #bottom boundary
            self.snake.head.y = 0

    def respawn_food(self):
        self.food.sprite = Food(self.food)

    def check_food(self):

        if(pygame.sprite.groupcollide(self.food,self.snake_sprites,False,False)):
            self.respawn_food()
            self.snake.append_part(self.snake_sprites)
            set_score(len(self.snake.parts)-1)

    def check_self_collision(self):
        for part in self.snake.parts:
            if(part != self.snake.head and pygame.sprite.collide_rect(part,self.snake.head)):
                self.reset()
                break

    def reset(self):
        self.respawn_food()
        self.snake_sprites.empty()
        self.snake = Snake(self.snake_sprites)
        self.timers = {"MOVE" : Timer(SNAKE_TIME,self.snake.move),
                       "INPUT" : Timer(INPUT_TIME,self.input)}

    def run(self):

        self.timers["MOVE"].runTimer()
        self.timers["INPUT"].runTimer()
        self.check_boundary()
        self.check_food()
        self.check_self_collision()
        
        self.screen.blit(self.game_screen, self.game_rect)
        self.game_screen.fill(GAME_COLOR) #VERY IMPORTANT : TO FILL OVER (CLEAR) CONTENTS OF PREVIOUS FRAME
   
        self.snake_sprites.update()

        self.snake_sprites.draw(self.game_screen)
        self.food.draw(self.game_screen)
        