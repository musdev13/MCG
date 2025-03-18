import pygame
import sys
from levelsController import LController as LC
from settings import *

# Инициализация Pygame
pygame.init()

# Размеры окна


# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marko Corner")


# background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабирование под размер окна

level = "intro"



# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    LC.loadLevel(levelName=level, screen=screen)

    # Отрисовка сетки
    if debugGrid:
        for x in range(0, WIDTH, 48):
            pygame.draw.line(screen, gridColor, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 48):
            pygame.draw.line(screen, gridColor, (0, y), (WIDTH, y))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
sys.exit()