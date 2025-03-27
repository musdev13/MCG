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

        # Initialize player one cell above spawn point
        start_position = 58
        spawn_y = start_position // 16 - 1  # Subtract 1 to move up one cell
        spawn_x = start_position % 16
        self.player = Player(
            self.grid[spawn_y][spawn_x][0],
            self.grid[spawn_y][spawn_x][1],
            0,
            "d"
        )

        # Add collision blocks
        self.collisionBlocks = [22, 25, 18, 50, 34, 66, 82, 114, 98, 130, 146, 162, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 46, 27, 28, 44, 45, 26, 62, 78, 110, 94, 126, 142, 158, 174, 38, 39, 41, 40, 21, 20, 19]

        # Initialize dialogs
        self.firstpaper = Dialog(screen, [["It's just a piece of paper with my plans.", 'D', 'None', 'False', 'True'], ['Why am I even focusing on this?', 'D', 'None', 'False', 'True']], self.player)
        self.second_papers = Dialog(screen, [['These are just some of my drawings', 'D', 'None', 'False', 'True'], ["I don't see anything interesting in them", 'D', 'None', 'False', 'True']], self.player)
        self.intro2 = Dialog(screen, [['Right!', 'D', 'None', 'False', 'True'], ['I can go and socialize with someone, after all this time....', 'D', 'None', 'False', 'True']], self.player)
        self.intro1 = Dialog(screen, [['Hmm...', 'D', 'None', 'False', 'True'], ['first I need to figure out what to do.', 'D', 'None', 'False', 'True']], self.player)
        self.intro = Dialog(screen, [['Well, new day, new events!', 'D', 'None', 'False', 'True']], self.player)
        self.windows = Dialog(screen, [["They're windows, like...", 'D', 'None', 'False', 'True'], ["They're not real. They're painted.", 'D', 'None', 'False', 'True'], ['Something like that.', 'D', 'None', 'False', 'True']], self.player)
        self.sideTables = Dialog(screen, [["They're nightstands.", 'D', 'None', 'False', 'True'], ['I keep my things and neatly folded clothes in them.', 'D', 'None', 'False', 'True']], self.player)
        self.inscriptions = Dialog(screen, [["There's some writing here", ' ', 'None', 'False', 'True'], ['Here are the names of your friends', ' ', 'None', 'False', 'True'], ["The first name is Marco. The second name is illegible, but it's probably Vlad", ' ', 'None', 'False', 'True']], self.player)
        self.catCarpet = Dialog(screen, [["It's just a cute little cat-shaped rug.", ' ', 'None', 'False', 'True']], self.player)

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
            for event in pygame.event.get(): pass
        self.intro.start_dialog()
        while self.intro.is_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.intro.next()
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            if self.intro.is_active:
                self.intro.draw()
            pygame.display.flip()
        start_time = time.time()
        while time.time() - start_time < 2:
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get(): pass
        self.intro1.start_dialog()
        while self.intro1.is_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.intro1.next()
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            if self.intro1.is_active:
                self.intro1.draw()
            pygame.display.flip()
        start_time = time.time()
        while time.time() - start_time < 3:
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get(): pass
        self.intro2.start_dialog()
        while self.intro2.is_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.intro2.next()
            self.screen.blit(self.bg_image, (0, 0))
            self.player.draw(self.screen)
            if self.intro2.is_active:
                self.intro2.draw()
            pygame.display.flip()
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
                        if player_grid_index in [35, 36, 37] and not self.windows.is_active:
                            self.windows.start_dialog()
                        if player_grid_index in [60, 61] and not self.sideTables.is_active:
                            self.sideTables.start_dialog()
                        if player_grid_index in [172, 173] and not self.inscriptions.is_active:
                            self.inscriptions.start_dialog()
                        if player_grid_index in [70, 86, 85, 101, 117, 118, 134, 135, 136, 137, 138, 139, 124, 108, 92, 75, 73, 74, 88, 87, 102, 103, 119, 120, 104, 89, 105, 90, 91, 107, 121, 106, 122, 123] and not self.catCarpet.is_active:
                            self.catCarpet.start_dialog()
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
                        elif self.intro2.is_active:
                            if self.intro2.dialog_ended:
                                self.intro2.current_index = 0
                                self.intro2.dialog_ended = False
                                self.intro2.is_active = False
                                self.intro2.current_text = ""
                                self.intro2.display_text = ""
                                self.intro2.text_counter = 0
                                self.intro2.is_text_complete = False
                            else:
                                self.intro2.next()
                        elif self.intro1.is_active:
                            if self.intro1.dialog_ended:
                                self.intro1.current_index = 0
                                self.intro1.dialog_ended = False
                                self.intro1.is_active = False
                                self.intro1.current_text = ""
                                self.intro1.display_text = ""
                                self.intro1.text_counter = 0
                                self.intro1.is_text_complete = False
                            else:
                                self.intro1.next()
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
                        elif self.windows.is_active:
                            if self.windows.dialog_ended:
                                self.windows.current_index = 0
                                self.windows.dialog_ended = False
                                self.windows.is_active = False
                                self.windows.current_text = ""
                                self.windows.display_text = ""
                                self.windows.text_counter = 0
                                self.windows.is_text_complete = False
                            else:
                                self.windows.next()
                        elif self.sideTables.is_active:
                            if self.sideTables.dialog_ended:
                                self.sideTables.current_index = 0
                                self.sideTables.dialog_ended = False
                                self.sideTables.is_active = False
                                self.sideTables.current_text = ""
                                self.sideTables.display_text = ""
                                self.sideTables.text_counter = 0
                                self.sideTables.is_text_complete = False
                            else:
                                self.sideTables.next()
                        elif self.inscriptions.is_active:
                            if self.inscriptions.dialog_ended:
                                self.inscriptions.current_index = 0
                                self.inscriptions.dialog_ended = False
                                self.inscriptions.is_active = False
                                self.inscriptions.current_text = ""
                                self.inscriptions.display_text = ""
                                self.inscriptions.text_counter = 0
                                self.inscriptions.is_text_complete = False
                            else:
                                self.inscriptions.next()
                        elif self.catCarpet.is_active:
                            if self.catCarpet.dialog_ended:
                                self.catCarpet.current_index = 0
                                self.catCarpet.dialog_ended = False
                                self.catCarpet.is_active = False
                                self.catCarpet.current_text = ""
                                self.catCarpet.display_text = ""
                                self.catCarpet.text_counter = 0
                                self.catCarpet.is_text_complete = False
                            else:
                                self.catCarpet.next()

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
            if self.intro2.is_active:
                self.intro2.draw()
            if self.intro1.is_active:
                self.intro1.draw()
            if self.intro.is_active:
                self.intro.draw()
            if self.windows.is_active:
                self.windows.draw()
            if self.sideTables.is_active:
                self.sideTables.draw()
            if self.inscriptions.is_active:
                self.inscriptions.draw()
            if self.catCarpet.is_active:
                self.catCarpet.draw()

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
            hasattr(self, "intro2") and self.intro2.is_active or
            hasattr(self, "intro1") and self.intro1.is_active or
            hasattr(self, "intro") and self.intro.is_active or
            hasattr(self, "windows") and self.windows.is_active or
            hasattr(self, "sideTables") and self.sideTables.is_active or
            hasattr(self, "inscriptions") and self.inscriptions.is_active or
            hasattr(self, "catCarpet") and self.catCarpet.is_active
        ])
