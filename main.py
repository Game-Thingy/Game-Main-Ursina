from ctypes import alignment
from dis import dis
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
import sprites
import yaml

saveslot = 'saves/slot1.yml'
with open('saves/slot1.yml', 'r') as fileread:
        savesread = yaml.safe_load(fileread)

def openfileRead():
    global savesread
    global fileread
    with open(saveslot, 'r') as fileread:
        savesread = yaml.safe_load(fileread)

app = Ursina()
# Window Setup


window.fps_counter.enabled = False
window.exit_button.visible = False
window.cog_button.visible = False
window.cog_button.enabled = False
window.borderless = False
camera.position = Vec3(-5, 2, -35)
last_time = time.time()
confirm = None
windowsOpen = 0
mapx = 10
mapy = 100
canMove = False
score = savesread['Score']
interactiveSpot = False
class SaveButton(Button):
    def __init__(self,name='Save', posx = -.3, clicked = False, saveDay = 1, saveScore = 0):
        super().__init__()
        self.model = 'cube'
        self.scale_y = .05
        self.color = color.azure
        self.scale_x = .25
        self.position = (.70,posx)
        self.text = name
        self.clicked = clicked
        self.saveDay = saveDay
        self.saveScore = saveScore
        self.fileInfo = Text('Day: ' + str(saveDay) + ' Score: ' + str(saveScore),
            position = (-1.2, .25),
            scale_x = 3,
            scale_y = 18

        )
        self.fileInfo.parent = self
        
    
    def input(self, key):
            global windowsOpen
            global confirm
            if self.disabled or not self.model:
                return

            if key == 'left mouse down':
                if self.hovered:
                    self.model.setColorScale(self.pressed_color)
                    self.model.setScale(Vec3(self.pressed_scale, self.pressed_scale, 1))
                    self.clicked = True

            if key == 'left mouse up':
                if self.hovered:
                    self.model.setColorScale(self.highlight_color)
                    self.model.setScale(Vec3(self.highlight_scale, self.highlight_scale, 1))
                else:
                    self.model.setColorScale(self.color)
                    self.model.setScale(Vec3(1,1,1))
            if key == 'right mouse down' and self.clicked == True:
                if self.hovered:
                    
                    try: 
                        if windowsOpen <= 0:
                            windowsOpen += 1
                            startScreen.startButton.enabled = False
                            confirm = WindowPanel(
                                title = '',
                                content=(
                                    Text(''),
                                    Text('Are you sure you want to delete save?'),
                                    Text(''),
                                    Button('Yes', on_click=delete),
                                    Button('No', on_click=deleteWindow)
                                ),
                            )
                            confirm.z = -5
                            
                            print(saveslot)
                    except:
                        print('Can not delete')

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
        saveButton1.visible = False
        saveButton1.disabled = True
        saveButton2.visible = False
        saveButton2.disabled = True
        saveButton3.visible = False
        saveButton3.disabled = True
        menuButton.visible = True
        menuButton.disabled = False
        eraseText.visible = False
        chooseText.visible = False
class Tool(Entity):
    def __init__(self):
        super().__init__()
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
        self.day = savesread['Day']
        self.origin_x = 0
        self.origin_y = 0
        self.maxmoves = savesread['MaxMoves']
        self.moves = savesread['MaxMoves']
        self.strength = savesread['Strength']
        self.strengthprice = 10
        self.movePrice = 10
        self.disMove = Text(text=self.moves, wordwrap=30)
        for key, value in kwargs.items():
            setattr(self, key, value)
    def update(self):
        global last_time
        global canMove
        if canMove:
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
            elif held_keys['s']:
                if last_time + 0.25 <= time.time():
                    last_time = time.time()
                    checkblock(movement = "down")
                    checkblank(movement= "down")
            else:
                if self.playerAnimate.state == 'walkLeft':
                    self.playerAnimate.state = 'standingL'
                if self.playerAnimate.state == 'walkRight':
                    self.playerAnimate.state= 'standingR'


startScreen = StartScreen()

