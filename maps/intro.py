import pygame
from settings import gamePath, Level
# from main import level
# from levelsController import LController as LC
import time

class intro:
    def __init__(self, screen, gamePath=gamePath):
        self.screen = screen
        self.gamePath = gamePath

    def draw(self):
        running = True
        start_time = time.time()
        
        while running:
            self.screen.fill((0, 0, 0))
            #здесь код сцены
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

            current_time = time.time() - start_time

            if current_time < 2:
                pass
            elif current_time < 10:
                text_alpha = min(255, (current_time - 3) * 51)  # Fade in over 5 seconds
                font = pygame.font.Font(None, 36)
                font = pygame.font.Font(f"{self.gamePath}/Mcg.ttf", 48)
                text = font.render("how much is left?", True, (255, 255, 255))
                text.set_alpha(int(text_alpha))
                text_rect = text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))
                self.screen.blit(text, text_rect)
            
            if current_time > 12:  # Total duration: 3 + 5 + 3 = 11 seconds
                running = False
                print("intro end")
                Level.levelName = "dreamW"
                break
            elif current_time > 6:  # Start screen fade at 6 seconds
                screen_alpha = min(255, (current_time - 6) * 85)  # Fade over 3 seconds
                white_surface = pygame.Surface(self.screen.get_size())
                white_surface.fill((255, 255, 255))
                white_surface.set_alpha(int(screen_alpha))
                self.screen.blit(white_surface, (0,0))

            pygame.display.flip()
            # pygame.time.Clock().tick(30)

        
        return None