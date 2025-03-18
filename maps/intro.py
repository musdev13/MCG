import pygame
from settings import gamePath

class intro:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen

    def draw(self):
        self.screen.fill((0, 0, 0))
        