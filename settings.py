import colors
import os

WIDTH, HEIGHT = 800, 600
gridColor = colors.purple
gamePath = os.path.dirname(__file__)
debugGrid = True

class Level:
    levelName = None    # This is now a class variable shared between all instances
    
    def getLevelName(self):
        return Level.levelName    # Access via class nam
