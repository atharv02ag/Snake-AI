from settings import *
from food import Food
from snake import Snake
from timer import Timer

import neat
import neat.config

class Game():

    def __init__(self):
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

    def init_neat(self,genomes,config):
        for x,g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g,config)
            self.neural_networks.append(net)

            snake_sprites = pygame.sprite.Group()
            self.snake_sprites_all.append(snake_sprites)

            snake = Snake(snake_sprites)  
            self.snakes.append(snake)

            timers = {"MOVE" : Timer(SNAKE_TIME,snake.move),
                            "INPUT" : Timer(INPUT_TIME,self.input)}
            self.timers_all.append(timers)

            g.fitness = 0
            self.ge.append(g)

    
    def input(self):
        
        for i,snake in enumerate(self.snakes):
            output = self.neural_networks[i].activate((self.snakes[i].head.x, self.snakes[i].head.y, self.food.sprite.x, self.food.sprite.y))

            if(output[0]>0.5):
                self.snakes[i].v_x = 0
                self.snakes[i].v_y = (-1)*GRID_CELL
                self.snakes[i].head.dir = (0,-1)
                self.ge[i].fitness += 0.1
            elif(output[1]>0.5):
                self.snakes[i].v_x = 0
                self.snakes[i].v_y = 1*GRID_CELL
                self.snakes[i].head.dir = (0,1)
                self.ge[i].fitness += 0.1
            elif(output[2]>0.5):
                self.snakes[i].v_x = 1*GRID_CELL
                self.snakes[i].v_y = 0
                self.snakes[i].head.dir = (1,0)
                self.ge[i].fitness += 0.1
            elif(output[3]>0.5):
                self.snakes[i].v_x = (-1)*GRID_CELL
                self.snakes[i].v_y = 0
                self.snakes[i].head.dir = (-1,0)
                self.ge[i].fitness += 0.1

    def check_boundary(self):
        for snake in self.snakes:
            if(snake.head.x < 0): #left boundary 
                snake.head.x = GAME_WIDTH-GRID_CELL

            elif(snake.head.x > GAME_WIDTH): #right boundary
                snake.head.x = 0
            
            elif(snake.head.y < 0): #top boundary
                snake.head.y = GAME_HEIGHT-GRID_CELL
            
            elif(snake.head.y > GAME_HEIGHT): #bottom boundary
                snake.head.y = 0

    def respawn_food(self):
        self.food.sprite = Food(self.food)

    def check_food(self):
        for i,snake_sprites in enumerate(self.snake_sprites_all):

            if(pygame.sprite.groupcollide(self.food,self.snake_sprites_all[i],False,False)):
                self.respawn_food()
                self.snakes[i].append_part(self.snake_sprites_all[i])
                self.ge[i].fitness += 10
                #set_score(len(self.snakes[i].parts)-1)

    def check_self_collision(self):
        for i,snake in enumerate(self.snakes):
            for part in self.snakes[i].parts:
                if(part != self.snakes[i].head and pygame.sprite.collide_rect(part,self.snakes[i].head)):
                    self.ge[i].fitness -= 2
                    self.snakes.pop(i)
                    self.neural_networks.pop(i)
                    self.ge.pop(i)
                    break

    # def reset(self):
    #     set_score(0)
    #     self.respawn_food()
    #     self.snake_sprites.empty()
    #     self.snake = Snake(self.snake_sprites)
    #     self.timers = {"MOVE" : Timer(SNAKE_TIME,self.snake.move),
    #                    "INPUT" : Timer(INPUT_TIME,self.input)}

    def run(self):

        for timers in self.timers_all:
            timers["MOVE"].runTimer()
            timers["INPUT"].runTimer()

        self.check_boundary()
        self.check_food()
        self.check_self_collision()
        
        self.screen.blit(self.game_screen, self.game_rect)
        self.game_screen.fill(GAME_COLOR) #VERY IMPORTANT : TO FILL OVER (CLEAR) CONTENTS OF PREVIOUS FRAME
   
        for snake_sprites in self.snake_sprites_all:
            snake_sprites.update()
            snake_sprites.draw(self.game_screen)

        self.food.draw(self.game_screen)