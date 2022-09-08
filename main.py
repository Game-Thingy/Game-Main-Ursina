from ursina import *
import random
app = Ursina()
# Window Setup
window.fps_counter.enabled = False
window.exit_button.visible = False
window.borderless = False
camera.position = Vec3(-5, -3, -35)

mapx = 10
mapy = 100
canMove = True

score = 0
class UI(Text):
    def __init__(self):
        super().__init__()
        self.text  = 'Score: ' + str(score)
        self.color = color.black
        
        
        
        

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.texture = 'white_cube'
        self.position = Vec3(-9, 1, -.1)
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
                    checkblock(self, movement = "right")
                if keys == 'a':
                    checkblock(self, movement = "left")
                if keys == 's':
                    checkblock(self, movement = "down")



class Wall(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 0
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

class Gold(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 3
        self.color = color.yellow

player = Player()
ui = UI()
ui.position = Vec3(-.8,.45,0)
blocks = [
    'wall1',
    'ore',
    'iron',
    'gold',
]

tiles =[


]

# Old Mine Generation code. Now all done with a single function
# instead of a line of if/else if statements
# def generateBlocks():
#     posx = 0
#     posy = 0
#     for x in range(mapy):
#         posx = 0
#         for y in range(mapx):
#             if x in range(0,5):
#                 y = Wall(posx, posy)
#                 tiles.append(y)

#             elif x in range(5,25):
#                 randint = random.choices(blocks, weights=[50, 2, 0, 0])
#                 if randint == ['wall1']:
#                     y = Wall(posx, posy)
#                     tiles.append(y)
#                 elif randint == ['ore']:
#                     y = Ore(posx, posy)
#                     tiles.append(y)

#             elif x in range(25,50):
#                 randint = random.choices(blocks, weights=[50, 2, 1, 0])
#                 if randint == ['wall1']:
#                     y = Wall(posx, posy)
#                     tiles.append(y)
#                 elif randint == ['ore']:
#                     y = Ore(posx, posy)
#                     tiles.append(y)
#                 elif randint == ['iron']:
#                     y = Iron(posx,posy)
#                     tiles.append(y)

#             elif x in range(50,100):
#                 randint = random.choices(blocks, weights=[50, 3, 2, 1])
#                 if randint == ['wall1']:
#                     y = Wall(posx, posy)
#                     tiles.append(y)
#                 elif randint == ['ore']:
#                     y = Ore(posx, posy)
#                     tiles.append(y)
#                 elif randint == ['iron']:
#                     y = Iron(posx,posy)
#                     tiles.append(y)
#                 elif randint == ['gold']:
#                     y = Gold(posx,posy)
#                     tiles.append(y)
#             posx -= 1
#         posy -= 1

# Generation function. Call the function with the below variables and it will generate the mine.
# If you don't want a tile to generate set weight as 0. You need all the weights of
# all tiles for this to work.
def generateBlocks(starting_posy, yrange, yrange2, weight1, weight2, weight3, weight4):
    posx = 0
    posy = starting_posy
    for x in range(yrange, yrange2):
        posx = 0
        for y in range(mapx):
            randint = random.choices(blocks, weights=[weight1, weight2, weight3, weight4])
            if randint == ['wall1']:
                y = Wall(posx, posy)
                tiles.append(y)
            elif randint == ['ore']:
                y = Ore(posx, posy)
                tiles.append(y)
            elif randint == ['iron']:
                y = Iron(posx,posy)
                tiles.append(y)
            elif randint == ['gold']:
                y = Gold(posx,posy)
                tiles.append(y)
            posx -= 1
        posy -= 1

generateBlocks(0, 0, 5, 40, 0, 0, 0) #Generates Stone. Y Levels 0-5
generateBlocks(-5, 5, 25, 40, 2, 0, 0) #Generates Stone and Ore Mix. Y Levels 5-25
generateBlocks(-25, 25, 50, 40, 2, 1, 0) #Generates Stone, Ore, and Iron Mix. Y Levels 25-50 
generateBlocks(-50, 50, 100, 40, 3, 2, 1) #Generates Stone, Ore, Iron, and Gold Mix. Y Levels 50-100

def checkblock(self, movement):
    for block in tiles:
        if player.x == block.x and player.y == block.y +1 and movement == "down":
            checkStrength(block, movement)
            print('Block Below!')
            break
        if player.y == block.y and player.x == block.x +1 and movement == "left":
            checkStrength(block, movement)
            print('Block Left!')
            break
        if player.y == block.y and player.x == block.x -1 and movement == "right":
            checkStrength(block, movement)
            print('Block Right!')
            break

def checkStrength(block, movement):
    if player.strength >= block.strength and movement == "down":
        block.position = Vec3(0,0,0)
        player.y -=1
        player.moves -= 1
        blockPay(block)
        print(block.name + ' Block Breakable')
    elif player.strength >= block.strength and movement == "left":
        block.position = Vec3(0,0,0)
        player.x -=1
        player.moves -= 1
        blockPay(block)
        print(block.name + ' Block Breakable')
    elif player.strength >= block.strength and movement == "right":
        block.position = Vec3(0,0,0)
        player.x +=1
        player.moves -= 1
        blockPay(block)
        print(block.name + ' Block Breakable')
    else:
        print("Can't Break That")

def blockPay(block):
    global score
    
    if block.name == 'ore':
        print('Added Moola')
        score = updateScore(5)
        ui.text = 'Score: '  + str(score)

        
def updateScore(oreprice):
    global score
    score = score + oreprice
    return score
    

# Updates the Camera Position if the Players position is Equal 
# (And less than just incase) so it keeps them at the center of the screen.

def update():
    if player.y <= camera.position.y:
        camera.position = Vec3(-5, camera.position.y - 1, -35)

# Need to add Gravity some how? Just check if there is a tile under the player
# and move them down a tile if not every 1 frame? Or maybe a bit more delay for
# smoother animation.


    

        
        

app.run()
