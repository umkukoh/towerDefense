import pygame
from common.MyColor import GREEN, RED1
from manager.Debugger import Debugger
from common.Enums import EntityType
from common.Interfaces import *
from manager.GameSetting import GameSetting

class BaseEntity(IEntity, IUpdate, IPostRender):
    __count = 0
    __screen = None
    __drawRect = False
    __drawPos = False
    
    def __init__(self, name:str, pos:pygame.Vector2, type:EntityType, scale = pygame.Vector2(1.0, 1.0), active = True, renderCenterType = RenderCenterType.Center) -> None:
        self.pendingDelete = False
        self.ID = BaseEntity.__count
        self.name = name
        self.scale = scale
        self.pos = pos
        self.type = type
        self.active = active
        self.angle = 0
        self.dir = pygame.Vector2(0.0, 0.0)
        self.renderCenterType = renderCenterType
        IEntity.__init__(self)
        IUpdate.__init__(self)
        IPostRender.__init__(self)
        
        if BaseEntity.__screen == None:
            BaseEntity.__screen = pygame.display.get_surface()
            
        if BaseEntity.__drawRect == False:
            BaseEntity.__drawRect = GameSetting.getBoolean("Debug", "Debugging") and GameSetting.getBoolean("Debug", "DrawRect")
        
        if BaseEntity.__drawPos == False:
            BaseEntity.__drawPos = GameSetting.getBoolean("Debug", "Debugging") and GameSetting.getBoolean("Debug", "DrawPos")

        BaseEntity.__count += 1

    def prepareDelete (self):
        IPostRender.prepareDelete(self)
        IUpdate.prepareDelete(self)
        IEntity.prepareDelete(self)
        self.pendingDelete = True
        
    def __del__(self):
        Debugger.print(f"Delete : {self.name}")

    def __str__(self):
        return self.name
    
    def IsPendingDelete(self) -> bool:
        return self.pendingDelete

    def update(self, delta) -> None:
        pass

    def getID(self) -> int:
        return self.ID
    
    def getName(self) -> str:
        return self.name
    
    def getScale(self) -> pygame.Vector2:
        return self.scale

    def setScale(self, scale: pygame.Vector2):
        self.scale = scale

    def getPos(self) -> pygame.Vector2:
        return self.pos
    
    def setPos(self, pos:pygame.Vector2):
        self.pos = pos

    def getType(self) -> EntityType:
        return self.type

    def getActive(self) -> bool:
        return self.active

    def setActive(self, active: bool):
        self.active = active

    def getAngle(self) -> float:
        return self.angle

    def setAngle(self, angle:float):
        self.angle = angle

    def setDir(self, dir:pygame.Vector2):
        self.dir = dir
        if self.dir.length() > 0.000001:
            if not self.dir.is_normalized():
                self.dir = self.dir.normalize()

    def getDir(self):
        return self.dir

    def postRender(self, delta) -> None:
        if BaseEntity.__drawRect == True:
            pygame.draw.rect(BaseEntity.__screen, GREEN, self.getRect(), 1)
        
        if BaseEntity.__drawPos == True:
            pygame.draw.circle(BaseEntity.__screen, RED1, self.getPos(), 3)
            
        return super().postRender(delta)
    
    def getRenderCenter(self) -> RenderCenterType:
        return self.renderCenterType
    
    
        

    