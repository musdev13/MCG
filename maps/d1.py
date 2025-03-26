import pygame
from settings import gamePath, Level

class d1:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.running = True

    def draw(self):
        while self.running:
            self.screen.fill((255, 255, 255))  # Fill with white color

            if Level.levelName == "d1":
                pygame.display.flip()  # Update the display
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()