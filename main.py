from sys import exit
from settings import *
from game import Game
from panel import Panel
pygame.mixer.init()

class Main():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.panel = Panel()

    def run(self):
        running = True
        while(running):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    running = False
                    pygame.quit()
                    exit()
            
            self.screen.fill(BACKGROUND_COLOR)

            self.game.run()
            self.panel.run()
            self.game.snake_body_dir()

            pygame.display.update()
            self.clock.tick(FPS)

if(__name__ == '__main__'):
    main = Main()
    main.run()
