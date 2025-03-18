# from settings import *

class LController:
    def loadLevel(levelName, screen):
        if levelName == "dreamW":
            from maps.dreamW import DreamW
            return DreamW(screen).draw()
        if levelName == "intro":
            from maps.intro import intro
            return intro(screen).draw()