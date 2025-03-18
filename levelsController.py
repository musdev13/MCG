# from settings import *

class LController:
    def loadLevel(levelName, screen):
        if levelName == "dreamW":
            from maps.dreamW import DreamW
            return DreamW(screen).draw()