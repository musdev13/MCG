import pygame
import sys
from levelsController import LController as LC
from settings import *

# Инициализация Pygame
pygame.init()
clock = pygame.time.Clock()

# Размеры окна


# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marko Corner")


# background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабирование под размер окна
Level.levelName = "dreamW"


# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    levelName = Level.levelName
    LC.loadLevel(levelName=levelName, screen=screen)

    # Отрисовка сетки
    

    
    # Обновление экрана
    # pygame.time.Clock().tick(30)
    pygame.display.flip()
    clock.tick(30)
    

# Завершение работы Pygame
pygame.quit()
sys.exit()