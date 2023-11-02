from abc import abstractmethod
import math
import pygame
from common.Enums import BoxCollisionArea, RenderCenterType
from common.MyColor import BLUE

from entity.BaseEntity import BaseEntity
from common.Interfaces import ICollision, IEntity
from manager.Debugger import Debugger
from manager.GameSetting import GameSetting

def rotatePos(pos:tuple[int, int], center:tuple[int, int], angle) -> tuple[int, int]:
    theta = -math.radians(angle)
    
    x = (pos[0] - center[0]) * math.cos(theta) - (pos[1] - center[1]) * math.sin(theta) + center[0]
    y = (pos[0] - center[0]) * math.sin(theta) + (pos[1] - center[1]) * math.cos(theta) + center[1]
    return (x, y)

def collideLineLine(l1_p1, l1_p2, l2_p1, l2_p2) -> bool:
    P = pygame.Vector2(*l1_p1)
    linel_vec = pygame.Vector2(*l1_p2) - P
    R = linel_vec.normalize()
    Q = pygame.Vector2(*l2_p1)
    line2_vec = pygame.Vector2(*l2_p2) - Q
    S = line2_vec.normalize()
    
    RNV = pygame.Vector2(R[1], -R[0])
    SNV = pygame.Vector2(S[1], -S[0])
    RdotSVN = R.dot(SNV)
    if RdotSVN == 0:
        return False
    
    QP = Q - P
    t = QP.dot(SNV) / RdotSVN
    u = QP.dot(RNV) / RdotSVN
    
    return t > 0 and u > 0 and t*t < linel_vec.magnitude_squared () and u*u < line2_vec.magnitude_squared()

def collidePolygon(pointList0:list[tuple[int,int]], pointList1:list[tuple[int, int]]):
    for j in range(len(pointList1)):
        for i in range(len(pointList0)):
            start0= i 
            if i == len(pointList0) - 1:
                end0 = 0
            else:
                end0 = i + 1
                
            start1 = j
            if j == len(pointList1) - 1:
                end1 = 0
            else:
                end1 = j + 1 
                
            if collideLineLine (pointList0[start0], pointList0[end0], pointList1[start1], pointList1[end1]):
                return True
    
    return False

class CollisionComponent(ICollision):
    __drawCollision = None
    def __init__(self, entity:BaseEntity, collisionRect:pygame.Rect, checkSet:set) -> None:
        ICollision.__init__(self, entity.getType())
        self.entity = entity
        self.originCollisionRectVertices = [collisionRect.topleft, collisionRect.bottomleft, collisionRect.bottomright, collisionRect.topright]
        self.collisionRectVerticles = self.originCollisionRectVertices.copy()
        self.checkSet = checkSet
        self.screen = pygame.display.get_surface()
        self.collisionRect = collisionRect
        
        if CollisionComponent.__drawCollision == None:
            CollisionComponent.__drawCollision = GameSetting.getBoolean("Debug", "Debugging") and GameSetting.getBoolean("Debug", "DrawCollision")
    
    def prepareDelete(self) :
        self.entity = None
        self.screen = None
        super().prepareDelete()
        
    def getCollisionPoint(selfRect:pygame.Rect, otherRect:pygame.Rect) -> BoxCollisionArea:
        flag = 0b0000
        if otherRect.collidepoint(selfRect.topleft):
            flag |= BoxCollisionArea.Top_Left
        
        if otherRect.collidepoint(selfRect.topright):
            flag |= BoxCollisionArea.Top_Right
            
        if otherRect.collidepoint(selfRect.bottomleft):
            flag |= BoxCollisionArea.Bottom_Left
            
        if otherRect.collidepoint(selfRect.bottomright):
            flag |= BoxCollisionArea.Bottom_Right
        
        return flag
    
    def checkCollision(self):
        selfCollisionRectVerticles = self.getCollisionRectVertices()
        _dict = ICollision.getCandidate(self.checkSet)
        
        for entityType, collisionList in _dict.items():
            rectDict:dict[IEntity, list[tuple[int,int]]] = {element.entity : element.getCollisionRectVertices() for element in collisionList}
            for otherEntity, otherRectVerticles in rectDict.items():
                if collidePolygon(selfCollisionRectVerticles, otherRectVerticles):
                    if CollisionComponent.__drawCollision:
                        Debugger.print(f"checkCollision true : {self.entity.getName} -> {otherEntity.getName()}")
                        
                    self.onCollision(otherEntity)
    
    def rotateCollisionRect(self, angle):
        center = (self.entity.getPos().x, self.entity.getPos().y)
        
        for i in range(len(self.collisionRectVerticles)):
            self.collisionRectVerticles[i] = rotatePos(self.originCollisionRectVertices[i], center, angle)
            
    def __updateOriginCollisionRect(self, pos:pygame.Vector2):
        self.collisionRect.center = (int(pos.x), int(pos.y))
        if self.entity.getRenderCenter() == RenderCenterType.Bottom:
            self.collisionRect.bottom = int(pos.y)
        self.originCollisionRectVertices = [self.collisionRect.topleft, self.collisionRect.bottomleft, self.collisionRect.bottomright, self.collisionRect.topright]
        
    def getCollisionCenter(self) -> pygame.Vector2:
        return pygame.Vector2(self.collisionRect.center[0], self.collisionRect.center[1])

    def updateCollision(self):
        self.__updateOriginCollisionRect(self.entity.getPos())
        self.rotateCollisionRect(self.entity.getAngle())
        
    def getCollisionRectVertices(self) -> list[tuple[int, int]]:
        return self.collisionRectVerticles.copy()
    
    def getCollisionRect(self) -> pygame.Rect:
        return self.collisionRect
    
    def setCollisionRect(self, collisionRect:pygame.Rect):
        self.collisionRect = collisionRect
        
    def postRender(self, delta) -> None:
        if CollisionComponent.__drawCollision == False:
            return
        
        pygame.draw.lines(self.screen, BLUE, True, self.collisionRectVerticles, 1)
        
    @abstractmethod
    def onCollision(self, other:BaseEntity) -> bool:
        pass 
        
    
            
    