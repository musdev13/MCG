from pdb import run
import pygame
from settings import gamePath

class dCat:
    def __init__(self, screen, gamePath = gamePath):
        self.screen = screen
        
    
    def draw(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return