from util import NO_DIR, WEST, EAST, SOUTH, NORTH, x, y, AJAR, CLOSED, opposite
from room import Room, Door
from jkey import Key
import miniMap
from skeleton import Skeleton
import random as r

class Dungeon(object):
    
    floorKeys = []
    
    def __init__(self, roomCount):
        self.roomCount = roomCount

        # list of all rooms in dungeon.. maybe restructure this later
        self.rooms = []
        self.visitedRoomCount = 1
        
        self.generateDungeon(roomCount)
        self.miniMap = miniMap.MiniMap(self.rooms)
        miniMap.updateMiniMap()
        
            
    def generateDungeon(self, roomCount):
        """ """
        print "Generating Dungeon"
        # initial start room creation
        self.rooms.append(Room(gridCoord=[0, 0], currentRoom=True))
        
        # populate rooms list
        while len(self.rooms) != roomCount:
            # random existing room to add on to (0-len(rooms[]-1))
            chosenRoom = r.randint(0, len(self.rooms) - 1)
            # random room type (0-4)
            roomType = Room.END if len(self.rooms) + 1 == roomCount else r.randint(Room.PUZZLE, Room.EMPTY) 
            # random direction (0-3)
            roomDir = r.randint(WEST, SOUTH)
            self.addRoom(self.rooms[chosenRoom], roomType, roomDir)
        for room in self.rooms:
            if room.type == Room.BATTLE:
                for i in range(r.randint(1,100)):
                    newBaddy = Skeleton()
                    xPos = r.randint(Room.currentRoom.boundingBox[WEST] + newBaddy.currentAnimation.images[0].width/2,
                                     Room.currentRoom.boundingBox[EAST] - newBaddy.currentAnimation.images[0].width/2)
                    yPos = r.randint(Room.currentRoom.boundingBox[NORTH] + newBaddy.currentAnimation.images[0].height/2,
                                     Room.currentRoom.boundingBox[SOUTH] - newBaddy.currentAnimation.images[0].height/2)
                    newBaddy.location = (xPos, yPos)
                    newBaddy.boundingBox = (xPos - Skeleton.sizeX,
                                            yPos - Skeleton.sizeY,
                                            xPos + Skeleton.sizeX,
                                            yPos + Skeleton.sizeY)
                    room.spritesInRoom.append(newBaddy)


    def addRoom(self, adjRoom, type, direction=NO_DIR):
        # print "Add Room Called"
        # assign the room new coords relative to the adjacent room 
        gridCoord = [0, 0]
        # if the new room is to the west of adjRoom
        if direction == WEST:
            gridCoord[x] = adjRoom.gridCoord[x] - 1
            gridCoord[y] = adjRoom.gridCoord[y]
        # if the new room is to the north of adjRoom
        elif direction == NORTH:
            gridCoord[x] = adjRoom.gridCoord[x]
            gridCoord[y] = adjRoom.gridCoord[y] - 1
        # if the new room is to the east of adjRoom
        elif direction == EAST:
            gridCoord[x] = adjRoom.gridCoord[x] + 1
            gridCoord[y] = adjRoom.gridCoord[y]
        # if the new room is to the south of adjRoom
        elif direction == SOUTH:
            gridCoord[x] = adjRoom.gridCoord[x]
            gridCoord[y] = adjRoom.gridCoord[y] + 1
        
        alreadyExists = False
        for room in self.rooms:
            if room.gridCoord == gridCoord:
                alreadyExists = True
        
        if not alreadyExists:
            # make the room
            newRoom = Room(direction, type, [None, None, None, None], gridCoord)
            newRoom.doors[opposite(direction)] = Door(opposite(direction))
            adjRoom.doors[direction] = Door(direction)
            # update pointers
            if direction != NO_DIR:
                adjRoom.adjRooms[direction] = newRoom
                newRoom.adjRooms[opposite(direction)] = adjRoom
            
            newRoom.roomId = len(Dungeon.floorKeys)
            room = r.randint(0, len(self.rooms) - 1)
            xPos = r.randint(Room.currentRoom.boundingBox[WEST] + Key.keyImg.width/2,
                            Room.currentRoom.boundingBox[EAST] - Key.keyImg.width/2)
            yPos = r.randint(Room.currentRoom.boundingBox[NORTH] + Key.keyImg.width/2,
                            Room.currentRoom.boundingBox[SOUTH] - Key.keyImg.width/2)
            newKey = Key(xPos, yPos, self.rooms[room])
            newRoom.rightKey = newKey
            Dungeon.floorKeys.append(newKey)
            self.rooms.append(newRoom)
            self.linkRooms(newRoom)
        
        return True if not alreadyExists else False
        
    def linkRooms(self, linkRoom):
        """ """
        for room in self.rooms:
            
            if room.gridCoord[x] == linkRoom.gridCoord[x]:
                # there is a room north of link room
                if room.gridCoord[y] == linkRoom.gridCoord[y] - 1:
                    room.adjRooms[SOUTH] = linkRoom
                    linkRoom.adjRooms[NORTH] = room
                # there is a room south of linkRoom
                elif room.gridCoord[y] == linkRoom.gridCoord[y] + 1:
                    room.adjRooms[NORTH] = linkRoom
                    linkRoom.adjRooms[SOUTH] = room
            if room.gridCoord[y] == linkRoom.gridCoord[y]:
                # there is a room west of link room
                if room.gridCoord[x] == linkRoom.gridCoord[x] - 1:
                    room.adjRooms[EAST] = linkRoom
                    linkRoom.adjRooms[WEST] = room
                # there is a room east of linkRoom
                elif room.gridCoord[x] == linkRoom.gridCoord[x] + 1:
                    room.adjRooms[WEST] = linkRoom
                    linkRoom.adjRooms[EAST] = room
                    

 
                    