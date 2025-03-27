# filepath: {gamePath}/maps/d1.py
import pygame
import time
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
        self.is_fading = False
        self.fade_screen = None

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
        self.intro = Dialog(screen, [['Text1', 'D', 'None', 'False', 'True'], ['Text2', 'D', 'None', 'False', 'True']], self.player)

        # Run startup script
        # Initialize fade surfaces
        self.black_surface = pygame.Surface((800, 600))
        self.black_surface.fill((0, 0, 0))
        self.cutscene_active = True
        start_time = time.time()
        fade_duration = 3
        while True:
            current_time = time.time() - start_time
            if current_time >= fade_duration:
                break
            fade_alpha = max(0, 255 * (1 - current_time / fade_duration))
            fade_surface = self.black_surface.copy()
            fade_surface.set_alpha(int(fade_alpha))
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            #pygame.time.Clock().tick(60)
            for event in pygame.event.get(): pass
        start_time = time.time()
        while time.time() - start_time < 2:
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            pygame.display.flip()
            #pygame.time.Clock().tick(60)
            for event in pygame.event.get(): pass
        self.intro.start_dialog()
        self.cutscene_active = False

    def draw(self):
        while self.running:
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
                            if self.firstpaper.dialog_ended:
                                self.firstpaper.current_index = 0
                                self.firstpaper.dialog_ended = False
                                self.firstpaper.is_active = False
                                self.firstpaper.current_text = ""
                                self.firstpaper.display_text = ""
                                self.firstpaper.text_counter = 0
                                self.firstpaper.is_text_complete = False
                            else:
                                self.firstpaper.next()
                        elif self.second_papers.is_active:
                            if self.second_papers.dialog_ended:
                                self.second_papers.current_index = 0
                                self.second_papers.dialog_ended = False
                                self.second_papers.is_active = False
                                self.second_papers.current_text = ""
                                self.second_papers.display_text = ""
                                self.second_papers.text_counter = 0
                                self.second_papers.is_text_complete = False
                            else:
                                self.second_papers.next()
                        elif self.intro.is_active:
                            if self.intro.dialog_ended:
                                self.intro.current_index = 0
                                self.intro.dialog_ended = False
                                self.intro.is_active = False
                                self.intro.current_text = ""
                                self.intro.display_text = ""
                                self.intro.text_counter = 0
                                self.intro.is_text_complete = False
                            else:
                                self.intro.next()

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
            if self.intro.is_active:
                self.intro.draw()

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
            hasattr(self, "firstpaper") and self.firstpaper.is_active or
            hasattr(self, "second_papers") and self.second_papers.is_active or
            hasattr(self, "intro") and self.intro.is_active
        ])
