from ctypes import alignment
from email.policy import default
from msilib import sequence
from pyclbr import Function
from tkinter import Scale
from turtle import back, onclick, position
from unicodedata import name
from ursina import *
import random
from ursina import Ursina, ButtonGroup
import time
app = Ursina()
# Window Setup
window.fps_counter.enabled = True
window.exit_button.visible = False
window.borderless = False
camera.position = Vec3(-5, -3, -35)
last_time = time.time()


mapx = 10
mapy = 100
canMove = False
score = 0
interactiveSpot = False
class StartScreen(Sprite):
    def __init__(self):
        super().__init__()
        self.model = 'cube'
        self.texture = 'assets/Digging-Game Title'
    
        self.scale = Vec3(5,2,0)
        self.parent = camera
        self.position = Vec3(0,1,15)
        self.background = Sprite(model='cube',color = color.gray, scale = (25,25,0), parent=camera, position=(0,0,16))
        self.startButton = Button('Start', scale=(.5,.1,0), position=(0,-.4,0))
        self.startButton.on_click = self.startGame
        self.onStart = True
        
    def startGame(self):
        self.onStart = False
        destroy(self)
        destroy(self.background)
        destroy(self.startButton)
class Tool(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'cube'
        self.scale = Vec3(.08, .08, 0)
        self.texture = 'assets/PlayerSprite'
        self.position = Vec2(-.8,-.4)
        self.toolStrenth = 1
        self.parent = camera.ui
        self.visible = False
    def update(self):
        if startScreen.onStart == False:
            self.visible = True


class UI(Text):
    def __init__(self):
        super().__init__()
        self.text  = 'Score: ' + str(score)
        self.color = color.white
        self.visible = False

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.scale = Vec3(1, 1, 0)
        self.playerAnimate = Animator(animations = {
            'walkLeft': Animation('assets/Playerleft', parent=self, scale = 1, fps=12),
            'walkRight': Animation('assets/Playerright', parent=self, scale = 1, fps=12), 
            'standingL': Sprite('assets/PlayerSprite', parent=self, scale=6),
            'standingR': Sprite('assets/PlayerSpriteR', parent=self,scale=6),

            }, )
        self.position = Vec3(-9, 1, -.1)
        self.origin_x = 0
        self.origin_y = 0
        self.moves = 100
        self.strength = 1
        self.disMove = Text(text=self.moves, wordwrap=30)
        for key, value in kwargs.items():
            setattr(self, key, value)
    def update(self):
        global last_time
        
        if held_keys['a']:
            if last_time + 0.25 <= time.time():
                last_time = time.time()
                self.playerAnimate.state = 'walkLeft'
                checkblock(movement = "left")
                checkblank(movement= "left")

        elif held_keys['d']:
            if last_time + 0.25 <= time.time():
                last_time = time.time()
                self.playerAnimate.state = 'walkRight'
                checkblock(movement = "right")
                checkblank(movement= "right")
        
        else:
            if self.playerAnimate.state == 'walkLeft':
                self.playerAnimate.state = 'standingL'
            if self.playerAnimate.state == 'walkRight':
                self.playerAnimate.state= 'standingR'
    def input(self, keys):  
        if canMove:
            if self.moves >= 1:
                # if keys == 'd':
                #     checkblock(movement = "right")
                #     checkblank(movement = "right")
                # if keys == 'a':
                    
                #     checkblock(movement = "left")
                #     checkblank(movement= "left")
                if keys == 's':
                    checkblock(movement = "down")
                    checkblank(movement= "down")
                    checkinteractive()
                    updatePosition()
                if keys == 'w':
                    player.y += 1
                

            
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
        self.strength = 100
        self.color = color.brown
startScreen = StartScreen()
#Game Objects
player = Player()

tool = Tool()
ui = UI()
ui.position = Vec3(-.8,.45,0)
ui2 = UI()
ui2.position = Vec3(-.5,.45, 0)
#Pause Menu

def inStore():
    print("You are in the store")
    disableButton(menu)
    enableButton(wp)

def disableButton(disButton):
    disButton.enabled = False
    disButton.visible = False

def enableButton(enButton):
    enButton.enabled = True
    enButton.visible = True

def goBack():
    disableButton(wp)
    enableButton(menu)

def openMenu():
    menu.visible = True
    menu.disabled = False
def addMoves():
    global score
    player.moves += 10
    score -= 5


def addPower():
    global powerText
    global score
    player.strength += 1
    score -= 5
    power.text = 'Power: ' + str(player.strength)
    powerToolTip = Tooltip('Power up!')
    powerToolTip.parent = addButton
    powerToolTip.position = (0,-1,-1)
    powerToolTip.scale_x = 2
    powerToolTip.scale_y = 15
    powerToolTip.fade_out(duration=1)
    powerToolTip.background.fade_out(duration=1)

def closeMenu():
    menu.disabled = True
    menu.visible = False

wp = WindowPanel(
    title='Store',
    content=(
        Text('Power: ' + str(player.strength)),
        Text(' '),
        Button(),
        Text('Add power' ),
        Button('+1', on_click= addPower),
        Text('Add moves'),
        Button('+10', on_click= addMoves),
        Button('Back',on_click = goBack),
        Text(' ')
        #Text('Store', alignment= 'center'),
        #InputField(name='name_field'),
        #Button(text='Submit', color=color.azure, on_click= inStore),
        #Slider(),
        #Slider(),
        #ButtonGroup(('box', 'eslk', 'skffk'))
        ),
    )
#Store Contents    
power = wp.content[0]
moneyButton = wp.content[2]
moneyButton.icon = "assets/currency_symbol"
moneyButton.scale_x = .1
moneyButton.x = -.4

currentMoney = wp.content[1]
currentMoney.x = 0
currentMoney.y = -3.6

addButton = wp.content[4]
addMovesBtn = wp.content[6]
addMovesTxt = wp.content[5]
powerText = wp.content[3]
powerText.origin = (-1.9,.9)
addMovesTxt.origin = (-1.9,.9)

menu = WindowPanel(
    
    title='Menu',
    content=(
        Text(' '),
        Button('Coninue', on_click= closeMenu),
        Button('Store', on_click= inStore),
        Button('Exit', on_click=application.quit),
        Text(' ')
        
        
    ),
)
menuButton = Button('Menu', scale_y = .05, color =color.azure , scale_x = .25, position = (.70, .45), on_click = openMenu) 

wp.z = 1
wp.visible = False
wp.disabled = True
wp.color = color.azure/.8
wp.panel.color = color.azure
wp.highlight_color = wp.color
wp.text_color = color.white
wp.position = (0,.25, 1)
menu.z = -2
menu.visible = False
menu.disabled = True
menu.color = color.azure/.8
menu.panel.color = color.azure
menu.highlight_color = menu.color

storeButton = menu.content[2]
storeButton.highlight_color = addButton.color.tint(.2)
def displayClosed():
        storeClosed =Tooltip('Store is Closed')
        storeClosed.parent = storeButton
        storeClosed.position = (-.15,5,5)
        storeClosed.scale_x = 2
        storeClosed.scale_y = 15
        storeClosed.fade_out(duration=1)
        storeClosed.background.fade_out(duration=1)
    


menu.text_color = color.white
menu.position = (0,.25)
#print(wp.content[5].value)





blocks = [
    'stone',
    'tinore',
    'ironore',
    'silverore',
    'gold',
]

tiles =[


]
removedTiles = [

]
interactiveTiles = [

]

#Background

x_cord = 0
y_cord = 0
for x in range(mapx):
    x_cord = 10
    for y in range(4):
        y = Background(x_cord, y_cord)
        x_cord -= 10
    y_cord -= 10

#Add Other Backgrounds the further they go down
       
    



# Generation function. Call the function with the below variables and it will generate the mine.
# If you don't want a tile to generate set weight as 0. You need all the weights of
# all tiles for this to work.
def generateBlocks(starting_posy, yrange, yrange2, weight1, weight2, weight3, weight4, weight5):
    posx = 0
    posy = starting_posy
    for x in range(yrange, yrange2):
        posx = 0
        for y in range(mapx):
            randint = random.choices(blocks, weights=[weight1, weight2, weight3, weight4, weight5])
            if randint == ['stone']:
                y = Stone(posx, posy)
                tiles.append(y)
            elif randint == ['tinore']:
                y = TinOre(posx, posy)
                tiles.append(y)
            elif randint == ['ironore']:
                y = IronOre(posx,posy)
                tiles.append(y)
            elif randint == ['silverore']:
                y = SilverOre(posx,posy)
                tiles.append(y)
            elif randint == ['gold']:
                y = Gold(posx,posy)
                tiles.append(y)
            posx -= 1
        posy -= 1

generateBlocks(0, 0, 5, 40, 0, 0, 0, 0) #Generates Stone. Y Levels 0-5
generateBlocks(-5, 5, 25, 40, 2, 0, 0, 0) #Generates Stone and Ore Mix. Y Levels 5-25
generateBlocks(-25, 25, 50, 40, 2, 1, 0, 0) #Generates Stone, Ore, and Iron Mix. Y Levels 25-50 
generateBlocks(-50, 50, 100, 40, 3, 2, 1, 0) #Generates Stone, Ore, Iron, and Gold Mix. Y Levels 50-100
generationStage = 100

#Structure Generation, simply call the method of structure you want to generate and where
#Example: chestroom(3, -24)
def chestroom (posx, posy):
   structurelayout = ["air", "air", "air", "air", "air", "air", "air", "Chest", "air"]
   structureoffsets = [-1, 1, 0, 1, 1, 1, -1, 0, 0, 0, 1, 0, 1, -1, 0, -1, -1, -1]
   print("Chest Room generation started")
   structuretilegenerator(posx, posy, structurelayout, structureoffsets)

def structuretilegenerator (posx, posy, structurelayout, structureoffsets):
    i = 0
    while i < len(structurelayout):
        xoffset = structureoffsets[i]
        yoffset = structureoffsets[i + 1]
        for block in tiles:
            if posx + xoffset == block.x and posy + yoffset == block.y:
                if structurelayout[i] == "air":
                    removedTiles.append(block)
                    block.visible = False
                    tiles.remove(block)
                else:
                    removedTiles.append(block)
                    block.visible = False
                    tiles.remove(block)
                    # newx = posx + xoffset
                    # newy = posy + yoffset
                    # y = f'{structurelayout[i]}({newx}, {newy})'
                    # tiles.append(y)
                    # break

                    #Need to figure this part out, about to give up after 3 hours of trying to figure it out
        i += 1
        print(f'Chest Room Generation Finished {i}')

chestroom(-4, -5)

def checkblock(movement):
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

def checkblank(movement):
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
def checkinteractive():
        for block in interactiveTiles:
            global interactiveSpot
            if player.y == block.y and player.x == block.x:
                interactiveSpot = True
                print('Interactive Block!')
                break
            else:
                interactiveSpot = False
                print('Not an Interactive Block!')
   
def checkStrength(block, movement):
    if player.strength >= block.strength and movement == "down":
        removedTiles.append(block)
        block.visible = False
        player.y -=1
        player.moves -= 1
        blockPay(block)
        print(block.name + ' Block Breakable')
        tiles.remove(block)
    elif player.strength >= block.strength and movement == "left":
        block.visible = False
        #playAnimation('assets/Player left', block.x, block.y, player)
        player.x -=1
        player.moves -= 1
        blockPay(block)
        tiles.remove(block)
        removedTiles.append(block)
        interactiveTiles.append(block)
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
        tip =Tooltip('Can\'t Break this')
        tip.parent = player
        tip.position = (0,1,-1)
        tip.scale = 10
        tip.fade_out(duration=1)
        tip.background.fade_out(duration=1)
        

def blockPay(block):
    global score
    match block.name:
        case "tin_ore":
            updateScore(block.price)
        case "iron_ore":
            updateScore(block.price)
        case "silver_ore":
            updateScore(block.price)

# def blockPay(block):
#     global score
#     if block.name == "tin_ore":
#         updateScore(5)
#     if block.name == "iron_ore":
#         updateScore(10)
#     if block.name == "silver_ore":
#         updateScore(15)

        
def updateScore(oreprice):
    global score
    score += oreprice
    ui.text = 'Score: '  + str(score)

def updatePosition():
    ui.text = f'Position: {player.x} {player.y}'
    print(f'{player.x} {player.y}')




# Updates the Camera Position if the Players position is Equal 
# (And less than just incase) so it keeps them at the center of the screen.

def update():
    global canMove
    global currentMoney
    global score
    
    if startScreen.onStart == False:
        ui.visible = True
        ui2.visible = True
        canMove = True
    
    if storeButton.disabled == True:
        displayClosed()
    if score > 0:
        menu.content[2].disabled = False
        

    else:
        menu.content[2].disabled = True


    if score <= 0:
        addMovesBtn.disabled = True
        addButton.disabled = True
        noMoney =Tooltip('You have no money!')
        noMoney.parent = addButton
        noMoney.position = (-.25,7,0)
        noMoney.scale_x = 2
        noMoney.scale_y = 15
        noMoney.fade_out(duration=1)
        noMoney.background.fade_out(duration=1)
        
    else:
        addButton.disabled = False
        addMovesBtn.disabled = False

    if menu.visible == True:
        canMove = False
    else:
        canMove = True
    ui2.text = 'Moves: ' + str(player.moves)
    menu.stop_dragging()
    ui.text = 'Score: ' + str(score)
    currentMoney.text = str(score)
    wp.stop_dragging()
    global generationStage
    if player.y <= camera.position.y:
        camera.position = Vec3(-5, camera.position.y - 1, -35)
    if player.y <= -50 and generationStage in range(100,150):
        generateBlocks(-generationStage, generationStage, generationStage + 1, 10, 3, 2, 1, 1)
        generationStage += 1
        print(f"Did the Thing {generationStage}")
    if player.y <= -100 and generationStage in range(150,200):
        generateBlocks(-generationStage, generationStage, generationStage + 1, 5, 10, 2, 1, 1)
        generationStage += 1
        print(f"Did the Thing v2 {generationStage}")
    # if interactiveSpot == True:
    #     tip =Tooltip('E')
    #     tip.parent = player
    #     tip.position = (0,1,-1)
    #     tip.scale = 10
    for block in removedTiles:
        if player.x == block.x and player.y == block.y +1:
            player.y -=1
            print('Gravity!')
            break
    

        

# Need to add Gravity some how? Just check if there is a tile under the player
# and move them down a tile if not every 1 frame? Or maybe a bit more delay for
# smoother animation.


    

        
        

app.run()
