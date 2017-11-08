from util import NO_DIR, WEST, EAST, SOUTH, NORTH, x, y, AJAR, CLOSED, opposite
from sprite import Sprite

class Door(Sprite):
    # Door images
    # Loading only works as early as setup(), unfortunately, so this has to
    # be put off until then... see initRoom() at bottom of file.
    # https://github.com/processing/processing/issues/4501
    northDoorOpen = None
    northDoorClosed = None
    eastDoorOpen = None
    eastDoorClosed = None
    westDoorOpen = None
    westDoorClosed = None
    southDoorOpen = None
    southDoorClosed = None
    doorZones = []

    level = 0

    def __init__(self, direction, initState=CLOSED):
        super(Door, self).__init__(Door.doorZones[direction], self,
                                   manageInSprite=False)
        self.state = initState
        self.direction = direction
        self.level = Door.level

    def draw(self, x, y):
        if self.direction == WEST:
            if self.state == AJAR:
                image(Door.westDoorOpen, 0,
                      height/2 - Door.westDoorOpen.height/2)
            else:
                image(Door.westDoorClosed, 0,
                  height/2 - Door.westDoorClosed.height/2)
        elif self.direction == NORTH:
            if self.state == AJAR:
                image(Door.northDoorOpen, width/2 - Door.northDoorOpen.width/2,
                      0)
            else:
                image(Door.northDoorClosed, width/2 -
                      Door.northDoorClosed.width/2, 0)
        elif self.direction == EAST:
            if self.state == AJAR:
                image(Door.eastDoorOpen, width - Door.eastDoorOpen.width,
                      height/2 - Door.eastDoorOpen.height/2)
            else:
                image(Door.eastDoorClosed, width - Door.eastDoorClosed.width,
                      height/2 - Door.eastDoorClosed.height/2)
        elif self.direction == SOUTH:
            if self.state == AJAR:
                image(Door.southDoorOpen, width/2 - Door.southDoorOpen.width/2,
                      height - Door.southDoorOpen.height)
            else:
                image(Door.southDoorClosed, width/2 -
                      Door.southDoorClosed.width/2, height -
                      Door.southDoorClosed.height)
       

    def toggleOpen(self):
        #print "Door ", self.direction, "was ", self.state, "now is " not self.state
        self.state = not self.state


