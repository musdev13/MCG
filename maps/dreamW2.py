# filepath: {gamePath}/maps/dreamW2.py
import pygame
import time
from settings import gamePath, Level
from debugGrid import debugGrid as dG
from Player import Player
from dialog import Dialog

class dreamW2:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.running = True
        self.grid_size = 48
        self.grid = []
        self.cutscene_active = False
        self.is_fading = False
        self.fade_screen = None

        self.bg_image = pygame.image.load(f"{gamePath}/img/dreamW/bg.png")

        # Create grid
        for y in range(12):
            row = []
            for x in range(16):
                row.append((x * self.grid_size, y * self.grid_size))
            self.grid.append(row)

        self.backgrounds = []
        # Load background layers
        self.backgrounds.append(pygame.image.load(f"{gamePath}/img/dreamW/bg_1.png"))
        self.backgrounds.append(pygame.image.load(f"{gamePath}/img/dreamW/bg.png"))

        # Initialize player one cell above spawn point
        start_position = 72
        spawn_y = start_position // 16 - 1  # Subtract 1 to move up one cell
        spawn_x = start_position % 16
        self.player = Player(
            self.grid[spawn_y][spawn_x][0],
            self.grid[spawn_y][spawn_x][1],
            0,
            "marko"
        )
        self.player_layer = 1

        # Add collision blocks
        self.collisionBlocks = []

        # Initialize dialogs


        # Run startup script


    def execute_script(self, script):
        # Split by newlines and semicolons
        commands = []
        for line in script.split("\n"):
            # Split line by semicolons and strip whitespace
            commands.extend([cmd.strip() for cmd in line.split(";") if cmd.strip()])
            
        for line in commands:
            line = line.strip()
            if line:
                if line.startswith("fadeIn("):
                    duration = float(line[7:-1])
                    start_time = time.time()
                    while True:
                        current_time = time.time() - start_time
                        if current_time >= duration:
                            break
                        fade_alpha = max(0, 255 * (1 - current_time / duration))
                        fade_surface = self.black_surface.copy()
                        fade_surface.set_alpha(int(fade_alpha))
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        self.screen.blit(fade_surface, (0, 0))
                        pygame.display.flip()
                        for event in pygame.event.get(): pass
                elif line.startswith("fadeOut("):
                    duration = float(line[8:-1])
                    start_time = time.time()
                    while True:
                        current_time = time.time() - start_time
                        if current_time >= duration:
                            break
                        fade_alpha = min(255, 255 * (current_time / duration))
                        fade_surface = self.black_surface.copy()
                        fade_surface.set_alpha(int(fade_alpha))
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        self.screen.blit(fade_surface, (0, 0))
                        pygame.display.flip()
                        for event in pygame.event.get(): pass
                elif line.startswith("wait("):
                    seconds = float(line[5:-1])
                    start_time = time.time()
                    while time.time() - start_time < seconds:
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        pygame.display.flip()
                        for event in pygame.event.get(): pass
                elif line.startswith("dialog("):
                    group = line[7:-1].strip('"\'"')
                    dialog = getattr(self, group)
                    dialog.start_dialog()
                    while dialog.is_active:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_z:
                                    dialog.next()
                        self.screen.blit(self.bg_image, (0, 0))
                        self.player.draw(self.screen)
                        if dialog.is_active:
                            dialog.draw()
                        pygame.display.flip()
                elif line == "playerCantMove()":
                    self.cutscene_active = True
                elif line == "playerCanMove()":
                    self.cutscene_active = False
                elif line.startswith("changeSprite("):
                    sprite_path = line[12:-1].strip()  # Remove changeSprite( and )
                    if sprite_path.startswith('"') or sprite_path.startswith("'"):
                        sprite_path = sprite_path[1:-1]  # Remove quotes
                    print(f"Changing sprite to path: {sprite_path}")
                    self.player.change_sprite(sprite_path)
                    # Redraw to show the change immediately
                    self.screen.blit(self.bg_image, (0, 0))
                    self.player.draw(self.screen)
                    pygame.display.flip()
                elif line == "resetSprite()":
                    skin_type = self.player.skin_type
                    sprite_path = f"{gamePath}/img/player/{'d/' if skin_type == 'd' else ''}idle_"
                    
                    # Reset all sprites to default
                    self.player.sprites = {
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
                    self.player.current_sprite = self.player.sprites[self.player.direction]
                    # Redraw to show the change immediately
                    self.screen.blit(self.bg_image, (0, 0))
                    self.player.draw(self.screen)
                    pygame.display.flip()

    def draw(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        player_grid_index = self.get_player_grid_index()




            self.screen.blit(self.bg_image, (0, 0))
            
            dG.draw(False, self.screen)
            
            self.player.is_moving = not (self.is_any_dialog_active() or self.cutscene_active)
            
            if not self.cutscene_active and not self.is_any_dialog_active():
                self.player.move(self)
            
            self.player.draw(self.screen)



            pygame.display.flip()
            #pygame.time.Clock().tick(60)

    def get_player_grid_index(self):
        player_feet_x = self.player.x + self.player.sprite_width // 2
        player_feet_y = self.player.y + self.player.sprite_height
        
        grid_x = player_feet_x // self.grid_size
        grid_y = player_feet_y // self.grid_size
        
        index = grid_y * 16 + grid_x
        return index if 0 <= grid_x < 16 and 0 <= grid_y < 12 else None

    def is_any_dialog_active(self):
        return any([
            False
        ])
