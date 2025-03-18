import pygame
import sys
import colors

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
gridColor = colors.purple

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marko Corner")

# Загрузка изображения фона
background = pygame.image.load("img/dreamW/bg.png")
# background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабирование под размер окна

# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заливка фона
    screen.fill((0, 0, 0))  # Черный цвет
    

    # Отображение изображения фона
    screen.blit(background, (0, 0))

    #Здесь будет отрисовка сетки
    # Отрисовка сетки
    for x in range(0, WIDTH, 48):
        pygame.draw.line(screen, gridColor, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 48):
        pygame.draw.line(screen, gridColor, (0, y), (WIDTH, y))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
sys.exit()