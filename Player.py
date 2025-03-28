import pygame
from settings import playerSpeed, gamePath

class Player:
    def __init__(self, x, y, angle, skin_type="marko"):
        self.x = x
        self.y = y
        self.speed = playerSpeed
        self.angle = angle
        self.skin_type = skin_type  # Add skin type parameter
        self.canMove = True
        self.targetX = x
        self.targetY = y
        self.movingTimer = 0
        self.gridSize = 48
        self.animation_timer = 0
        self.animation_frame = 0
        self.is_moving = False
        
        # Load player sprites based on skin type
        sprite_path = f"{gamePath}/img/player/{'d/' if skin_type == 'd' else ''}idle_"
        self.sprites = {
            'up': pygame.transform.scale(pygame.image.load(f"{sprite_path}u.png"), (96, 96)),
            'up1': pygame.transform.scale(pygame.image.load(f"{sprite_path}u1.png"), (96, 96)),
            'up2': pygame.transform.scale(pygame.image.load(f"{sprite_path}u2.png"), (96, 96)),
            'down': pygame.transform.scale(pygame.image.load(f"{sprite_path}d.png"), (96, 96)),
            'down1': pygame.transform.scale(pygame.image.load(f"{sprite_path}d1.png"), (96, 96)),
            'down2': pygame.transform.scale(pygame.image.load(f"{sprite_path}d2.png"), (96, 96)),
            'left': pygame.transform.scale(pygame.image.load(f"{sprite_path}l.png"), (96, 96)),
            'left1': pygame.transform.scale(pygame.image.load(f"{sprite_path}l1.png"), (96, 96)),
            'left2': pygame.transform.scale(pygame.image.load(f"{sprite_path}l2.png"), (96, 96)),
            'right': pygame.transform.scale(pygame.image.load(f"{sprite_path}r.png"), (96, 96)),
            'right1': pygame.transform.scale(pygame.image.load(f"{sprite_path}r1.png"), (96, 96)),
            'right2': pygame.transform.scale(pygame.image.load(f"{sprite_path}r2.png"), (96, 96))
        }
        self.current_sprite = self.sprites['down']
        self.direction = 'down'
        
        # Add screen boundaries
        self.screen_width = 800  # Total width (16 * 48)
        self.screen_height = 576  # Total height (12 * 48)
        self.sprite_width = 96   # Width of player sprite
        self.sprite_height = 96  # Height of player sprite

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

    def move(self, level=None):
        # First check if we have a valid level and can move
        if not level or not self.is_moving:
            print(f"Movement blocked: level={bool(level)}, is_moving={self.is_moving}")
            return
        
        keys = pygame.key.get_pressed()
        
        # Store potential new position
        new_x = self.x
        new_y = self.y

        # Check for any active dialogs or cutscenes
        dialog_active = False
        if hasattr(level, 'dialog'):
            dialog_active = getattr(level.dialog, 'active', False)
        if hasattr(level, 'dialog1'):
            dialog_active = dialog_active or getattr(level.dialog1, 'active', False)
        if hasattr(level, 'paperDialog'):
            dialog_active = dialog_active or getattr(level.paperDialog, 'active', False)
        
        # Block movement if dialog or cutscene is active
        if level.cutscene_active or dialog_active:
            print(f"Movement blocked: cutscene={level.cutscene_active}, dialog={dialog_active}")
            self.is_moving = False
            return

        self.is_moving = False  # Reset movement state
        
        if keys[pygame.K_LEFT]:
            print("Left key pressed")
            new_x = self.x - self.speed
            self.direction = 'left'
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            print("Right key pressed")
            new_x = self.x + self.speed
            self.direction = 'right'
            self.is_moving = True
        if keys[pygame.K_UP]:
            print("Up key pressed")
            new_y = self.y - self.speed
            self.direction = 'up'
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            print("Down key pressed")
            new_y = self.y + self.speed
            self.direction = 'down'
            self.is_moving = True

        # If we're moving and there's no collision, update position
        if self.is_moving and (not level or not self.check_collision(level, new_x, new_y)):
            self.x = new_x
            self.y = new_y

            # Check boundaries
            if self.x < 0:
                self.x = 0
            elif self.x > self.screen_width - self.sprite_width:
                self.x = self.screen_width - self.sprite_width
            if self.y < -self.gridSize:
                self.y = -self.gridSize
            elif self.y > self.screen_height - self.sprite_height:
                self.y = self.screen_height - self.sprite_height

        self.update_animation()

    def check_collision(self, level, next_x, next_y):
        """Check collision for multiple points along player's width"""
        # Height of collision box (8 pixels up from feet)
        collision_height = 8
        
        # Check points along bottom of player (full width)
        feet_y = next_y + self.sprite_height
        
        # Check multiple x positions (wider coverage)
        check_points = [
            # Bottom points
            (next_x + 24, feet_y),              # Far Left
            (next_x + 40, feet_y),              # Left
            (next_x + self.sprite_width//2, feet_y),  # Center
            (next_x + 56, feet_y),              # Right
            (next_x + 72, feet_y),              # Far Right
            
            # Points 8 pixels above feet
            (next_x + 24, feet_y - collision_height),
            (next_x + 40, feet_y - collision_height),
            (next_x + self.sprite_width//2, feet_y - collision_height),
            (next_x + 56, feet_y - collision_height),
            (next_x + 72, feet_y - collision_height),
            
            # Additional middle height points (4 pixels up)
            (next_x + 24, feet_y - collision_height//2),
            (next_x + 40, feet_y - collision_height//2),
            (next_x + self.sprite_width//2, feet_y - collision_height//2),
            (next_x + 56, feet_y - collision_height//2),
            (next_x + 72, feet_y - collision_height//2),
        ]
        
        for x, y in check_points:
            grid_x = x // level.grid_size
            grid_y = y // level.grid_size
            
            if 0 <= grid_x < 16 and 0 <= grid_y < 12:
                index = grid_y * 16 + grid_x
                if index in level.collisionBlocks:
                    return True
                    
        return False
    
    def draw(self, screen):
        screen.blit(self.current_sprite, (self.x, self.y))

    def change_skin(self, new_skin_type):
        """Change player skin and reload sprites"""
        self.skin_type = new_skin_type
        sprite_path = f"{gamePath}/img/player/{'d/' if new_skin_type == 'd' else ''}idle_"
        
        # Reload all sprites with new skin
        self.sprites = {
            'up': pygame.transform.scale(pygame.image.load(f"{sprite_path}u.png"), (96, 96)),
            'up1': pygame.transform.scale(pygame.image.load(f"{sprite_path}u1.png"), (96, 96)),
            'up2': pygame.transform.scale(pygame.image.load(f"{sprite_path}u2.png"), (96, 96)),
            'down': pygame.transform.scale(pygame.image.load(f"{sprite_path}d.png"), (96, 96)),
            'down1': pygame.transform.scale(pygame.image.load(f"{sprite_path}d1.png"), (96, 96)),
            'down2': pygame.transform.scale(pygame.image.load(f"{sprite_path}d2.png"), (96, 96)),
            'left': pygame.transform.scale(pygame.image.load(f"{sprite_path}l.png"), (96, 96)),
            'left1': pygame.transform.scale(pygame.image.load(f"{sprite_path}l1.png"), (96, 96)),
            'left2': pygame.transform.scale(pygame.image.load(f"{sprite_path}l2.png"), (96, 96)),
            'right': pygame.transform.scale(pygame.image.load(f"{sprite_path}r.png"), (96, 96)),
            'right1': pygame.transform.scale(pygame.image.load(f"{sprite_path}r1.png"), (96, 96)),
            'right2': pygame.transform.scale(pygame.image.load(f"{sprite_path}r2.png"), (96, 96))
        }
        self.current_sprite = self.sprites[self.direction]

    def change_sprite(self, sprite_path):
        """Change player sprite to a specific image path"""
        try:
            sprite_path = sprite_path[:-1]
            base_path = f"{gamePath}/img/{sprite_path}"
            print(f"Loading sprite from: {base_path}")
            
            # Load and scale the sprite
            new_sprite = pygame.transform.scale(
                pygame.image.load(f"{base_path}.png"), 
                (96, 96)
            )
            
            # Update both current sprite and the default sprite for current direction
            self.current_sprite = new_sprite
            self.sprites[self.direction] = new_sprite
            
            print("Sprite changed successfully")
            
        except Exception as e:
            print(f"Error changing sprite: {e}")
