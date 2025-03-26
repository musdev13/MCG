import pygame
from settings import gamePath, Level
from pyvidplayer2 import Video

class dCat:
    def __init__(self, screen, gamePath = gamePath):
        self.screen = screen
        self.video = Video(f"{gamePath}/img/dCat/dCat.mp4")
        
    
    def draw(self):
        running = True
        while running:
            # Check if video has ended
            if self.video.get_pos() >= self.video.duration:
                running = False
                Level.levelName = "d1"
                
                return
            
            # if not self.video.active:
            #     print("not active")

            self.video.draw(self.screen, (0,0), force_draw=False)

            if Level.levelName == "dCat":
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return