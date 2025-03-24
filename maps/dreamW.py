import pygame
from settings import gamePath
from Player import Player
from debugGrid import debugGrid as dG
from dialog import Dialog

class DreamW:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.background = pygame.image.load(f"{gamePath}/img/dreamW/bg.png")
        self.grid_size = 48
        self.grid = []
        for y in range(12):  # 600/48 = 12 rows
            for x in range(16):  # 800/48 = 16 columns
                self.grid.append((x * self.grid_size, y * self.grid_size))
        self.map = None
        self.player = Player(self.grid[5][0], self.grid[80][1], 2)  # Place player at first grid position
        
        # Example dialog data
        dialog_data = [
            ["Hello there!", "Character 1", f"{gamePath}/img/avatars/char1.png", False, True],
            ["How are you today? aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Character 2", f"{gamePath}/img/avatars/char2.png", False, False],
            ["I'm doing great!", "Character 1", f"{gamePath}/img/avatars/char1.png", False, True]
        ]
        self.dialog = Dialog(screen, dialog_data)
        self.performing_action = False
        self.action_timer = 0

    def draw(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            
            self.screen.blit(self.background, (0, 0))
            
            # Handle player movement only when no dialog is active
            if not self.dialog.is_active and not self.performing_action:
                self.player.move()
                
            self.player.draw(self.screen)
            
            if self.performing_action:
                if current_time - self.action_timer < 1000:
                    self.player.direction = 'left'
                elif current_time - self.action_timer < 2000:
                    self.player.direction = 'right'
                else:
                    self.player.direction = 'down'
                    self.performing_action = False
                    self.dialog.is_active = True
            
            # Draw debug grid
            dG.draw(True, self.screen)
            
            # Draw dialog if active
            if self.dialog.is_active:
                self.dialog.draw()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and not self.dialog.is_active:
                        self.dialog.is_active = True
                        self.dialog.start_dialog()  # Начать диалог с анимацией открытия
                    elif event.key == pygame.K_z and self.dialog.is_active:
                        actID = self.dialog.next()
