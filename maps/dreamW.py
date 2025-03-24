import pygame
from settings import gamePath
from Player import Player
from debugGrid import debugGrid as dG
from dialog import Dialog

class DreamW:
    def __init__(self, screen, gamePath=gamePath):
        self.play_intro = True  # New flag to control intro sequence and dialogs
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
            ["And... what now?", None, None, False, False]  # Fixed format with all 5 elements
        ]

        paperDialog_data = [
            ["You picked up the paper", None, None, False, False],
            [""]
        ]
        
        self.dialog = Dialog(screen, dialog_data)
        self.dialog1 = Dialog(screen, dialog1_data)
        
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
        self.all_dialogs_complete = False

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

    def draw(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            
            self.screen.blit(self.background, (0, 0))
            
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
                    self.player.move()
            else:
                # Skip all intro sequences and enable player movement immediately
                self.player.move()
            
            self.player.draw(self.screen)
            
            # Draw debug grid
            dG.draw(False, self.screen)
            
            # Draw active dialog (only if play_intro is True)
            if self.play_intro:
                if self.dialog.is_active:
                    self.dialog.draw()
                elif self.dialog1.is_active:
                    self.dialog1.draw()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        if self.dialog.is_active:
                            self.dialog.next()
                        elif self.dialog1.is_active:
                            self.dialog1.next()
                    elif event.key == pygame.K_b:
                        mouse_pos = pygame.mouse.get_pos()
                        index, coords = self.get_grid_pos(mouse_pos)
                        if index is not None:
                            print(f"Grid Index: {index}, Coordinates: {coords}")
