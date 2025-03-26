from colors import PURPLE
import os

WIDTH, HEIGHT = 800, 600
gridColor = PURPLE
gamePath = os.path.dirname(__file__)
debugGrid = False

class Level:
    levelName = None    # This is now a class variable shared between all instances
    
    def getLevelName(self):
        return Level.levelName    # Access via class nam

playerSpeed = 1.5
