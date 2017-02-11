from room import Room
from sprite import Sprite
from util import x, y, WEST, EAST, NORTH, SOUTH, directionSigns, boundBoxCheck
# Screw you, Python people, you just wasted 3 hours of my life because main.py
# produces a module named "__main__" instead of a module named "main"...
import __main__


class Character(Sprite):
    radius = 15
    # width, height - note, these are the dimensions for when it is facing
    # north/south.
    attackSize = 200, 100

    def __init__(self, initPos=(350, 350)):
        super(Character, self).__init__((initPos[x] - Character.radius,
                                         initPos[y] - Character.radius,
                                         initPos[x] + Character.radius,
                                         initPos[y] + Character.radius),
                                        self, location=initPos)
        self.velocity = 0, 0
        self.speed = .75
        self.damage = 5
        self.maxHealth = 100
        self.currentHealth = 100
        Sprite.autoMoveSprites.append(self)

    def attackBox(self):
        """Gives the sides of the rectangle that is the attack box... in the
        same form as the boundingBox used by Sprite - that is, left, top, right,
        bottom"""
        if self.direction == WEST:
            return (self.location[x] - Character.radius -
                    Character.attackSize[y],
                    self.location[y] - Character.attackSize[x] / 2,
                    self.location[x] - Character.radius,
                    self.location[y] + Character.attackSize[x] / 2,)

        elif self.direction == EAST:
            return (self.location[x] + Character.radius,
                    self.location[y] - Character.attackSize[x] / 2,
                    self.location[x] + Character.radius +
                    Character.attackSize[y],
                    self.location[y] + Character.attackSize[x] / 2)

        elif self.direction == SOUTH:
            return (self.location[x] - Character.attackSize[x] / 2,
                    self.location[y] + Character.radius,
                    self.location[x] + Character.attackSize[x] / 2,
                    self.location[y] + Character.radius +
                    Character.attackSize[y])

        elif self.direction == NORTH:
            return (self.location[x] - Character.attackSize[x] / 2,
                    self.location[y] - Character.radius -
                    Character.attackSize[y],
                    self.location[x] + Character.attackSize[x] / 2,
                    self.location[y] - Character.radius)

    def isAttacking(self):
        return __main__.key_states.get(' ')
    
    def triggerDoorToggle(self, triggerZone, enterDoor, function, arg1=None):
        if(enterDoor and boundBoxCheck(triggerZone, (self.left, self.top, self.right, self.bottom))):
            __main__.enterDoor = False
            function(arg1)

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

    def draw(self, x, y):
        ellipse(x, y, 2*Character.radius, 2*Character.radius)
        # Drawing the attack box just to give us an idea of what it's like
        if self.isAttacking():
            left, top, right, bottom = self.attackBox()
            rect(left, top, right - left, bottom - top)

    def updatePosition(self, timePassed):
        dx = self.velocity[x] * timePassed
        dy = self.velocity[y] * timePassed
        futureLeft = self.left + dx
        futureRight = self.right + dx
        futureTop = self.top + dy
        futureBottom = self.bottom + dy
        if boundBoxCheck(Room.currentRoom.boundingBox, 
                         (futureLeft,
                          self.top,
                          futureRight,
                          self.bottom)):
           if boundBoxCheck(Room.currentRoom.boundingBox,
                           (futureLeft,
                            futureTop,
                            futureRight,
                            futureBottom)):
               self.move(dx, dy)
           else:
               self.move(dx, 0)
        elif boundBoxCheck(Room.currentRoom.boundingBox,
                          (self.left,
                           futureTop,
                           self.right,
                           futureBottom)):
           self.move(0, dy)


def updatePositions(timePassed):
    for sprite in Sprite.autoMoveSprites:
        sprite.updatePosition(timePassed)