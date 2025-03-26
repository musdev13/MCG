import pygame
from settings import gamePath, Level
from Player import Player
from debugGrid import debugGrid as dG
from dialog import Dialog
from pyvidplayer2 import Video

class dreamW:
    def __init__(self, screen, gamePath=gamePath):
        self.play_intro = False  # New flag to control intro sequence and dialogs
        self.screen = screen
        self.background = pygame.image.load(f"{gamePath}/img/dreamW/bg.png")
        self.grid_size = 48
        self.grid = []
        for y in range(12):  # 600/48 = 12 rows
            for x in range(16):  # 800/48 = 16 columns
                self.grid.append((x * self.grid_size, y * self.grid_size))
        self.map = None
        self.player = Player(self.grid[87][0], self.grid[87][1], 2)  # Place player at grid position (7,5)
        
        # Example dialog data
        dialog_data = [
            ["You looked around, but didn't recognize the place", None, None, False, False],
            ["Um...", "Marko", None, False, True],
            ["and where am I?", "Marko", None, False, True],
        ]

        dialog1_data = [
            ["And... what now?", "Marko", None, False, True]  # Fixed format with all 5 elements
        ]

        paperDialog_data = [
            ["You picked up the paper", None, None, False, False],
            ["''ym rdwanisg laawsy ned ta hte ilens''", "Text on paper", None, False, True],
            ["Maybe, you have dyslexia.", None, None, False, False],
        ]
        
        self.dialog = Dialog(screen, dialog_data, self.player)
        self.dialog1 = Dialog(screen, dialog1_data, self.player)

        self.paperDialog = Dialog(screen, paperDialog_data, self.player)
        self.carpetDialog = Dialog(screen, [
            ["Just a carpet with a cute face", None, None, False, False],
            ["Nothing special", None, None, False, False]
        ], self.player)
        self.spotDialog = Dialog(screen, [
            ["Just a spot", None, None, False, False],
            ["You hope it gets erased soon", None, None, False, False]
        ], self.player)

        self.catDialog = Dialog(screen, [
            ["You see a picture", None, None, False, False],
            ["It's a cat, maybe...", None, None, False, False],
            ["She most likely drew you as a cat", None, None, False, False]
        ], self.player)

        self.mrFaceDialog = Dialog(screen, [
            ["You see the outline of two eyes and a line that looks like a face", None, None, False, False],
            ["There is something written on the floor", None, None, False, False],
            ["''rm. afec''", "Text on the floor", None, False, True],
            ["You don't understand this", None, None, False, False]
        ], self.player)

        self.poemDialog = Dialog(screen, [
            ["''fi oy'uer tslil afllnig,", "...", None, False, True],
            ["I ekpe acllnig.", "...", None, False, True],
            ["nad fi no hte raorw", "...", None, False, True],
            ["htsi iwll ehpl oyu otomrrwo.''", "...", None, False, True],
            ["...", None, None, False, False],
            ["You don't understand what it means, but it sounds sad.", None, None, False, False]
        ], self.player)

        self.ihyDialog = Dialog(screen, [
            ["''AHET OYU''", "...", None, False, True],
            ["You think this means ''I love you''", None, None, False, False],
            ["I love you too!", "Marko", None, False, True]
        ], self.player)

        self.homeDialog = Dialog(screen, [
            ["This was your house.", None, None, False, False],
            ["unfortunately, that entrance is not available ", None, None, False, False],
            ["It's a good thing I made an alternate entrance in the lower left corner.", "Marko", None, False, True],
            ["It may not be visible, but it's there.", "Marko", None, False, True]
        ], self.player)
        
        # Add intro sequence properties
        self.sequence_started = False
        self.sequence_start_time = 0
        self.current_sequence = -1  # Start at -1 to ensure first update
        self.post_sequence_dialog_shown = False  # Add this new flag
        self.sequence_times = [
            3000,  # Initial wait
            2000,  # Left look duration
            2000,  # Right look duration
            2000  # Down look duration
        ]
        self.sequence_directions = [
            'down',    # Initial direction
            'left',    # Turn left
            'right',   # Turn right
            'down'     # Turn down
        ]

        # Add timing for second dialog
        self.dialog1_timer = 0
        self.dialog1_delay = 2000  # 2 seconds in milliseconds
        self.dialog1_started = False
        self.all_dialogs_complete = not self.play_intro  # Set to True if play_intro is False

        self.videobg = Video(f"{gamePath}/img/dreamW/blackwater.mp4")
        # self.videobg.set_size((800, 600))
        # self.videobg.preview()
        self.videobg.no_audio = True

        self.collisionBlocks = [
            16,17,1,21,22,80,96,
            112,128,144,162,163,179,
            178,183,184,185,186,191,
            175,143,142,126,79,
            63,47,30,13
        ]

        # Add cutscene properties
        self.cutscene_active = False
        self.cutscene_start_time = 0
        self.fade_surface = pygame.Surface((800, 600))
        self.fade_surface.fill((0, 0, 0))
        self.fade_alpha = 0

        self.running = True

    def start_sequence(self, current_time):
        if not self.sequence_started:
            self.sequence_started = True
            self.sequence_start_time = current_time
            self.player.direction = self.sequence_directions[0]
            return
        
        elapsed = current_time - self.sequence_start_time
        total_time = 0
        sequence_completed = True
        
        # Calculate which sequence step we should be in
        for i, time in enumerate(self.sequence_times):
            total_time += time
            if elapsed < total_time:
                sequence_completed = False
                if self.current_sequence != i:
                    self.current_sequence = i
                    if i < len(self.sequence_directions):
                        self.player.direction = self.sequence_directions[i]
                        self.player.current_sprite = self.player.sprites[self.player.direction]
                break
        
        # Start dialog when sequence is complete
        if sequence_completed and not self.dialog.is_active:
            self.dialog.is_active = True
            self.dialog.start_dialog()

    def get_grid_pos(self, mouse_pos):
        mx, my = mouse_pos
        grid_x = mx // self.grid_size
        grid_y = my // self.grid_size
        index = grid_y * 16 + grid_x  # 16 is the number of columns
        if 0 <= grid_x < 16 and 0 <= grid_y < 12:  # Check if within grid bounds
            return index, self.grid[index]
        return None, None

    def get_player_grid_index(self):
        # Get player's feet position (bottom center of sprite)
        player_feet_x = self.player.x + self.player.sprite_width // 2
        player_feet_y = self.player.y + self.player.sprite_height
        
        # Convert to grid position
        grid_x = player_feet_x // self.grid_size
        grid_y = player_feet_y // self.grid_size
        
        # Calculate grid index
        index = grid_y * 16 + grid_x
        return index if 0 <= grid_x < 16 and 0 <= grid_y < 12 else None

    def is_any_dialog_active(self):
        return any([
            self.dialog.is_active,
            self.dialog1.is_active,
            self.paperDialog.is_active,
            self.carpetDialog.is_active,
            self.spotDialog.is_active,
            self.catDialog.is_active,
            self.mrFaceDialog.is_active,
            self.poemDialog.is_active,
            self.ihyDialog.is_active,
            self.homeDialog.is_active
        ])

    def check_collision(self, next_x, next_y):
        # Calculate feet position (bottom center of sprite)
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
            
        # Add a small offset check to prevent sliding along walls
        offset = 10  # Adjust this value as needed
        for dx in [-offset, offset]:
            check_x = (feet_x + dx) // self.grid_size
            if 0 <= check_x < 16:
                index = grid_y * 16 + check_x
                if index in self.collisionBlocks:
                    return True
                    
        return False

    def handle_cutscene(self, current_time):
        if not self.cutscene_start_time:
            self.cutscene_start_time = current_time
            self.player.is_moving = False
            return True

        elapsed = current_time - self.cutscene_start_time
        
        if elapsed < 2000:  # First 2 seconds - just wait
            return True
        elif elapsed < 5000:  # Next 3 seconds - fade to black
            self.fade_alpha = min(255, int((elapsed - 2000) / 3000 * 255))
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))
            return True
        elif elapsed < 8000:  # Next 3 seconds - black screen
            self.screen.blit(self.fade_surface, (0, 0))
            return True
        else:  # After 8 seconds
            self.running = False
            Level.levelName = "dCat"

    def draw(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            
            # Video background handling
            if self.videobg.get_pos() >= self.videobg.duration:
                self.videobg.restart()
            self.videobg.draw(self.screen, (0,0), force_draw=False)
            self.screen.blit(self.background, (0, 0))
            
            # Set player movement based on dialog state AND cutscene state
            self.player.is_moving = not (self.is_any_dialog_active() or self.cutscene_active)
            
            # Only allow movement if not in cutscene
            if not self.cutscene_active:
                if self.play_intro:
                    # Handle intro sequence and first dialog
                    sequence_total_time = sum(self.sequence_times)
                    if not self.sequence_started or current_time - self.sequence_start_time < sequence_total_time:
                        self.start_sequence(current_time)
                        self.player.is_moving = False
                    elif not self.dialog.is_active and self.sequence_started and not self.post_sequence_dialog_shown:
                        self.dialog.start_dialog()
                        self.player.is_moving = False
                        self.post_sequence_dialog_shown = True
                    # Handle second dialog after delay
                    elif self.dialog.dialog_ended and not self.dialog1_started:
                        if self.dialog1_timer == 0:
                            self.dialog1_timer = current_time
                        elif current_time - self.dialog1_timer >= self.dialog1_delay:
                            self.dialog1.current_index = 0
                            self.dialog1.start_dialog()
                            self.dialog1_started = True
                    # Enable player movement only after all dialogs complete
                    elif not self.dialog.is_active and not self.dialog1.is_active and self.dialog1_started:
                        self.all_dialogs_complete = True
                        self.player.move(self)
                else:
                    self.player.move(self)
            
            self.player.draw(self.screen)
            
            # Draw debug grid
            dG.draw(True, self.screen)
            
            # Draw active dialog (only if play_intro is True)
            if self.play_intro:
                if self.dialog.is_active:
                    self.dialog.draw()
                elif self.dialog1.is_active:
                    self.dialog1.draw()
            
            # Add paperDialog drawing
            if self.paperDialog.is_active:
                self.paperDialog.draw()
            
            # Add carpetDialog drawing
            if self.carpetDialog.is_active:
                self.carpetDialog.draw()
            
            if self.spotDialog.is_active:
                self.spotDialog.draw()
            
            if self.catDialog.is_active:
                self.catDialog.draw()
            if self.mrFaceDialog.is_active:
                self.mrFaceDialog.draw()
            if self.poemDialog.is_active:
                self.poemDialog.draw()
            if self.ihyDialog.is_active:
                self.ihyDialog.draw()
            
            if self.homeDialog.is_active:
                self.homeDialog.draw()
            
            if self.cutscene_active:
                self.cutscene_active = self.handle_cutscene(current_time)

            if Level.levelName == "dreamW":
                pygame.display.flip()
                pygame.time.Clock().tick(120)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.videobg.close()
                    pygame.quit()
                    return
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        player_grid_index = self.get_player_grid_index()
                        carpet_indices = [103, 104, 120, 119]  # Grid indices for carpet area
                        spot_indices = [92,93,109,108]  # Grid indices for spot area
                        mrFace_indices = [113,114,115,129,130,131,132,145,146,147,148]
                        poem_indices = [9,10,11,12,25,26,27,28,41,42]
                        ihy_indices = [149,150,151,152,153,154,155,169,170,171,168,167,166]
                        homeDialog_indices = [180,181,182]

                        # Add this new condition before other dialog checks

                        if player_grid_index == 177:
                            print("нажато")
                            self.cutscene_active = True
                            self.cutscene_start_time = 0
                        elif player_grid_index == 174 and not self.paperDialog.is_active:
                            self.paperDialog.start_dialog()
                        # Only allow carpet dialog interaction when intro is complete
                        elif player_grid_index in carpet_indices and not self.carpetDialog.is_active and self.all_dialogs_complete:
                            self.carpetDialog.start_dialog()
                        elif player_grid_index in spot_indices and not self.spotDialog.is_active:
                            self.spotDialog.start_dialog()
                        elif player_grid_index == 49 and not self.catDialog.is_active:
                            self.catDialog.start_dialog()
                        elif player_grid_index in mrFace_indices and not self.mrFaceDialog.is_active:
                            self.mrFaceDialog.start_dialog()
                        elif player_grid_index in poem_indices and not self.poemDialog.is_active:
                            self.poemDialog.start_dialog()
                        elif player_grid_index in ihy_indices and not self.ihyDialog.is_active:
                            self.ihyDialog.start_dialog()
                        elif player_grid_index in homeDialog_indices and not self.homeDialog.is_active:
                            self.homeDialog.start_dialog()
                        

                        elif self.dialog.is_active:
                            self.dialog.next()
                        elif self.dialog1.is_active:
                            self.dialog1.next()
                        elif self.paperDialog.is_active:
                            self.paperDialog.next()
                        elif self.carpetDialog.is_active:
                            self.carpetDialog.next()
                        elif self.spotDialog.is_active:
                            self.spotDialog.next()
                        elif self.catDialog.is_active:
                            self.catDialog.next()
                        elif self.mrFaceDialog.is_active:
                            self.mrFaceDialog.next()
                        elif self.poemDialog.is_active:
                            self.poemDialog.next()
                        elif self.ihyDialog.is_active:
                            self.ihyDialog.next()
                        elif self.homeDialog.is_active:
                            self.homeDialog.next()

                    elif event.key == pygame.K_b:
                        mouse_pos = pygame.mouse.get_pos()
                        index, coords = self.get_grid_pos(mouse_pos)
                        if index is not None:
                            print(f"Grid Index: {index}, Coordinates: {coords}")
