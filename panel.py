
from settings import *

FONT_RATIO = 35/680

#top panel used to display score (of best performer currently alive in the a generation)
class Panel():

    def __init__(self):
        self.panel_surface = pygame.surface.Surface((PANEL_WIDTH,PANEL_HEIGHT))
        self.panel_rect = self.panel_surface.get_rect(topleft = (PADDING,PADDING))
        self.screen = pygame.display.get_surface()

    def display_score(self):
        score = get_score()
        font = pygame.font.SysFont("Ariel",int(GAME_WIDTH*FONT_RATIO))
        image = font.render(f"Score : {score}",True,FONT_COLOR)
        rect = image.get_rect(topleft = (PADDING,PADDING))
        self.panel_surface.blit(image,rect)
    
    def display_count(self,count):
        font = pygame.font.SysFont("Ariel",int(GAME_WIDTH*FONT_RATIO))
        image = font.render(f"Generation : {count}",True,FONT_COLOR)
        rect = image.get_rect(topright=(GAME_WIDTH-2*PADDING,PADDING))
        self.panel_surface.blit(image,rect)

    def display_max_score(self):
        if(get_score() > get_max_score()):
            set_max_score(get_score())

        font = pygame.font.SysFont("Ariel",int(GAME_WIDTH*FONT_RATIO))
        image = font.render(f"Max. Score : {get_max_score()}",True,FONT_COLOR)
        rect = image.get_rect(topleft = (GAME_WIDTH/4,PADDING))
        self.panel_surface.blit(image,rect)

    def run(self,count):
        self.screen.blit(self.panel_surface,self.panel_rect)
        self.panel_surface.fill(PANEL_COLOR)
        self.display_score()
        self.display_count(count)
        self.display_max_score()