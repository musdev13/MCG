import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marko Corner")

# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заливка фона
    screen.fill((0, 0, 0))  # Черный цвет

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
sys.exit()