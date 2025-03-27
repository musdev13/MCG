# filepath: {gamePath}/maps/d1.py
import pygame
from settings import gamePath, Level
from debugGrid import debugGrid as dG
from Player import Player
from dialog import Dialog

class d1:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.running = True
        self.grid_size = 48
        self.grid = []
        self.cutscene_active = False

        self.bg_image = pygame.image.load(f"{gamePath}/img/d1/bg.png")

        # Create grid
        for y in range(12):
            row = []
            for x in range(16):
                row.append((x * self.grid_size, y * self.grid_size))
            self.grid.append(row)

        # Initialize player
        start_position = 58
        self.player = Player(
            self.grid[start_position // 16][start_position % 16][0],
            self.grid[start_position // 16][start_position % 16][1],
            0,
            "d"
        )

        # Add collision blocks
        self.collisionBlocks = [22, 25, 18, 50, 34, 66, 82, 114, 98, 130, 146, 162, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 46, 27, 28, 44, 45, 26, 62, 78, 110, 94, 126, 142, 158, 174, 38, 39, 41, 40, 21, 20, 19]

        # Initialize dialogs
        self.firstpaper = Dialog(screen, [['First Dialog', 'D', 'None', 'False', 'True'], ['Nothing new', 'D', 'None', 'False', 'True']], self.player)
        self.second_papers = Dialog(screen, [['Second dialogs', 'D', 'None', 'False', 'True']], self.player)

    def check_collision(self, next_x, next_y):
        feet_x = next_x + self.player.sprite_width // 2
        feet_y = next_y + self.player.sprite_height
        
        grid_x = feet_x // self.grid_size
        grid_y = feet_y // self.grid_size
        
        if 0 <= grid_x < 16 and 0 <= grid_y < 12:
            index = grid_y * 16 + grid_x
            if index in self.collisionBlocks:
                return True
        return False

    def is_any_dialog_active(self):
        return any([
            hasattr(self, "firstpaper") and self.firstpaper.is_active or
            hasattr(self, "second_papers") and self.second_papers.is_active
        ])

    def get_player_grid_index(self):
        player_feet_x = self.player.x + self.player.sprite_width // 2
        player_feet_y = self.player.y + self.player.sprite_height
        
        grid_x = player_feet_x // self.grid_size
        grid_y = player_feet_y // self.grid_size
        
        index = grid_y * 16 + grid_x
        return index if 0 <= grid_x < 16 and 0 <= grid_y < 12 else None

    def draw(self):
        while self.running:
            self.screen.blit(self.bg_image, (0, 0))
            
            dG.draw(False, self.screen)
            
            self.player.is_moving = not (self.is_any_dialog_active() or self.cutscene_active)
            
            if not self.cutscene_active and not self.is_any_dialog_active():
                self.player.move(self)
            
            self.player.draw(self.screen)

            if self.firstpaper.is_active:
                self.firstpaper.draw()
            if self.second_papers.is_active:
                self.second_papers.draw()

            if Level.levelName == "d1":
                pygame.display.flip()
                #pygame.time.Clock().tick(120)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        player_grid_index = self.get_player_grid_index()
                        if player_grid_index in [38, 38, 39, 38, 39, 55, 38, 38, 38, 54] and not self.firstpaper.is_active:
                            self.firstpaper.start_dialog()
                        if player_grid_index in [56, 57] and not self.second_papers.is_active:
                            self.second_papers.start_dialog()
                        elif self.firstpaper.is_active:
                            # Check if this is the last dialog
                            if self.firstpaper.current_dialog_index == len(self.firstpaper.dialogs) - 1:
                                self.firstpaper.next()
                                self.firstpaper.current_dialog_index = 0  # Reset index
                            else:
                                self.firstpaper.next()
                        elif self.second_papers.is_active:
                            # Check if this is the last dialog
                            if self.second_papers.current_dialog_index == len(self.second_papers.dialogs) - 1:
                                self.second_papers.next()
                                self.second_papers.current_dialog_index = 0  # Reset index
                            else:
                                self.second_papers.next()
