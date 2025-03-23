import pygame
from settings import playerSpeed, gamePath

class Player:
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
        self.animation_timer = 0
        self.animation_frame = 0
        self.is_moving = False
        
        # Load player sprites
        self.sprites = {
            'up': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_u.png"), (96, 96)),
            'up1': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_u1.png"), (96, 96)),
            'up2': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_u2.png"), (96, 96)),
            'down': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_d.png"), (96, 96)),
            'down1': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_d1.png"), (96, 96)),
            'down2': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_d2.png"), (96, 96)),
            'left': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_l.png"), (96, 96)),
            'left1': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_l1.png"), (96, 96)),
            'left2': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_l2.png"), (96, 96)),
            'right': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_r.png"), (96, 96)),
            'right1': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_r1.png"), (96, 96)),
            'right2': pygame.transform.scale(pygame.image.load(f"{gamePath}/img/player/idle_r2.png"), (96, 96))
        }
        self.current_sprite = self.sprites['down']
        self.direction = 'down'

    def update_animation(self):
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > 150:  # Update every 150ms
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % 4
                
            if self.animation_frame == 0:
                self.current_sprite = self.sprites[f'{self.direction}1']
            elif self.animation_frame == 1:
                self.current_sprite = self.sprites[self.direction]
            elif self.animation_frame == 2:
                self.current_sprite = self.sprites[f'{self.direction}2']
            elif self.animation_frame == 3:
                self.current_sprite = self.sprites[self.direction]
        else:
            self.current_sprite = self.sprites[self.direction]
            self.animation_timer = pygame.time.get_ticks()
            self.animation_frame = 0

    def move(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = 'left'
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = 'right'
            self.is_moving = True
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = 'up'
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = 'down'
            self.is_moving = True

        if keys[pygame.K_p]:
            print(f"Player coordinates: x={self.x}, y={self.y}")
            
        self.update_animation()
    
    def draw(self, screen):
        screen.blit(self.current_sprite, (self.x, self.y))
