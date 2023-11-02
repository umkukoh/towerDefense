import pygame
import os

from common.Interfaces import *
from common.Enums import *
from common.Interfaces import IEntity
from common.MyColor import *
from common.MyColor import WHITE
from manager.Debugger import Debugger
from manager.ResourceManager import ResourceManager

class RenderComponent(IRender):

    def __init__(self, entity:IEntity, resourcePath:str, priority, color = WHITE) -> None:
        IRender.__init__(self, priority)
        self.entity = entity
        self.screen = None
        self.resourcePath = ""
        self.originResource = None
        self.resource = None
        self.rect:pygame.Rect = None
        self.size = (0, 0)
        self.color = color
        self.flipX = False
        self.flipY = False
        self.setResource(resourcePath)

    def render(self):
        if self.screen == None:
            self.screen = pygame.display.get_surface()

        self.screen.blit(self.resource, self.getRect())

    def getRenderSize(self) -> tuple:
        scale = self.entity.getScale()
        return (self.size[0] * scale[0], self.size[1] * scale[1])

    def getRenderPos(self) -> tuple:
        pos = self.entity.getPos()
        scale = self.entity.getScale()
        return (pos[0] - self.size[0] * scale[0] * 0.5, pos[1] - self.size[1] * 0.5)

    def getRect(self) -> pygame.Rect:
        self.rect.center = self.entity.getPos()
        if self.entity.getRenderCenter() == RenderCenterType.Bottom:
            self.rect.bottom = self.entity.getPos().y
            
        return self.rect

    def updateResource(self):
        self.originResource = ResourceManager.GetResource(self.resourcePath, ResourceType.image)
        self.size = self.originResource.get_size()
        self.originResource = pygame.transform.flip(self.originResource, self.flipX, self.flipY)
        self.originResource = pygame.transform.scale(self.originResource, self.getRenderSize())
        self.resource = self.originResource
        self.rect = self.resource.get_rect()

    def setFlip(self, flipX:bool = False, flipY:bool = False):
        if self.flipX == flipX and self.flipY == flipY:
            return
        
        self.flipX = flipX
        self.flipY = flipY
        self.updateResource()

    def setResource(self, resourcePath:str):
        if self.resource != None:
            self.resource = None

        self.resourcePath = resourcePath

        if len(resourcePath) > 0:
            self.updateResource()
        else:
            self.resource = pygame.surface.Surface(self.size)
            self.resource.fill(self.color)

    # 0~255
    def setAlpha(self, alpha):
        self.resource.set_alpha(alpha)

    def rotate(self, angle):
        center = self.rect.center
        self.resource = pygame.transform.rotate(self.originResource, angle)
        self.rect = self.resource.get_rect()
        self.rect.center = center
    
    def getResourceSize(self) -> tuple[int, int]:
        return self.size

    def renderRect(self):
        if self.screen == None:
            self.screen = pygame.display.get_surface()

        pygame.draw.rect(self.screen, BLUE, self.getRect(), 1)

class AnimationComponent(RenderComponent):
    
    def __init__(self, entity: IEntity, resourcePath: str, priority) -> None:
        self.resourceList = self.__getResourceList(resourcePath)
        for resource in self.resourceList:
            ResourceManager.GetResource(resource)

        self.resourceCount = max(1, len(self.resourceList))
        self.imageIndex = 0
        self.curDelta = 0
        self.updateDelta = 1000 / self.resourceCount
        RenderComponent.__init__(self, entity, self.resourceList[0], priority)

    def prepareDelete(self):
        self.resourceList.clear()
        super().prepareDelete()

    def __getResourceList(self, path) -> list:
        files:list[str] = os.listdir(path)
        files = [f"{path}/{file}" for file in files if file.endswith(".png")]
        files.sort()

        return files
    
    def updateAnim(self, delta) -> None:
        if self.curDelta >= self.updateDelta:
            self.imageIndex += 1
            
            if self.imageIndex >= self.resourceCount:
                self.imageIndex = 0

            self.setResource(self.resourceList[self.imageIndex])
            angle = self.entity.getAngle()
            self.rotate(angle)
            self.curDelta -= self.updateDelta
        else:
            self.curDelta += delta
            
    