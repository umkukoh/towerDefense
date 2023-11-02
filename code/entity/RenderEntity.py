import pygame
from common.MyColor import PINK, WHITE
from entity.BaseEntity import BaseEntity
from component.Renderer import *

class RenderEntity(BaseEntity, RenderComponent):
    def __init__(self, name, pos:pygame.Vector2, entityType, resource, priority, scale=pygame.Vector2(1,1), active=True, renderCenter:RenderCenterType = RenderCenterType.Center) -> None:
        BaseEntity.__init__(self, name, pos, entityType, scale, active, renderCenter)
        RenderComponent.__init__(self, self, resource, priority)

    def prepareDelete(self):
        RenderComponent.prepareDelete(self)
        BaseEntity.prepareDelete(self)

    def setAngle(self, angle: float):
        BaseEntity.setAngle(self, angle)
        RenderComponent.rotate(self, angle)

    def setScale(self, scale: pygame.Vector2):
        RenderComponent.updateResource(self)

    def postRender(self, delta) -> None:
        RenderComponent.renderRect(self)

class AniEntity(BaseEntity, AnimationComponent):
    def __init__(self, name: str, pos:pygame.Vector2, entityType, resourcePath, priority, scale=pygame.Vector2(1,1), active=True, renderCenter : RenderCenterType = RenderCenterType.Center ) -> None:
        BaseEntity.__init__(self, name, pos, entityType, scale, active, renderCenter)
        AnimationComponent.__init__(self, self, resourcePath, priority)
    
    def prepareDelete(self):
        AnimationComponent.prepareDelete(self)
        BaseEntity.prepareDelete(self)
    
    # override
    def setAngle(self, angle):
        BaseEntity.setAngle(self, angle)
        AnimationComponent.rotate(self, angle)

    def update(self, delta) -> None:
        BaseEntity.update(self, delta)
        AnimationComponent.updateAnim(self, delta)
        