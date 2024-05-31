from settings import *
from food import Food

class Game():

    def __init__(self):
        self.game_screen = pygame.surface.Surface((GAME_WIDTH,GAME_HEIGHT))
        self.game_rect = self.game_screen.get_rect(bottomleft=(PADDING,(SCREEN_HEIGHT-PADDING)))
        self.screen = pygame.display.get_surface()
        self.food = pygame.sprite.GroupSingle()

        food = Food(self.food)
    
    def respawn_food(self):
        if (self.food.sprite.eaten):
            self.food.sprite = Food()

    def run(self):
        self.screen.blit(self.game_screen, self.game_rect)
        self.game_screen.fill(GAME_COLOR)

        self.respawn_food()
        
        self.food.draw(self.game_screen)

