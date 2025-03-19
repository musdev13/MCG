# from settings import *

class LController:
    def loadLevel(levelName, screen):
        if levelName == "dreamW":
            from maps.dreamW import DreamW as level
            
        if levelName == "intro":
            from maps.intro import intro as level
        
        return level(screen).draw()