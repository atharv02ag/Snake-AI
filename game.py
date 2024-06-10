from settings import *
from food import Food
from snake import Snake
from timer import Timer
from random import randint

import neat
import neat.config

class Game():

    def __init__(self):
        set_population(1)
        set_score(0)
        self.game_screen = pygame.surface.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.game_rect = self.game_screen.get_rect(bottomleft=(PADDING,(SCREEN_HEIGHT-PADDING)))
        self.screen = pygame.display.get_surface()

        self.food = pygame.sprite.GroupSingle()
        food = Food(self.food)

        self.snakes = []
        self.snake_sprites_all = []
        self.neural_networks = []
        self.timers_all = []
        self.ge = []
        self.start_time = pygame.time.get_ticks()

    def init_neat(self,genomes,config):

        x_init = GRID_CELL*randint(0,GRID_DIM-1) 
        y_init = GRID_CELL*randint(0,GRID_DIM-1)

        for x,g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g,config)
            self.neural_networks.append(net)

            snake_sprites = pygame.sprite.Group()
            self.snake_sprites_all.append(snake_sprites)

            snake = Snake(snake_sprites,x_init,y_init)  
            self.snakes.append(snake)

            timers = {"MOVE" : Timer(SNAKE_TIME,snake.move),
                            "INPUT" : Timer(INPUT_TIME,self.input)}
            self.timers_all.append(timers)

            g.fitness = 0
            self.ge.append(g)

    
    def input(self,x=0,y=0):
        
        for i,snake in enumerate(self.snakes):
            #displ = math.sqrt((snake.head.x-self.food.sprite.x)**2 + (snake.head.y-self.food.sprite.y)**2)
            #print(f"{i} {snake.closer_to_food}")
            # inp_1 = 0
            # inp_2 = 0
            # inp_3 = 0
            # inp_4 = 0
            dist_r = (GAME_WIDTH-snake.head.x)/GRID_CELL
            dist_l = snake.head.x/GRID_CELL
            dist_u = snake.head.y/GRID_CELL
            dist_b = (GAME_HEIGHT-snake.head.y)/GRID_CELL
            # if(self.food.sprite.x == snake.head.x and self.food.sprite.y > snake.head.y):
            #     inp_1 = (self.food.sprite.y - snake.head.y)
            # elif(self.food.sprite.x == snake.head.x and self.food.sprite.y < snake.head.y):
            #     inp_2 = (snake.head.y - self.food.sprite.y)
            # elif(self.food.sprite.y == snake.head.y and self.food.sprite.x > snake.head.x):
            #     inp_3 = (self.food.sprite.x - snake.head.x)
            # elif(self.food.sprite.y == snake.head.y and self.food.sprite.x < snake.head.x):
            #     inp_4 = (snake.head.x - self.food.sprite.x)
            #inp_5 = 1 if (inp_1 or inp_2 or inp_3 or inp_4) else 0

            snake_to_food_vec = pygame.Vector2((self.food.sprite.x-self.snakes[i].head.x),(self.food.sprite.y-self.snakes[i].head.y))
            food_distance = snake_to_food_vec.length()
            food_angle = snake_to_food_vec.as_polar()[1]

            directions = [(0,-1),(0,1),(1,0),(-1,0)]
            opp_directions = {(0,-1) : (0,1), (0,1) : (0,-1),(1,0) : (-1,0),(-1,0) : (1,0)}

            prev_direction = self.snakes[i].head.dir

            output = self.neural_networks[i].activate((food_distance,food_angle,dist_r,dist_l,dist_u,dist_b))
            direction = directions[output.index(max(output))]
            if(prev_direction != (0,0) and opp_directions[prev_direction]==direction):
                self.ge[i].fitness -= 1
            
            (self.snakes[i].v_x, self.snakes[i].v_y) = (direction[0]*GRID_CELL,direction[1]*GRID_CELL)
            self.snakes[i].head.dir = direction
            # if(output[0]>0.5):
            #     self.snakes[i].v_x = 0
            #     self.snakes[i].v_y = (-1)*GRID_CELL
            #     self.snakes[i].head.dir = (0,-1)             
            
            # elif(output[1]>0.5):
            #     self.snakes[i].v_x = 0
            #     self.snakes[i].v_y = 1*GRID_CELL
            #     self.snakes[i].head.dir = (0,1)
                         
            # elif(output[2]>0.5):
            #     self.snakes[i].v_x = 1*GRID_CELL
            #     self.snakes[i].v_y = 0
            #     self.snakes[i].head.dir = (1,0)
                            
            # elif(output[3]>0.5):
            #     self.snakes[i].v_x = (-1)*GRID_CELL
            #     self.snakes[i].v_y = 0
            #     self.snakes[i].head.dir = (-1,0)             

    def check_boundary(self):
        for i,snake in enumerate(self.snakes):
            if(snake.head.x < 0): #left boundary 
                snake.head.x = GAME_WIDTH-GRID_CELL
                self.ge[i].fitness -= 5
                self.snakes.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)

            elif(snake.head.x > GAME_WIDTH-GRID_CELL): #right boundary
                snake.head.x = 0
                self.ge[i].fitness -= 5
                self.snakes.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)

            elif(snake.head.y < 0): #top boundary
                snake.head.y = GAME_HEIGHT-GRID_CELL
                self.ge[i].fitness -= 5
                self.snakes.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)

            elif(snake.head.y > GAME_HEIGHT-GRID_CELL): #bottom boundary
                snake.head.y = 0
                self.ge[i].fitness -= 5
                self.snakes.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)
                
    def respawn_food(self):
        self.food.sprite = Food(self.food)

    def check_food(self):
        global_max = 0
        for i,snake_sprites in enumerate(self.snake_sprites_all):
            if(pygame.sprite.groupcollide(self.food,self.snake_sprites_all[i],False,False)):
                self.respawn_food()
                self.snakes[i].append_part(self.snake_sprites_all[i])
                self.ge[i].fitness += 100
            global_max = max(global_max,len(self.snakes[i].parts)-1)
        set_score(global_max)

    def check_self_collision(self):
        for i,snake in enumerate(self.snakes):
            for part in self.snakes[i].parts:
                if(part != self.snakes[i].head and pygame.sprite.collide_rect(part,self.snakes[i].head)):
                    self.ge[i].fitness -= 10
                    self.snakes.pop(i)
                    self.snake_sprites_all.pop(i)
                    self.neural_networks.pop(i)
                    self.ge.pop(i)
                    break

    def punishments(self):
        curr_time = pygame.time.get_ticks()
        for i,snake in enumerate(self.snakes): 
            if(snake.closer_to_food == 1):
                self.ge[i].fitness += 0.5
            else:
                self.ge[i].fitness -= 0.5    
            # displ = (snake.head.x-self.food.sprite.x)**2 + (snake.head.y-self.food.sprite.y)**2
            # if(displ>10000):
            #     self.ge[i].fitness -= 0.02
            # else:
            #     self.ge[i].fitness += 0.01

            # if (curr_time-self.start_time >= 20000):
            #     #print('ending')
            #     self.snakes.pop(i)
            #     self.snake_sprites_all.pop(i)
            #     self.neural_networks.pop(i)
            #     self.ge.pop(i)
            # else:
            for ls in snake.visited:
                for el in ls:
                    if (el > 25):
                        self.ge[i].fitness -= 50                     
                        self.snakes.pop(i)
                        self.snake_sprites_all.pop(i)
                        self.neural_networks.pop(i)
                        self.ge.pop(i)

            

    # def reset(self):
    #     set_score(0)
    #     self.respawn_food()
    #     self.snake_sprites.empty()
    #     self.snake = Snake(self.snake_sprites)
    #     self.timers = {"MOVE" : Timer(SNAKE_TIME,self.snake.move),
    #                    "INPUT" : Timer(INPUT_TIME,self.input)}

    def run(self):

        set_population(len(self.snakes))

        for timers in self.timers_all:
            timers["MOVE"].runTimer(x=self.food.sprite.x,y=self.food.sprite.y)
            timers["INPUT"].runTimer()

        self.punishments()
        self.check_boundary()
        self.check_food()
        self.check_self_collision()
        
        self.screen.blit(self.game_screen, self.game_rect)
        self.game_screen.fill(GAME_COLOR) #VERY IMPORTANT : TO FILL OVER (CLEAR) CONTENTS OF PREVIOUS FRAME
   
        for snake_sprites in self.snake_sprites_all:
            snake_sprites.update()
            snake_sprites.draw(self.game_screen)

        self.food.draw(self.game_screen)