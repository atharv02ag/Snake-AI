from settings import *
from food import Food
from snake import Snake
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

        #On the same game surface, we spawn several snakes and their corresponding target food
        self.foods = []
        self.snakes = []
        self.snake_sprites_all = []
        self.neural_networks = []
        self.ge = []
        self.start_time = pygame.time.get_ticks()

    #NEAT initialization
    #reads config file. 'Genomes' refers to a list of all the snake's genomes. 
    #genome encapsulates the snake's brain (neural network) and fitness
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

            food_sprite = pygame.sprite.GroupSingle()
            food = Food(food_sprite)
            self.foods.append(food_sprite)

            g.fitness = 0
            self.ge.append(g)

    
    def input(self,x=0,y=0):
        
        for i,snake in enumerate(self.snakes):

            #inputs - distances of snake head to each boundary
            dist_r = (GAME_WIDTH-snake.head.x)/GRID_CELL
            dist_l = snake.head.x/GRID_CELL
            dist_u = snake.head.y/GRID_CELL
            dist_b = (GAME_HEIGHT-snake.head.y)/GRID_CELL

            #inputs - length and angle of snake-head-to-food vector
            snake_to_food_vec = pygame.Vector2((self.foods[i].sprite.x-self.snakes[i].head.x),(self.foods[i].sprite.y-self.snakes[i].head.y))
            food_distance = snake_to_food_vec.length()
            food_angle = snake_to_food_vec.as_polar()[1]

            directions = [(0,-1),(0,1),(1,0),(-1,0)]
            opp_directions = {(0,-1) : (0,1), (0,1) : (0,-1),(1,0) : (-1,0),(-1,0) : (1,0)}

            prev_direction = self.snakes[i].head.dir

            #outputs - 4 possible values corresponding to each direction. Only the direction corresponding to maximum is considered
            output = self.neural_networks[i].activate((food_distance,food_angle,dist_r,dist_l,dist_u,dist_b))
            direction = directions[output.index(max(output))]

            #If current direction is opposite to previous direction, the snake's fitness is decreased
            if(opp_directions[prev_direction]==direction):
                self.ge[i].fitness -= 1
            
            #update snake's velocity and direction
            (self.snakes[i].v_x, self.snakes[i].v_y) = (direction[0]*GRID_CELL,direction[1]*GRID_CELL)
            self.snakes[i].head.dir = direction    

    #to check if the snake crosses the boundary. If so, then killed and fitness decreased
    def check_boundary(self):
        for i,snake in enumerate(self.snakes):
            if(snake.head.x < 0): #left boundary 
                snake.head.x = GAME_WIDTH-GRID_CELL
                self.ge[i].fitness -= 10
                self.snakes.pop(i)
                self.foods.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)

            elif(snake.head.x > GAME_WIDTH-GRID_CELL): #right boundary
                snake.head.x = 0
                self.ge[i].fitness -= 10
                self.snakes.pop(i)
                self.foods.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)

            elif(snake.head.y < 0): #top boundary
                snake.head.y = GAME_HEIGHT-GRID_CELL
                self.ge[i].fitness -= 10
                self.snakes.pop(i)
                self.foods.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)

            elif(snake.head.y > GAME_HEIGHT-GRID_CELL): #bottom boundary
                snake.head.y = 0
                self.ge[i].fitness -= 10
                self.snakes.pop(i)
                self.foods.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)
            
    def respawn_food(self,i):
        self.foods[i].sprite = Food(self.foods[i])

    #to check if the snake eats food. If so, then length increased, fitness increased, and food respawned
    def check_food(self):
        global_max = 0
        for i,snake_sprites in enumerate(self.snake_sprites_all):
            if(pygame.sprite.groupcollide(self.foods[i],self.snake_sprites_all[i],False,False)):
                self.respawn_food(i)
                self.snakes[i].append_part(self.snake_sprites_all[i])
                self.ge[i].fitness += 100
                self.start_time = pygame.time.get_ticks()
            global_max = max(global_max,len(self.snakes[i].parts)-1)
        set_score(global_max)

    #to check if the snake collides with itself. If so, then killed and fitness decreased 
    def check_self_collision(self):
        for i,snake in enumerate(self.snakes):
            for part in self.snakes[i].parts:
                if(part != self.snakes[i].head and pygame.sprite.collide_rect(part,self.snakes[i].head)):
                    self.ge[i].fitness -= 10
                    self.snakes.pop(i)
                    self.snake_sprites_all.pop(i)
                    self.foods.pop(i)
                    self.neural_networks.pop(i)
                    self.ge.pop(i)
                    break
                
    #fitness criterions
    def punishments(self):
        curr_time = pygame.time.get_ticks()
        for i,snake in enumerate(self.snakes): 

            #if the move taken by snake results in it getting closer to the food, fitness increased, and vice versa
            if(snake.closer_to_food == 1):
                self.ge[i].fitness += 0.5
            else:
                self.ge[i].fitness -= 0.5    

            #time based punishment. If the snake is alive for more than some threshold duration (proportional to snake's length)
            #without eating food, then killed and fitness decreased. Each time snake eats food, timer is reset.
            if(curr_time-self.start_time > 2000*len(snake.parts)):
                self.ge[i].fitness -= 10                     
                self.snakes.pop(i)
                self.foods.pop(i)
                self.snake_sprites_all.pop(i)
                self.neural_networks.pop(i)
                self.ge.pop(i)

    def run(self):

        #to keep of track of population on board
        set_population(len(self.snakes))

        #performing move based on output received by the snake's neural network
        self.input()
        for i,snake in enumerate(self.snakes):
            snake.move(x=self.foods[i].sprite.x,y=self.foods[i].sprite.y)
        
        #performing all checks
        self.punishments()
        self.check_boundary()
        self.check_self_collision()
        self.check_food()
        
        #ui updates
        self.screen.blit(self.game_screen, self.game_rect)
        self.game_screen.fill(GAME_COLOR) #VERY IMPORTANT : TO FILL OVER (CLEAR) CONTENTS OF PREVIOUS FRAME
   
        for snake_sprites in self.snake_sprites_all:
            snake_sprites.update()
            snake_sprites.draw(self.game_screen)

        for food_sprite in self.foods:
            food_sprite.draw(self.game_screen)