#Game Objects

player = Player()
topBackground = sprites.TopBackground()
tool = Tool()
ui = UI()
ui.position = Vec3(-.8,.45,0)
ui2 = UI()
ui2.position = Vec3(-.5,.45, 0)
uiDay = UI()
uiDay.position = Vec3(.4,.45,0)

#Pause Menu
def delete():
    global windowsOpen
    global confirm
    global savesread
    startScreen.startButton.enabled = True
    with open(saveslot) as deletefile:
        saves = yaml.safe_load(deletefile)
    saves['Score'] = 0
    saves['Day'] = 1
    saves['MaxMoves'] = 25
    saves['Strength'] = 1
    with open(saveslot, 'w') as deletefile:
        yaml.dump(saves, deletefile)
    deletefile.close()
    openfileRead()
    reloadsavedata()
    print("Deleted")
    windowsOpen = 0
    destroy(confirm)

def deleteWindow():
    global windowsOpen
    global confirm
    startScreen.startButton.enabled = True
    print('Nothing deleted')
    windowsOpen = 0
    destroy(confirm)

def disableButton(disButton):
    disButton.disabled = True
    disButton.visible = False

def enableButton(enButton):
    enButton.disabled = False
    enButton.visible = True
def moveToFront(obj, obj2):
    obj.z = -1
    obj2.z = 0

def inStore():
    print("You are in the store")
    disableButton(menu)
    enableButton(wp)
    moveToFront(wp,menu)
    

def goBack():
    disableButton(wp)
    enableButton(menu)
    moveToFront(menu,wp)

def openMenu():
    menu.visible = True
    menu.disabled = False
    moveToFront(menu,wp)
    
    
def addMoves():
    global score
    player.maxmoves += 10
    player.moves += 10
    score -= 5
    saveGame()

def addPower():
    global powerText
    global score
    player.strength += 1
    score -= 10
    # int(100 * (1 + 0.75 * float(savesread['Strength'])) * (1.15 ** float(savesread['Strength'])))
    power.text = 'Power: ' + str(player.strength)
    powerToolTip = Tooltip('Power up!')
    powerToolTip.parent = addButton
    powerToolTip.position = (0,-1,-1)
    powerToolTip.scale_x = 2
    powerToolTip.scale_y = 15
    powerToolTip.fade_out(duration=1)
    powerToolTip.background.fade_out(duration=1)
    saveGame()

def closeMenu():
    menu.disabled = True
    menu.visible = False

def resetMenu():
    
    menuButton1.text = 'Continue'
    menuButton1.on_click = closeMenu

    menuButton3.text = 'Restart'
    menuButton3.on_click = restart
    menuButton4.text = 'Exit'
    menuButton4.on_click = app.closeWindow
    menuButton4.disabled = False
    menuButton4.visible = True
    

def restart():
    closeMenu()
    resetMenu()
    player.position = Vec3(-9, 1, -.1)
    player.moves = savesread['MaxMoves']
    camera.position = Vec3(-5, -3, -35)
    player.day += 1
    global tiles
    global removedTiles
    global interactiveTiles
    global generationStage
    global backgroundtiles
    for block in tiles:
        destroy(block)
    for block in removedTiles:
        destroy(block)
    for block in interactiveTiles:
        destroy(block)
    for block in backgroundtiles:
        destroy(block)
    tiles = []
    removedTiles = []
    interactiveTiles = []
    backgroundtiles = []
    generateBlocks(0, 0, 5, 40, 0, 0, 0, 0) #Generates Stone. Y Levels 0-5
    generateBlocks(-5, 5, 25, 40, 2, 0, 0, 0) #Generates Stone and Ore Mix. Y Levels 5-25
    generateBlocks(-25, 25, 50, 40, 2, 1, 0, 0) #Generates Stone, Ore, and Iron Mix. Y Levels 25-50 
    generateBlocks(-50, 50, 100, 40, 3, 2, 1, 0) #Generates Stone, Ore, Iron, and Gold Mix. Y Levels 50-100
    generationStage = 100
    saveGame()

