# from settings import *

class LController:
    def loadLevel(levelName, screen):
        if levelName == "dreamW":
            from maps.dreamW import DreamW as map
            
        if levelName == "intro":
            from maps.intro import intro as map
        
        if levelName == "dCat":
            from maps.dCat import dCat as map
        
        return map(screen).draw()