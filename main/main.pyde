# File: main.py
'''Description: This program is going to be the main source file for our game.
The only built in functions will be in here (like draw, setup, keyPressed, etc).
'''


# Imports
import sprite
from sprite import Sprite
import combatSprite
import character
import room
import dungeon
import jkey
import inventory
import miniMap
from game import Game
from util import NO_DIR, NORTH, WEST, EAST, SOUTH, CLOSED, AJAR

# Ugly globals
key_states = dict()
startTime = millis()
endTime = 0
timeOfLastUpdate = millis()
ourGame = None
player = None
levelsPassed = 0
win = False

def setup():
    size(800, 800)
    # When we try doing this outside of setup(), for some reason we end up with
    # 2 invocations of Character()... and for some reason dict() doesn't work
    # either.
    # Ugly hack
    initializeImages()
    global player, ourGame
    ourGame = Game(startSize=10, sizeScale=3, levelCount=2)
    updateGameInfo()
    player = character.Character()
    


def draw():
    global timeOfLastUpdate, test, player
    background(30, 50, 130)
    update(millis() - timeOfLastUpdate)
    timeOfLastUpdate = millis()
    sprite.drawAllSprites()
    displayGameInfo(0, 0)

def keyPressed():
    global key_states
    # Adjust player velocity based on arrow key states
    

    if key == CODED:
        key_states[keyCode] = True
        if keyCode == UP:
            player.setWalkY(NORTH)
        elif keyCode == DOWN:
            player.setWalkY(SOUTH)
        if keyCode == LEFT:
            player.setWalkX(WEST)
        elif keyCode == RIGHT:
            player.setWalkX(EAST)
            
    else:
        # (UP, DOWN, LEFT, RIGHT)
        if key == 'q' or key == 'Q':
            player.triggerDoorToggle()
            
        if key == 'e' or key == 'E':
            player.toggleInventory()
            
        if key == 'm' or key == 'M':
            player.toggleMiniMap()
        
        # WASD controls
        if key == 'w' or key == 'W':
            player.setWalkY(NORTH)
        elif key == 's' or key == 'S':
            player.setWalkY(SOUTH)
        if key == 'a' or key == 'A':
            player.setWalkX(WEST)
        elif key == 'd' or key == 'D':
            player.setWalkX(EAST)

        key_states[key] = True


def keyReleased():
    global key_states
    if key == CODED:
        key_states[keyCode] = False
        if not (key_states.get(UP) or key_states.get(DOWN)):
            player.setWalkY(None)
        if not (key_states.get(LEFT) or key_states.get(RIGHT)):
            player.setWalkX(None)
    else:
        key_states[key] = False    
        if not (key_states.get('W') or key_states.get('w') or key_states.get('S') or key_states.get('s')):
            player.setWalkY(None)
        if not (key_states.get('a') or key_states.get('A') or key_states.get('d') or key_states.get('D')):
            player.setWalkX(None)


def update(timePassed):
    """timePassed is the amount of time passed since last update (in
    milliseconds)"""
    combatSprite.updatePositions(timePassed)
    updateGameInfo()
    global levelsPassed, player, win, endTime
    
    # at the end of a level
    if Game.victoryCount != levelsPassed:
        levelsPassed += 1
        ourGame.nextLevel()
        
        # if we've won
        if Game.victoryCount == ourGame.levelCount:
            endTime = float(millis()-startTime)
            win = True
            #player.removeSprite()
        else:
            player = character.Character()

    
def initializeImages():
    room.initDoor()
    room.initRoom()
    jkey.initKey()
    inventory.initInventory()
    miniMap.initMiniMap()
    
    
def updateGameInfo():
    # Game.gameInfo has tuples with strings and fontSize to be displayed
    # in the top left corner
    roomsCompleted = 0
    for room in ourGame.currentDungeon.rooms:
        if room.visited:
            roomsCompleted += 1
    Game.gameInfo[0] = ("Tutorial Dungeon: " + str(ourGame.levelCount) + " levels", 30)
    Game.gameInfo[1] = ("Level: " + str(Game.victoryCount), 20)
    Game.gameInfo[2] = (str(int(float(100*roomsCompleted)/float(ourGame.startSize + ourGame.sizeScale * (Game.victoryCount-1 if win else Game.victoryCount )))) + " % completed", 20)
    Game.gameInfo[3] = ("Time: " + nf((float(millis()-startTime) if not win else endTime)/1000.0, 0, 1)+"s", 20)
    
    
def displayGameInfo(x, y):
    fill(255)
    offset = 0
    textAlign(LEFT, TOP)
    for gameInfo in Game.gameInfo:
        textSize(gameInfo[1])
        text(gameInfo[0], x, y+offset)
        offset += gameInfo[1]
    fill(0)
    textSize(14)
    
    
def main():
    # The actual entry point to the program isn't really clear, so here we'll
    # just describe what order we expect Processing to automagically call stuff
    # in.

    # 1. setup()
    # 2. draw(), check for events like keyPressed, call the associated event
    # handlers (keyPressed(), keyReleased(), mousePressed(), mouseReleased(),
    # mouseClicked(), etc)
    # 3. Repeat 2 until the window is closed or escape is pressed or some other
    # thing that would indicate it should stop.
    pass


# The main() call of destiny (doesn't do anything)
main()