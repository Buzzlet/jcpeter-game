from combatSprite import CombatSprite
from animation import Animation
from util import x, y, NO_DIR, WEST, EAST, NORTH, SOUTH, directionSigns, boundBoxCheck, opposite, inZone, IDLE, WALKING, ATTACKING, JUMPING
from room import Room

class Skeleton(CombatSprite):
    
    skeleAniPrefix = 'skele'
    skeleAniType = '.png'
    skeleNumFrames = 2
    
    skeleWalkPrefix = 'skeleWalk'
    skeleWalkType = '.png'
    skeleWalkNumFrames = 7
    
    skeleAttackPrefix = 'skeleAttack'
    skeleAttackType = '.png'
    skeleAttackNumFrames = 0
    
    skeleJumpPrefix = 'skeleJump'
    skeleJumpType = '.png'
    skeleJumpNumFrames = 0
    
    # half of the bounding box (smaller than animation size)
    sizeX = 15
    sizeY = 25
    
    bboxLeniency = 0
    
    def __init__(self, initPos=(400, 400)):
        super(Skeleton, self).__init__((initPos[x] - Skeleton.sizeX,
                                        initPos[y] - Skeleton.sizeY,
                                        initPos[x] + Skeleton.sizeX,
                                        initPos[y] + Skeleton.sizeY), #boundingBox
                                        self, # drawer
                                        initPos, #location
                                        (0,0), #velocity
                                        .15, #speed
                                        5, #damage
                                        30, #maxHealth
                                        30, #currentHealth
                                        False) #moving
        
        self.animations =[Animation(Skeleton.skeleAniPrefix,
                                    Skeleton.skeleAniType,
                                    Skeleton.skeleNumFrames, 6),
                          Animation(Skeleton.skeleWalkPrefix,
                                    Skeleton.skeleWalkType,
                                    Skeleton.skeleWalkNumFrames),
                          Animation(Skeleton.skeleAttackPrefix,
                                    Skeleton.skeleAttackType,
                                    Skeleton.skeleAttackNumFrames, 10),
                          Animation(Skeleton.skeleJumpPrefix,
                                    Skeleton.skeleJumpType,
                                    Skeleton.skeleJumpNumFrames, 10)]
        self.currentAnimation = self.animations[IDLE]

    def draw(self, x, y):
        if self in Room.currentRoom.spritesInRoom:
            
            #TODO: Get some placeholder skeleton animations
            if self.velocity[0] >= 0:
                self.currentAnimation.display(x - Skeleton.sizeX, y - Skeleton.sizeY)
            else:
                self.currentAnimation.flipXDisplay(x - Skeleton.sizeX, y - Skeleton.sizeY)
        
            if not self.moving:
                self.currentAnimation = self.animations[IDLE]
            else:
                self.currentAnimation = self.animations[WALKING]
            
    def movingChecks(self, timePassed):
        pass
        