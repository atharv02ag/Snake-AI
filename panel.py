from settings import *

class Panel():

    def __init__(self):
        self.panel_surface = pygame.surface.Surface((PANEL_WIDTH,PANEL_HEIGHT))
        self.panel_rect = self.panel_surface.get_rect(topleft = (PADDING,PADDING))
        self.screen = pygame.display.get_surface()

    def display_score(self):
        score = get_score()
        font = pygame.font.SysFont("Ariel",35)
        image = font.render(f"Score : {score}",True,FONT_COLOR)
        self.panel_surface.blit(image,(PADDING,PADDING))

    def run(self):
        self.screen.blit(self.panel_surface,self.panel_rect)
        self.panel_surface.fill(PANEL_COLOR)
        self.display_score()
