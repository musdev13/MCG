import pygame
from settings import gamePath, Level
from debugGrid import debugGrid as dG

class d1:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.running = True
        self.grid_size = 48
        self.grid = []
        for y in range(12):  # 600/48 = 12 rows
            for x in range(16):  # 800/48 = 16 columns
                self.grid.append((x * self.grid_size, y * self.grid_size))

    def draw(self):
        while self.running:
            self.screen.fill((255, 255, 255))  # Fill with white color


            dG.draw(True, self.screen)

            if Level.levelName == "d1":
                pygame.display.flip()  # Update the display
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                