class Room(Sprite):

    # Wall depth in pixels
    wallDepth = 75

    currentRoom = None

    # Some enums for the types of rooms
    START = 0
    PUZZLE = 1
    BATTLE = 2
    EMPTY = 3
    END = 4

    # Room images
    startRoom = None
    puzzleRoom = None
    battleRoom = None
    endRoom = None

    def __init__(self, enterDirection=NO_DIR, type=START, doors=None, gridCoord=[None, None], currentRoom=False):
        """ """
        # DON'T GET RID OF THIS, IDIOT butt
        if doors != None:
            self.doors = doors
        else:
            self.doors = [None, None, None, None]
            
        super(Room, self).__init__((Room.wallDepth,
                                    Room.wallDepth, width - Room.wallDepth,
                                    height - Room.wallDepth),
                                   self,
                                   location=(width/2,
                                             height/2)) 
        self.spritesInRoom = []
        self.visited = False
        self.discovered = False
        if currentRoom:
            Room.currentRoom = self
            Room.currentRoom.discovered = True
            Room.currentRoom.visited = True
        self.wallBounds = [0, 0, 0, 0]
        self.gridCoord = gridCoord
        self.adjRooms = [None, None, None, None]
        self.type = type
        self.enterDirection = enterDirection
        self.rightKey = None
        self.roomId = -1
        self.locked = True
        
        
        
    

    def enter(self, enterDirection):
        # enter a room from a direction 
        self.enterDirection = enterDirection
        if not self.visited:
            self.visited = True
            self.locked = False
        Room.currentRoom = self
        print "adjRooms: ", self.adjRooms
        if enterDirection != NO_DIR and self.doors[enterDirection] != None:
            self.doors[enterDirection].state = AJAR
            if self.adjRooms[enterDirection] != None:
                self.adjRooms[enterDirection].doors[opposite(enterDirection)].state = AJAR
        print self.gridCoord
        

    def draw(self, arg1, arg2):
        if self == Room.currentRoom:
            # draw the background image based on the type of currentRoom
            drawImg = None
            if Room.currentRoom.type == Room.START:
                drawImg = Room.startRoom
            elif Room.currentRoom.type == Room.PUZZLE:
                drawImg = Room.puzzleRoom
            elif Room.currentRoom.type == Room.BATTLE:
                drawImg = Room.battleRoom
            elif Room.currentRoom.type == Room.EMPTY:
                drawImg = Room.startRoom
            elif Room.currentRoom.type == Room.END:
                drawImg = Room.endRoom
            image(drawImg, 0, 0)
            textAlign(CENTER)
            text("Room " + str(self.roomId) if self.roomId != -1 else "Start", 
                 (self.boundingBox[2]+self.boundingBox[0])/2, 
                 (self.boundingBox[3]+self.boundingBox[1])/2)
            
            for door in self.doors:
                if door:
                    door.drawSprite()
                    if door.direction == WEST and Room.currentRoom.adjRooms[WEST] != None:
                        text("Room " + str(Room.currentRoom.adjRooms[WEST].roomId) if Room.currentRoom.adjRooms[WEST].roomId != -1 else "Start",
                        door.boundingBox[EAST] + 20, 
                        (door.boundingBox[SOUTH] + door.boundingBox[NORTH]) / 2)
                    elif door.direction == NORTH and Room.currentRoom.adjRooms[NORTH] != None:
                        text("Room " + str(Room.currentRoom.adjRooms[NORTH].roomId) if Room.currentRoom.adjRooms[NORTH].roomId != -1 else "Start", 
                             (door.boundingBox[EAST] + door.boundingBox[WEST]) / 2, 
                             door.boundingBox[SOUTH] + 20)
                    elif door.direction == EAST and Room.currentRoom.adjRooms[EAST] != None:
                        text("Room " + str(Room.currentRoom.adjRooms[EAST].roomId) if Room.currentRoom.adjRooms[EAST].roomId != -1 else "Start", 
                             door.boundingBox[WEST] - 20, 
                             (door.boundingBox[SOUTH] + door.boundingBox[NORTH]) / 2)
                    elif door.direction == SOUTH and Room.currentRoom.adjRooms[SOUTH] != None:
                        text("Room " + str(Room.currentRoom.adjRooms[SOUTH].roomId) if Room.currentRoom.adjRooms[SOUTH].roomId != -1 else "Start", 
                             (door.boundingBox[EAST] + door.boundingBox[WEST])/2, 
                             door.boundingBox[NORTH] - 20)
                                     
            textAlign(CORNER)
        
    

    def updateDoor(self, direction, state):
        """ """
        print "Door direction updated:: ", direction
        self.doors[direction].state = state


    def toggleDoor(self, direction):
        print "Door direction toggled:: ", direction
        self.doors[direction].state = not self.doors[direction].state


    def setWallBounds(self):
        self.wallBounds[WEST] = Door.westDoorOpen.width
        self.wallBounds[NORTH] = Door.southDoorOpen.height
        self.wallBounds[EAST] = Door.eastDoorOpen.width
        self.wallBounds[SOUTH] = Door.southDoorOpen.height
        

def initDoor():
    Door.northDoorOpen = loadImage("northDoorOpen.png")
    Door.northDoorClosed = loadImage("northDoorClosed.png")
    Door.eastDoorOpen = loadImage("eastDoorOpen.png")
    Door.eastDoorClosed = loadImage("eastDoorClosed.png")
    Door.southDoorOpen = loadImage("southDoorOpen.png")
    Door.southDoorClosed = loadImage("southDoorClosed.png")
    Door.westDoorOpen = loadImage("westDoorOpen.png")
    Door.westDoorClosed = loadImage("westDoorClosed.png")
    # West
    Door.doorZones.append((0,
                           height/2 - Door.westDoorOpen.height/2,
                           Room.wallDepth,
                           height/2 + Door.westDoorOpen.height/2))
    # North
    Door.doorZones.append((width/2 - Door.northDoorOpen.width/2,
                           0,
                           width/2 + Door.northDoorOpen.width/2,
                           Room.wallDepth))
    # East
    Door.doorZones.append((width - Room.wallDepth,
                           height/2 - Door.eastDoorOpen.height/2,
                           width,
                           height/2 + Door.eastDoorOpen.height/2))
    # South
    Door.doorZones.append((width/2 - Door.southDoorOpen.width/2,
                           height - Room.wallDepth,
                           width/2 + Door.southDoorOpen.width/2,
                           height))


def initRoom():
        """Annoyingly enough, we can't use loadImage() until at least setup()
        time."""
        Room.startRoom = loadImage("startRoom.png")
        Room.puzzleRoom = loadImage("puzzleRoom.png")
        Room.battleRoom = loadImage("battleRoom.png")
        Room.endRoom = loadImage("endRoom.png")