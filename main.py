from ursina import *
import random
app = Ursina()
# Window Setup
window.fps_counter.enabled = False
window.exit_button.visible = False
window.borderless = False
camera.position = Vec3(-5, -5, -35)


mapx = 10
mapy = 10
canMove = True

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.texture = 'white_cube'
        self.position = Vec3(-5, 1, -.1)
        self.origin_x = 0
        self.origin_y = 0
        self.moves = 100
        self.strength = 1




        self.disMove = Text(text=self.moves, wordwrap=30)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, keys):
        if canMove:
            if self.moves >= 1:
                if keys == 'd':

                    self.x += 1
                    self.moves -= 1
                if keys == 'a':
                    self.x -= 1
                    self.moves -= 1
                if keys == 's':
                    checkblock(self)

                    self.moves -= 1



class Wall(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0

        self.texture = "brick"


class Ore(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 1
        self.color = color.blue
class Iron(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 2
        self.color = color.red

player = Player()

blocks = [
    'wall1',
    'ore',
    'iron'
]

tiles =[


]


def generateBlocks():
    posx = 0
    posy = 0
    for x in range(mapx):
        x = Wall(posx, 1)
        posx -= 1
    for x in range(mapx):
        posx = 0
        for y in range(mapy):
            randint = random.choices(blocks, weights=[20, 1, 2])
            if randint == ['wall1']:
                y = Wall(posx, posy)
            elif randint == ['ore']:
                y = Ore(posx, posy)
                tiles.append(y)
            elif randint == ['iron']:
                y = Iron(posx,posy)
                tiles.append(y)
            posx -= 1
        posy -= 1

generateBlocks()
def checkblock(self):
    blockthere = False
    for block in tiles:
        if player.x == block.x and player.y == block.y +1:
            blockthere = True
            checkStrength(block, blockthere)
    if not blockthere:
        self.y -= 1
def checkStrength(block, blockthere):
    if player.strength >= block.strength:
        block.position = Vec3(0,0,0)
        player.y -=1
        blockPay(block)
        print(block.name)

def blockPay(block):
    if block.name == 'ore':
        print('Added Moolaaa')




app.run()

