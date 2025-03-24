import pygame
from settings import WIDTH, HEIGHT, gridColor

class debugGrid:
    def draw(toggle, screen):
        if toggle:
            for x in range(0, WIDTH, 48):
                pygame.draw.line(screen, gridColor, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, 48):
                pygame.draw.line(screen, gridColor, (0, y), (WIDTH, y))
        return