from turtle import Turtle
from unicodedata import name
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
class Tool(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'cube'
        self.scale = Vec3(.08, .08, 0)
        self.texture = 'assets/PlayerSprite'
        self.position = Vec2(-.8,-.4)
        self.toolStrenth = 1
        self.parent = camera.ui

class Gui(Button):
    def __init__(self):
        super().__init__()
        global canMove
        self.scale = (.5,.25)
        self.visible = False
        self.disabled = True
        self.color = color.white
        

    def input(self, keys):
        global canMove
        if keys == 'tab':
            if self.visible == False:
                self.disabled = False
                for x in removedTiles:
                    print(x)
                self.visible = True
                canMove = False
            else:
                self.visible = False
                self.disabled = True
                canMove = True

                
  


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
        self.texture = 'assets/PlayerSprite'
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
                    checkblank(self,movement = "right")
                if keys == 'a':
                    checkblock(self, movement = "left")
                    checkblank(self, movement= "left")
                if keys == 's':
                    checkblock(self, movement = "down")
                    checkblank(self, movement= "down")
            
        




class Wall(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 0
        self.texture = "assets/StoneSprite"

class Ore(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 1
        self.texture = "assets/OreSprite"

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
#Pause Menu
def inStore():
    print("You are in the store")
    gui.disabled = True
    gui.visible = False
    gui2.disabled = True
    gui2.visible = False
    store.disabled = True
    store.visible = False


gui = Gui()
gui.on_click = application.quit
gui.texture = 'assets/Exit_Button'
gui.position = (0,.0)
gui2 = Gui()
gui2.texture = 'assets/Continue_Button'
gui2.position = (0,.25)
store = Gui()
store.text = 'Store'
store.position = (0, -.25)
store.on_click = inStore








player = Player()
tool = Tool()
ui = UI()
ui.position = Vec3(-.8,.45,0)
ui2 = UI()
ui2.position = Vec3(-.5,.45, 0)

blocks = [
    'wall1',
    'ore',
    'iron',
    'gold',
]

tiles =[


]
removedTiles = [

]


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
        elif player.y == block.y and player.x == block.x +1 and movement == "left":
            checkStrength(block, movement)
            print('Block Left!')
            break
        elif player.y == block.y and player.x == block.x -1 and movement == "right":
            checkStrength(block, movement)
            print('Block Right!')
            break

def checkblank(self, movement):
        for block in removedTiles:
            if player.x == block.x and player.y == block.y +1 and movement == "down":
                print('Can Move Back')
                break
            elif player.y == block.y and player.x == block.x +1 and movement == "left":
                player.x -=1
                print('Can Move Left!')
                break
            elif player.y == block.y and player.x == block.x -1 and movement == "right":
                player.x += 1
                print('Can Move Right!')
                break
   
def checkStrength(block, movement):
    if player.strength >= block.strength and movement == "down":
        removedTiles.append(block)
        block.visible = False
        print(block.color)
        player.y -=1
        player.moves -= 1
        blockPay(block)
        print(block.name + ' Block Breakable')
        tiles.remove(block)
    elif player.strength >= block.strength and movement == "left":
        block.visible = False
        player.x -=1
        player.moves -= 1
        blockPay(block)
        tiles.remove(block)
        removedTiles.append(block)
        print(block.name + ' Block Breakable')
    elif player.strength >= block.strength and movement == "right":
        block.visible = False
        player.x +=1
        player.moves -= 1
        blockPay(block)
        print(block.name + ' Block Breakable')
        tiles.remove(block)
        removedTiles.append(block)
    else:
        print("Can't Break That")

def blockPay(block):
    global score
    
    if block.name == 'ore':
        print('Added Moola')
        updateScore(5)
        ui.text = 'Score: '  + str(score)

        
def updateScore(oreprice):
    global score
    score += oreprice




# Updates the Camera Position if the Players position is Equal 
# (And less than just incase) so it keeps them at the center of the screen.

def update():
    ui2.text = 'Moves: ' + str(player.moves)
    if player.y <= camera.position.y:
        camera.position = Vec3(-5, camera.position.y - 1, -35)
    

# Need to add Gravity some how? Just check if there is a tile under the player
# and move them down a tile if not every 1 frame? Or maybe a bit more delay for
# smoother animation.


    

        
        

app.run()