def saveGame():
    print('in save game function')
    with open(saveslot) as file:
        saves = yaml.safe_load(file)
    saves['Score'] = score
    saves['Day'] = player.day
    saves['MaxMoves'] = player.maxmoves
    saves['Strength'] = player.strength
    with open(saveslot, 'w') as file:
        yaml.dump(saves, file)
    file.close()
    fileread.close()
    openfileRead()

def reloadsavedata():
    global score
    score = savesread['Score']
    player.day = savesread['Day']
    player.maxmoves = savesread['MaxMoves']
    player.moves = player.maxmoves
    player.strength = savesread['Strength']
    print("Reloaded Save DATA I SWEAR TO GO IF YOU DON'T YOU WILL REGRET IT")

def dayEnd():
    openMenu()
    storeButton.disabled = False
    menuButton1.text = 'Go to next Day'
    menuButton1.on_click = restart
    menuButton3.text = 'Exit'
    menuButton3.on_click = app.closeWindow
    menuButton4.disabled = True
    menuButton4.visible = False

wp = WindowPanel(
    
    title='Store',
    content=(
        Text('Power: ' + str(player.strength)),
        Text(' '),
        Button(),
        Text('+1 Strength' ),
        Button(str(player.strengthprice), on_click= addPower),
        Text('+5 Moves'),
        Button((str(player.movePrice)), on_click= addMoves),
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

def checkedSave1():
    global saveslot
    global fileread
    saveButton1.color = color.blue
    saveButton2.color = color.azure
    saveButton3.color = color.azure
    saveButton2.clicked = False
    saveButton3.clicked = False
    saveGame()
    fileread.close()
    saveslot = 'saves/slot1.yml'
    openfileRead()
    reloadsavedata()
def checkedSave2():
    global saveslot
    global fileread
    saveButton2.color = color.blue
    saveButton1.color = color.azure
    saveButton3.color = color.azure
    saveButton1.clicked = False
    saveButton3.clicked = False
    print('Changed to save 2')
    saveGame()
    fileread.close()
    saveslot = 'saves/slot2.yml'
    openfileRead()
    reloadsavedata()
def checkedSave3():
    global saveslot
    global fileread
    saveButton3.color = color.blue
    saveButton2.color = color.azure
    saveButton1.color = color.azure
    saveButton1.clicked = False
    saveButton2.clicked = False
    saveGame()
    fileread.close()
    saveslot = 'saves/slot3.yml'
    openfileRead()
    reloadsavedata()
  
menu = WindowPanel(
    title='Menu',
    content=(
        Text(' '),
        Button('Continue', on_click= closeMenu),
        Button('Store', on_click= inStore),
        Button('Restart', on_click = restart),
        Button('Exit', on_click=app.closeWindow),
        Text(' ')
        
        
    ),
)

menuButton1 = menu.content[1]

menuButton3 = menu.content[3]
menuButton4 = menu.content[4]
menuButton = Button('Menu', scale_y = .05, color =color.azure , scale_x = .25, position = (.70, .45), on_click = openMenu) 
chooseText = Text(
    'Choose a save',
    color = color.white,
    position =  (.61, -.23, -5)
)
eraseText = Text(
    'Click save then right click to erase save',
    color = color.white,
    position =  (.49, -.47, -5)
)
saveButton1 = SaveButton('Save 1',-.3)   
saveButton1.on_click = checkedSave1
saveButton2 = SaveButton('Save 2', -.36)
saveButton2.on_click = checkedSave2
saveButton3 = SaveButton('Save 3', -.42) 
saveButton3.on_click = checkedSave3
checkedSave1()
saveButton1.clicked = True
#Doesn't pull data from yaml files yet.
wp.z = 0
wp.visible = False
wp.disabled = True
wp.color = color.azure/.8
wp.panel.color = color.azure
wp.highlight_color = wp.color
wp.text_color = color.white
wp.position = (0,.25)
menu.z = 0
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


blocks = [
    'stone',
    'tinore',
    'ironore',
    'silverore',
    'gold',
]
tiles =[

]
backgroundtiles =[

]
removedTiles = [

]
interactiveTiles = [

]

#Background

x_cord = 0
y_cord = 50
for x in range(100):
    x_cord = 10
    for y in range(4):
        y = sprites.Background(x_cord, y_cord)
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
                y = sprites.Stone(posx, posy)
                tiles.append(y)
            elif randint == ['tinore']:
                y = sprites.TinOre(posx, posy)
                tiles.append(y)
            elif randint == ['ironore']:
                y = sprites.IronOre(posx,posy)
                tiles.append(y)
            elif randint == ['silverore']:
                y = sprites.SilverOre(posx,posy)
                tiles.append(y)
            elif randint == ['gold']:
                y = sprites.Gold(posx,posy)
                tiles.append(y)
            posx -= 1
        posy -= 1

generateBlocks(0, 0, 5, 40, 0, 0, 0, 0) #Generates Stone. Y Levels 0-5
generateBlocks(-5, 5, 25, 40, 2, 0, 0, 0) #Generates Stone and Ore Mix. Y Levels 5-25
generateBlocks(-25, 25, 50, 40, 2, 1, 0, 0) #Generates Stone, Ore, and Iron Mix. Y Levels 25-50 
generateBlocks(-50, 50, 100, 40, 3, 2, 1, 0) #Generates Stone, Ore, Iron, and Gold Mix. Y Levels 50-100
generationStage = 100

def generateStructures(yrange, yrange2):
    for x in range(int(yrange / 15), int((yrange2 - 15) / 15)):
        doGeneration = random.randrange(1,3)
        if doGeneration == 1:
            chooseGeneration = random.randrange(1,5)
            if chooseGeneration == 1:
                chestroom(-x * 15)
            if chooseGeneration == 2:
                caveroomthatislegitjustairbecauseheislazyaf(-x * 15)
            if chooseGeneration == 3:
                mineshaft(-x * 15)
            if chooseGeneration == 4:
                jungle(-x * 15)

#Structure Generation, simply call the method of structure you want to generate and where
#Example: chestroom(3, -24)
def chestroom (posy):
   posx = random.randrange(-7,-3)
   structurelayout = ["air", "air", "air", "air", "air", "air", "air", "chest", "air"]
   structureoffsets = [-1, 1, 0, 1, 1, 1, -1, 0, 0, 0, 1, 0, 1, -1, 0, -1, -1, -1]
   print("Chest Room generation started")
   structuretilegenerator(posx, posy, structurelayout, structureoffsets)

def caveroomthatislegitjustairbecauseheislazyaf (posy):
   posx = random.randrange(-6,-4)
   structurelayout = ["air","air","air","air","air","air","air","air","air","air","air","air","air","air","air","air","air","air","air","air"]    
   structureoffsets = [0,1,1,1,2,1,-1,0,0,0,1,0,2,0,3,0,-2,-1,-1,-1,0,-1,1,-1,2,-1,3,-1,-2,-2,-1,-2,0,-2,1,-2,2,-2,3,-2]
   print("Cave room that is legit just air because he is lazy af generation started")
   structuretilegenerator(posx, posy, structurelayout, structureoffsets)

def mineshaft (posy):
   posx = int(-5)
   structurelayout = ["air","stalactite","air","air","air","air","air","air","air","air","air","air","shaftplank","shaftplank","shaftplank","shaftplank","air","air","air","air","shaftsupport","air","air","shaftsupport","air","air","rail","rail","shaftsupport","chest","air","shaftsupport","air","minecart"]
   structureoffsets = [-1,2,0,2,1,2,2,2,-2,1,-1,1,0,1,1,1,2,1,3,1,-3,0,-2,0,-1,0,0,0,1,0,2,0,3,0,4,0,-3,-1,-2,-1,-1,-1,0,-1,1,-1,2,-1,3,-1,4,-1,-3,-2,-2,-2,-1,-2,0,-2,1,-2,2,-2,3,-2,4,-2]
   print("Mineshaft generation started")
   structuretilegenerator(posx, posy, structurelayout, structureoffsets)

def jungle (posy):
    posx = int(-5)
    structurelayout = ["air","air","air","air","air","air","air","air","stalactite","stalactite","air","treeleft","jungle_leaf","treeright","air","air","air","air","air","jungle_leaf","jungle_leaf","jungle_leaf","air","air","air","air","air","air","log","vine","air","air","air","lilac","jungle_bush","air","log","vine","air","jungle_bush","jungle_bush"]
    structureoffsets = [-1,2,0,2,1,2,-2,1,-1,1,0,1,1,1,2,1,3,1,-3,0,-2,0,-1,0,0,0,1,0,2,0,3,0,4,0,-3,-1,-2,-1,-1,-1,0,-1,1,-1,2,-1,3,-1,4,-1,-3,-2,-2,-2,-1,-2,0,-2,1,-2,2,-2,3,-2,4,-2,-3,-3,-2,-3,1,-3,0,-3,1,-3,2,-3,3,-3,4,-3]
    print("Jungle generation started")
    structuretilegenerator(posx, posy, structurelayout, structureoffsets)

def structuretilegenerator (posx, posy, structurelayout, structureoffsets):
    i = 0
    j = 0
    while i < len(structureoffsets):
        xoffset = structureoffsets[i]
        yoffset = structureoffsets[i + 1]
        for block in tiles:
            if posx + xoffset == block.x and posy + yoffset == block.y:
                match structurelayout[j]:
                    case "air":
                        removedTiles.append(block)
                        block.visible = False
                        tiles.remove(block)
                        break
                    case "chest":
                        structureblockgenbackground(block, sprites.Chest, posx, posy, xoffset, yoffset)
                        break
                    case "stalactite":
                        structureblockgen(block, sprites.Stalactite, posx, posy, xoffset, yoffset)
                        break
                    case "shaftplank":
                        structureblockgenbackground(block, sprites.ShaftPlank, posx, posy, xoffset, yoffset)
                        break
                    case "shaftsupport":
                        structureblockgenbackground(block, sprites.ShaftSupport, posx, posy, xoffset, yoffset)
                        break
                    case "rail":
                        structureblockgenbackground(block, sprites.Rail, posx, posy, xoffset, yoffset)
                        break
                    case "minecart":
                        structureblockgenbackground(block, sprites.Minecart, posx, posy, xoffset, yoffset)
                        break
                    case "treeleft":
                        structureblockgenbackground(block, sprites.TreeLeft, posx, posy, xoffset, yoffset)
                        break
                    case "treeright":
                        structureblockgenbackground(block, sprites.TreeRight, posx, posy, xoffset, yoffset)
                        break
                    case "jungle_leaf":
                        structureblockgenbackground(block, sprites.JungleLeaf, posx, posy, xoffset, yoffset)
                        break
                    case "jungle_bush":
                        structureblockgenbackground(block, sprites.JungleBush, posx, posy, xoffset, yoffset)
                        break
                    case "vine":
                        structureblockgenbackground(block, sprites.JungleVine, posx, posy, xoffset, yoffset)
                        break
                    case "log":
                        structureblockgenbackground(block, sprites.Log, posx, posy, xoffset, yoffset)
                        break
                    case "lilac":
                        structureblockgenbackground(block, sprites.Lilac, posx, posy, xoffset, yoffset)
                        break
        i += 2
        j += 1

def structureblockgen(block, newblock, posx, posy, xoffset, yoffset):
    removedTiles.append(block)
    tiles.remove(block)
    block.visible = False
    newx = posx + xoffset
    newy = posy + yoffset
    y = newblock(newx,newy)
    tiles.append(y)

def structureblockgenbackground(block, newblock, posx, posy, xoffset, yoffset):
    removedTiles.append(block)
    tiles.remove(block)
    block.visible = False
    newx = posx + xoffset
    newy = posy + yoffset
    y = newblock(newx,newy)
    backgroundtiles.append(y)

generateStructures(20, 100)

def checkblock(movement):
    for block in tiles:
        if player.x == block.x and player.y == block.y +1 and movement == "down":
            checkStrength(block, movement)
            break
        elif player.y == block.y and player.x == block.x +1 and movement == "left":
            checkStrength(block, movement)
            break
        elif player.y == block.y and player.x == block.x -1 and movement == "right":
            checkStrength(block, movement)
            break

def checkblank(movement):
        for block in removedTiles:
            if player.x == block.x and player.y == block.y +1 and movement == "down":
                break
            elif player.y == block.y and player.x == block.x +1 and movement == "left":
                player.x -=1
                break
            elif player.y == block.y and player.x == block.x -1 and movement == "right":
                player.x += 1
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
        if player.moves <= 0:
            dayEnd()
        blockPay(block)
        tiles.remove(block)
    elif player.strength >= block.strength and movement == "left":
        block.visible = False
        player.x -=1
        player.moves -= 1
        if player.moves <= 0:
            dayEnd()
        blockPay(block)
        tiles.remove(block)
        removedTiles.append(block)
        interactiveTiles.append(block)
    elif player.strength >= block.strength and movement == "right":
        block.visible = False
        player.x +=1
        player.moves -= 1
        if player.moves <= 0:
            dayEnd()
        blockPay(block)
        tiles.remove(block)
        removedTiles.append(block)
    else:
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
       
def updateScore(oreprice):
    global score
    score += oreprice
    ui.text = 'Score: '  + str(score)

def updatePosition():
    ui.text = f'Position: {player.x} {player.y}'


# Updates the Camera Position if the Players position is Equal 
# (And less than just incase) so it keeps them at the center of the screen.

def update():
    global canMove
    global currentMoney
    global score
    if startScreen.onStart == False:
        ui.visible = True
        ui2.visible = True
        uiDay.visible = True
        canMove = True
    else:
        menuButton.visible = False
        menuButton.disabled = True
    if storeButton.disabled == True:
        displayClosed()
    if player.y == 1 or player.moves == 0:
        storeButton.disabled = False
    else:
        storeButton.disabled = True
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
    if menu.visible == True or player.moves == 0:
        canMove = False
    if wp.visible == True:
        canMove = False
    ui2.text = 'Moves: ' + str(player.moves)
    uiDay.text = "Day: " + str(player.day)
    menu.stop_dragging()
    ui.text = 'Score: ' + str(score)
    currentMoney.text = str(score)
    
    wp.stop_dragging()
    global generationStage
    if player.y <= camera.position.y:
        camera.position = Vec3(-5, camera.position.y - 1, -35)
    if player.y <= -50 and generationStage in range(100,150):
        generateBlocks(-generationStage, generationStage, generationStage + 1, 5, 3, 2, 1, 1)
        if player.y <= -150 and generationStage == 249:
            generateStructures(120, 150)
        print("Did the thing V1")
        generationStage += 1
    if player.y <= -100 and generationStage in range(150,200):
        generateBlocks(-generationStage, generationStage, generationStage + 1, 5, 4, 3, 2, 1)
        if player.y <= -150 and generationStage == 249:
            generateStructures(170, 200)
        print("Did the thing V2")
        generationStage += 1
    if player.y <= -150 and generationStage in range(200,250):
        generateBlocks(-generationStage, generationStage, generationStage + 1, 6, 5, 4, 2, 2)
        print("Did the thing V3")
        if player.y <= -150 and generationStage == 249:
            generateStructures(220, 250)
        generationStage += 1
    # if interactiveSpot == True:
    #     tip =Tooltip('E')
    #     tip.parent = player
    #     tip.position = (0,1,-1)
    #     tip.scale = 10
    for block in removedTiles:
        if player.x == block.x and player.y == block.y +1:
            player.y -=1
            break
    

        

# Need to add Gravity some how? Just check if there is a tile under the player
# and move them down a tile if not every 1 frame? Or maybe a bit more delay for
# smoother animation.


    

        
        

app.run()