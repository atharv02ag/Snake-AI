from settings import *

FONT_RATIO = 35/680

#Panel to display score, game number, and maximum score achieved so far
class Panel():

    def __init__(self):
        self.panel_surface = pygame.surface.Surface((PANEL_WIDTH,PANEL_HEIGHT))
        self.panel_rect = self.panel_surface.get_rect(topleft = (PADDING,PADDING))
        self.screen = pygame.display.get_surface()
        self.max_score = 0

    def display_score(self):
        score = get_score()
        font = pygame.font.SysFont("Ariel",int(GAME_WIDTH*FONT_RATIO))
        image = font.render(f"Score : {score}",True,FONT_COLOR)
        rect = image.get_rect(topleft = (PADDING,PADDING))
        self.panel_surface.blit(image,rect)
    
    def display_count(self,count):
        font = pygame.font.SysFont("Ariel",int(GAME_WIDTH*FONT_RATIO))
        image = font.render(f"Game Number : {count}",True,FONT_COLOR)
        rect = image.get_rect(topright=(GAME_WIDTH-2*PADDING,PADDING))
        self.panel_surface.blit(image,rect)

    def display_max_score(self):
        if(get_score() > self.max_score):
            self.max_score = get_score()

        font = pygame.font.SysFont("Ariel",int(GAME_WIDTH*FONT_RATIO))
        image = font.render(f"Max. Score : {self.max_score}",True,FONT_COLOR)
        rect = image.get_rect(topleft = (GAME_WIDTH/4,PADDING))
        self.panel_surface.blit(image,rect)

    def run(self,count):
        self.screen.blit(self.panel_surface,self.panel_rect)
        self.panel_surface.fill(PANEL_COLOR)
        self.display_score()
        self.display_count(count)
        self.display_max_score()
