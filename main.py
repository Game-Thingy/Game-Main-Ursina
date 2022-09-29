
from ctypes import alignment
from email.policy import default
from msilib import sequence
from turtle import back, onclick
from unicodedata import name
from ursina import *
import random
from ursina import Ursina, ButtonGroup
import asyncio
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


class UI(Text):
    def __init__(self):
        super().__init__()
        self.text  = 'Score: ' + str(score)
        self.color = color.white


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.texture = 'assets/PlayerSprite'
        self.position = Vec3(-9, 1, -.1)
        self.origin_x = 0
        self.origin_y = 0
        self.moves = 1000
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
            
class Background(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model= 'cube'
        self.texture = 'background_level1'
        self.scale= Vec3(10,10,0)
        self.z = 5

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
        self.price = 5

class Iron(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.texture = 'assets/iron_ore'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 2
        self.price = 10

class Gold(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.model = 'cube'
        self.scale = Vec3(1, 1, 0)
        self.z = 0
        self.strength = 3
        self.texture = 'assets/gold_ore'
        self.price = 25
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

def addPower():
    global score
    player.strength += 1
    print(player.strength)
    score -= 5

def closeMenu():
    menu.disabled = True
    menu.visible = False

wp = WindowPanel(
    title='Store',
    content=(
        Text(' '),
        Button(),
        Text('Add power' ),
        Button('+1', on_click= addPower),
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

moneyButton = wp.content[1]
moneyButton.icon = "assets/currency_symbol"
moneyButton.scale_x = .1
moneyButton.x = -.4

currentMoney = wp.content[0]
currentMoney.x = 0
currentMoney.y = -2.3

addButton = wp.content[3]

powerText = wp.content[2]
powerText.origin = (-1.9,.9)


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
menuButton = Button('Menu', scale_y = .05, color =color.light_blue , scale_x = .25, position = (.70, .45), on_click = openMenu) 

wp.z = 1
wp.visible = False
wp.disabled = True
wp.color = color.light_blue/.5
wp.panel.color = color.light_blue
wp.highlight_color = wp.color
wp.text_color = color.white
wp.position = (0,.25)
menu.z = -2
menu.visible = False
menu.disabled = True
menu.color = color.light_blue/.5
menu.panel.color = color.light_blue
menu.highlight_color = menu.color

storeButton = menu.content[2]
storeButton.highlight_color = addButton.color.tint(.2)
def displayClosed():
        storeClosed =Tooltip('Store is Closed')
        storeClosed.parent = storeButton
        storeClosed.position = (-.25,6,5)
        storeClosed.scale_x = 2
        storeClosed.scale_y = 15
        storeClosed.fade_out(duration=1)
        storeClosed.background.fade_out(duration=1)
    


menu.text_color = color.white
menu.position = (0,.25)
#print(wp.content[5].value)



#Game Objects
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

#Background

x_cord = 0
y_cord = 0
for x in range(mapx):
    x_cord = 10
    for y in range(4):
        y = Background(x_cord, y_cord)
        x_cord -= 10
    y_cord -= 10
       
    



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
generationStage = 100

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
        #Animation('assets/stone_break', scale = 1,fps=12, loop= False, position = (block.x, block.y))
        player.y -=1
        player.moves -= 1
        blockPay(block)
        print(block.name + ' Block Breakable')
        tiles.remove(block)
    elif player.strength >= block.strength and movement == "left":
        block.visible = False
        #Animation('assets/stone_break', scale = 1,fps=12, loop= False, position = (block.x, block.y))
        player.x -=1
        player.moves -= 1
        blockPay(block)
        tiles.remove(block)
        removedTiles.append(block)
        print(block.name + ' Block Breakable')
    elif player.strength >= block.strength and movement == "right":
        
        block.visible = False
        #Animation('assets/stone_break', scale = 1,fps=12, loop= False, position = (block.x, block.y))
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
    if block.name == 'ore':
        print('Added Moola')
        updateScore(block.price)
        ui.text = 'Score: '  + str(score)
    if block.name == 'iron':
        updateScore(block.price)
        ui.text = 'Score: ' + str(score)
    if block.name == 'gold':
        updateScore(block.price)
        ui.text = 'Score: ' + str(score)    

        
def updateScore(oreprice):
    global score
    score += oreprice




# Updates the Camera Position if the Players position is Equal 
# (And less than just incase) so it keeps them at the center of the screen.

def update():
    global canMove
    global currentMoney
    global score
    if storeButton.disabled == True:
        displayClosed()
    if score > 0:
        menu.content[2].disabled = False

    else:
        menu.content[2].disabled = True


    if score <= 0:
        addButton.disabled = True
        noMoney =Tooltip('You have no money!')
        noMoney.parent = addButton
        noMoney.position = (-.25,6,0)
        noMoney.scale_x = 2
        noMoney.scale_y = 15
        noMoney.fade_out(duration=1)
        noMoney.background.fade_out(duration=1)
        
    else:
        addButton.disabled = False
        
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
        generateBlocks(-generationStage, generationStage, generationStage + 1, 10, 3, 2, 1)
        generationStage += 1
        print(f"Did the Thing {generationStage}")
    if player.y <= -100 and generationStage in range(150,200):
        generateBlocks(-generationStage, generationStage, generationStage + 1, 5, 10, 2, 1)
        generationStage += 1
        print(f"Did the Thing v2 {generationStage}")
        

# Need to add Gravity some how? Just check if there is a tile under the player
# and move them down a tile if not every 1 frame? Or maybe a bit more delay for
# smoother animation.


    

        
        

app.run()
