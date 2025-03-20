import pygame
from settings import playerSpeed
class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = playerSpeed
        self.angle = angle #0 - вверх, 1 - вправо, 2 - вниз, 3 - влево

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = playerSpeed
        self.angle = angle
        self.canMove = True
        self.targetX = x
        self.targetY = y
        self.movingTimer = 0
        self.gridSize = 48

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = playerSpeed
        self.angle = angle
        self.canMove = True
        self.targetX = x
        self.targetY = y
        self.movingTimer = 0
        self.gridSize = 48
        # Load player sprites
        self.sprites = {
            'up': pygame.image.load("gamePath/img/player/idle_u.png"),
            'down': pygame.image.load("gamePath/img/player/idle_d.png"),
            'left': pygame.image.load("gamePath/img/player/idle_l.png"),
            'right': pygame.image.load("gamePath/img/player/idle_r.png")
        }
        self.current_sprite = self.sprites['down']  # Default facing down

    def move(self):
        if not self.canMove:
            # Continue animation
            dx = self.targetX - self.x
            dy = self.targetY - self.y
            
            if dx > 0:
                self.x += min(self.speed, dx)
            elif dx < 0:
                self.x -= min(self.speed, -dx)
            
            if dy > 0:
                self.y += min(self.speed, dy)
            elif dy < 0:
                self.y -= min(self.speed, -dy)
            
            # Check if reached target
            if self.x == self.targetX and self.y == self.targetY:
                self.canMove = True
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.targetX = self.x - self.gridSize
            self.canMove = False
            self.current_sprite = self.sprites['left']
        elif keys[pygame.K_RIGHT]:
            self.targetX = self.x + self.gridSize
            self.canMove = False
            self.current_sprite = self.sprites['right']
        elif keys[pygame.K_UP]:
            self.targetY = self.y - self.gridSize
            self.canMove = False
            self.current_sprite = self.sprites['up']
        elif keys[pygame.K_DOWN]:
            self.targetY = self.y + self.gridSize
            self.canMove = False
            self.current_sprite = self.sprites['down']

        if keys[pygame.K_p]:
            print(f"Player coordinates: x={self.x}, y={self.y}")
    
    def draw(self, screen):
        screen.blit(self.current_sprite, (self.x, self.y))
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 48, 48))
    
