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

        self.timers = {"MOVE" : Timer(SNAKE_TIME,self.snake.move)}

    def run(self):

        self.timers["MOVE"].runTimer()
        
        self.screen.blit(self.game_screen, self.game_rect)
        self.game_screen.fill(GAME_COLOR) #VERY IMPORTANT : TO FILL OVER (CLEAR) CONTENTS OF PREVIOUS FRAME
   
        self.snake_sprites.update()

        self.snake_sprites.draw(self.game_screen)
        self.food.draw(self.game_screen)
        



