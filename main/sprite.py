from util import SOUTH, x, y, boundBoxCheck


class Sprite(object):
    """Anything in this class should be able to:
       - test for collision between itself and another Sprite
       - draw itself at its location
       - face a direction
       - have a location"""

    # Class keeps track of the various sprites it's made
    allSprites = []

    # These ones automatically get moved each game update, based on their
    # velocity and time passed and stuff. Not all sprites do this ("walls"),
    # and it would be wasteful to add all those 0s to their positions, so we
    # just leave them out by design. NOTE: being in here means it MUST have a
    # updatePosition() method!
    autoMoveSprites = []

    def __init__(self, boundingBox, drawer, direction=SOUTH, location=(0, 0)):
        """boundingBox is a tuple of the form left, top, right, bottom.
        IMPORTANT NOTE: top here means "Processing visual top", so it's
        actually numerically lower than bottom.

        drawer is an outsourcing of drawing capability to some other object,
        probably a PImage or something similar.

        direction is one of WEST, EAST, SOUTH, NORTH, or other useful ones we
        might want to add later.

        location is a tuple containing x and y position - it should be in the
        visual center of the object."""
        self.boundingBox = boundingBox
        left, top, right, bottom = boundingBox
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.drawer = drawer
        self.direction = direction
        self.location = location

        # As mentioned above, the class keeps track of the stuff it's made so we
        # can easily draw all of them, update their positions, etc.
        Sprite.allSprites.append(self)

    def move(self, deltaX, deltaY):
        # Update location
        self.location = (self.location[x] + deltaX, self.location[y] + deltaY)

        # Update hitbox
        self.left += deltaX
        self.right += deltaX
        self.top += deltaY
        self.bottom += deltaY

    def draw(self):
        # Outsource drawing to some other object
        self.drawer.draw(self.location[x], self.location[y])

    def checkCollision(self, otherSprite):
        # Our left is to the left of their right
        return boundBoxCheck(self, otherSprite)


def drawAllSprites():
    for sprite in Sprite.allSprites:
        sprite.draw(sprite.location[x], sprite.location[y])