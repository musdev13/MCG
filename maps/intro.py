import pygame
from settings import gamePath
# from main import level
from levelsController import LController as LC

class intro:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen

    def draw(self):
        self.screen.fill((0, 0, 0))
        #здесь код сцены
        LC.loadLevel(levelName="dreamW", screen=self.screen)
        return