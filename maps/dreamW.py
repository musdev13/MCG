import pygame
from settings import gamePath
from Player import Player
from debugGrid import debugGrid as dG

class DreamW:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.background = pygame.image.load(f"{gamePath}/img/dreamW/bg.png")
        self.grid_size = 48
        self.grid = []
        for y in range(12):  # 600/48 = 12 rows
            for x in range(16):  # 800/48 = 16 columns
                self.grid.append((x * self.grid_size, y * self.grid_size))
        self.map = None
        self.player = Player(self.grid[5][0], self.grid[80][1], 2)  # Place player at first grid position

    def draw(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            self.player.move()
            self.player.draw(self.screen)

            dG.draw(True, self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
        