# from settings import *

class LController:
    def loadLevel(levelName, screen):
        try:
            module = __import__(f'maps.{levelName}', fromlist=[levelName])
            map = getattr(module, levelName)
        except (ImportError, AttributeError):
            raise ValueError(f"Level '{levelName}' not found")

        return map(screen).draw()