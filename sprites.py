from ursina import *

class TopBackground(Sprite):
    def __init__(self, x = -4.5, y = 5.5, z=0):
        super().__init__()
        self.position = (x,y,z)
        self.model = 'cube'
        self.texture = 'assets/snow'
        self.scale = Vec3(10,10,0)
            
class Background(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model= 'cube'
        self.texture = 'background_level1'
        self.scale= Vec3(10,10,0)
        self.z = 5

class Stone(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 0
        self.texture = "assets/StoneSprite"

class TinOre(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 1
        self.texture = "assets/TinOreSprite"
        self.price = 5

class IronOre(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 2
        self.texture = "assets/IronOreSprite"
        self.price = 10

class SilverOre(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 2
        self.texture = "assets/SilverOreSprite"
        self.price = 15

class Gold(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 3
        self.texture = 'assets/GoldOreSprite'
        self.price = 25

class Chest(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.texture = 'assets/Chest'

class Stalactite(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 1
        self.texture = 'assets/Stalactite'

class ShaftPlank(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.texture = 'assets/ShaftPlank'

class ShaftSupport(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.texture = 'assets/ShaftSupport'

class Rail(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.texture = 'assets/Rail'

class Minecart(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.texture = 'assets/Minecart'