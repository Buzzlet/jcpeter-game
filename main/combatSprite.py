from sprite import Sprite
from room import Room
from util import x, y, NO_DIR, WEST, EAST, NORTH, SOUTH, directionSigns, boundBoxCheck, opposite, inZone

class CombatSprite(Sprite):
    def __init__(self, boundingBox, drawer, location, velocity, speed, damage, maxHealth, currentHealth, moving):
        super(CombatSprite, self).__init__(boundingBox, drawer, location=location)
        
        self.velocity = velocity
        self.speed = speed
        self.damage = damage
        self.maxHealth = maxHealth
        self.currentHealth = currentHealth
        self.moving = moving
        Sprite.autoMoveSprites.append(drawer)
        
    
    def validMove(self, timePassed):
        dx = self.velocity[x] * timePassed
        dy = self.velocity[y] * timePassed
        left, top, right, bottom = self.boundingBox
        left += self.drawer.bboxLeniency
        right -= self.drawer.bboxLeniency
        top += self.drawer.bboxLeniency
        bottom -= self.drawer.bboxLeniency
        futureLeft = left + dx
        futureRight = right + dx
        futureTop = top + dy
        futureBottom = bottom + dy
    
        moveX = 0
        moveY = 0
        # no CombatSprites can leave the bounding box of the room
        if inZone((futureLeft, top, futureRight, bottom), Room.currentRoom.boundingBox):
            if inZone((futureLeft, futureTop, futureRight, futureBottom), Room.currentRoom.boundingBox):
                moveX = dx
                moveY = dy
            else:
                moveX = dx
        elif inZone((left, futureTop, right, futureBottom), Room.currentRoom.boundingBox):
            moveY = dy
        return (moveX, moveY)
            
    
    def updatePosition(self, timePassed):
        dx = self.velocity[x] * timePassed
        dy = self.velocity[y] * timePassed
        if abs(dy) > 0 or abs(dx) > 0:
            self.moving = True
        else:
            self.moving = False
            
        moveX, moveY = self.validMove(timePassed)
        self.drawer.movingChecks(timePassed)
        self.move(moveX, moveY)
        
        
        
    def attackBox(self):
        """Gives the sides of the rectangle that is the attack box... in the
        same form as the boundingBox used by Sprite - that is, left, top,
        right, bottom"""
        if self.direction == WEST:
            return (self.location[x] - self.drawer.sizeX - self.drawer.attackSize[y],
                    self.location[y] - self.drawer.attackSize[x] / 2,
                    self.location[x] - self.drawer.sizeX,
                    self.location[y] + self.drawer.attackSize[x] / 2,)
            
        elif self.direction == NORTH:
            return (self.location[x] - self.drawer.attackSize[x] / 2,
                    self.location[y] - self.drawer.sizeY - self.drawer.attackSize[y],
                    self.location[x] + self.drawer.attackSize[x] / 2,
                    self.location[y] - self.drawer.sizeY)
            
        elif self.direction == EAST:
            return (self.location[x] + self.drawer.sizeX,
                    self.location[y] - self.drawer.attackSize[x] / 2,
                    self.location[x] + self.drawer.sizeX + self.drawer.attackSize[y],
                    self.location[y] + self.drawer.attackSize[x] / 2)
    
        elif self.direction == SOUTH:
            return (self.location[x] - self.drawer.attackSize[x] / 2,
                    self.location[y] + self.drawer.sizeY,
                    self.location[x] + self.drawer.attackSize[x] / 2,
                    self.location[y] + self.drawer.sizeY + self.drawer.attackSize[y])
    
    
    def setWalkY(self, flag):
        if flag is None:
            self.velocity = self.velocity[x], 0
        else:
            self.velocity = self.velocity[x], directionSigns[flag] * self.speed
            self.direction = flag


    def setWalkX(self, flag):
        if flag is None:
            self.velocity = 0, self.velocity[y]
        else:
            self.velocity = directionSigns[flag] * self.speed, self.velocity[y]
            self.direction = flag
    
        
def updatePositions(timePassed):
    for sprite in Sprite.autoMoveSprites:
        if sprite in Room.currentRoom.spritesInRoom:
            #print(type(sprite))
            sprite.updatePosition(timePassed)