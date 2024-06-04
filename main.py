from sys import exit

from settings import *
from game import Game
from panel import Panel

import os
import neat
import neat.config


def eval_genomes(genomes,config):
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    panel = Panel()
    game.init_neat(genomes,config)

    running = True

    while(running):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
                pygame.quit()
                exit()
            elif(get_population() == 0):
                running = False
                break
        
        screen.fill(BACKGROUND_COLOR)

        game.run()
        panel.run()

        pygame.display.update()
        clock.tick(FPS)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))

    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(eval_genomes,500)

if(__name__ == '__main__'):

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neat-config.txt")
    run(config_path)

