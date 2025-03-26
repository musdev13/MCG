import pygame
from settings import gamePath, Level
from debugGrid import debugGrid as dG
from Player import Player

class d1:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.running = True
        self.grid_size = 48
        self.grid = []
        self.cutscene_active = False
        self.dialog = None  # Add dialog property

        # Create grid properly
        for y in range(12):
            row = []
            for x in range(16):
                row.append((x * self.grid_size, y * self.grid_size))
            self.grid.append(row)

        # Initialize player at grid position
        start_position = 87  # Example grid position (can be changed)
        self.player = Player(
            self.grid[start_position // 16][start_position % 16][0],
            self.grid[start_position // 16][start_position % 16][1],
            0,
            "d"
        )

        # Add collision blocks
        self.collisionBlocks = []  # Add indices of blocked grid cells here

    def check_collision(self, next_x, next_y):
        # Calculate feet position
        feet_x = next_x + self.player.sprite_width // 2
        feet_y = next_y + self.player.sprite_height
        
        # Convert to grid position
        grid_x = feet_x // self.grid_size
        grid_y = feet_y // self.grid_size
        
        # Check if feet position is within grid bounds
        if 0 <= grid_x < 16 and 0 <= grid_y < 12:
            index = grid_y * 16 + grid_x
            if index in self.collisionBlocks:
                return True
                
        return False

    def is_any_dialog_active(self):
        return (hasattr(self, 'dialog') and 
                self.dialog is not None and 
                getattr(self.dialog, 'is_active', False))

    def draw(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            
            # Draw debug grid
            dG.draw(True, self.screen)
            
            # Set player movement based on dialog state AND cutscene state
            self.player.is_moving = not (self.is_any_dialog_active() or self.cutscene_active)
            
            # Only move player if not in cutscene or dialog
            if not self.cutscene_active and not self.is_any_dialog_active():
                print("Movement state:", self.player.is_moving)
                self.player.move(self)
            
            self.player.draw(self.screen)

            # Draw active dialog if exists
            if self.dialog and self.dialog.is_active:
                self.dialog.draw()

            if Level.levelName == "d1":
                pygame.display.flip()
                pygame.time.Clock().tick(120)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
