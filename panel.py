from settings import *

class Panel():

    def __init__(self):
        self.panel_surface = pygame.surface.Surface((PANEL_WIDTH,PANEL_HEIGHT))
        self.panel_rect = self.panel_surface.get_rect(topleft = (PADDING,PADDING))
        self.screen = pygame.display.get_surface()

    def run(self):
        self.screen.blit(self.panel_surface,self.panel_rect)
        self.panel_surface.fill(PANEL_COLOR)