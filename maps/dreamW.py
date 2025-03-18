import pygame
from settings import gamePath

class DreamW:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.background = pygame.image.load(f"{gamePath}/img/dreamW/bg.png")

    def draw(self):
        self.screen.blit(self.background, (0, 0))