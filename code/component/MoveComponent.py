import pygame
from common.Interfaces import IEntity, IMove
from manager.GameSetting import GameSetting


class MoveComponent(IMove):
    __drawMovement = False

    def __init__(self, entity:IEntity, speed:float) -> None:
        self.entity = entity
        self.lastPosition = self.entity.getPos()
        self.speed = speed
        self.screen = pygame.display.get_surface()
        self.trails = []
        self.addPos = None

        MoveComponent.__drawMovement = GameSetting.getBoolean("Debug", "Debugging") \
            and GameSetting.getBoolean("Debug", "DrawMovement")
        IMove.__init__(self)

    def prepareDelete(self):
        IMove.prepareDelete(self)
        self.entity = None
    
    def getLastPos(self) -> pygame.Vector2:
        return self.lastPosition
    
    def getSpeed(self) -> float:
        return self.speed
    
    def setAddPos(self, pos:pygame.Vector2):
        self.addPos = pos

    def preMove(self, delta):
        if self.addPos != None:
            self.entity.setPos(self.entity.getPos() + self.addPos)
            self.addPos = None
    
    def afterMove(self, delta):
        pass

    def move(self, delta):
        if self.entity.getDir().magnitude() == 0.0:
            return
        
        self.preMove(delta)
        self.lastPosition = self.entity.getPos()
        self.trails.insert(0, self.lastPosition)
        if len(self.trails) > 20:
            self.trails = self.trails[0:20]

        deltaVector = self.entity.getDir() * self.speed * delta
        self.entity.setPos(self.lastPosition + deltaVector)
        self.afterMove(delta)

    def postRender(self, delta) -> None:
        if MoveComponent.__drawMovement == False:
            return
        
        start = self.entity.getPos()
        for lastPos in self.trails:
            pygame.draw.line(self.screen, (255, 100, 100), start, lastPos)
            start = lastPos