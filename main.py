from sys import exit

from settings import *
from game import Game
from panel import Panel

import os
import neat
import neat.config


class Main():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.panel = Panel()

    def eval_genomes(self,genomes,config):
        running = True
        self.game.init_neat(genomes,config)
        while(running):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    running = False
                    pygame.quit()
                    exit()
            
            self.screen.fill(BACKGROUND_COLOR)

            self.game.run()
            self.panel.run()

            pygame.display.update()
            self.clock.tick(FPS)
    
    def run(self,config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
        pop = neat.Population(config)
        pop.add_reporter(neat.StdOutReporter(True))

        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)

        winner = pop.run(self.eval_genomes,50)

if(__name__ == '__main__'):

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neat-config.txt")

    main = Main()
    main.run(config_path)

