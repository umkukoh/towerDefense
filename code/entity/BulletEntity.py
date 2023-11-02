from common.Enums import EntityType, PriorityType
from common.info import BulletInfo
from component.CollisionComponent import CollisionComponent
from component.MoveComponent import MoveComponent
from entity.BaseEntity import BaseEntity
from entity.RenderEntity import RenderEntity


class BulletEntity(RenderEntity, MoveComponent, CollisionComponent):
    __resourceFormat = "./resource/bullet/{_ID}.png"
    __count = 0
    def __init__(self, bulletInfo:BulletInfo, pos, angle:float = 0.0) -> None:
        resource = BulletEntity.__resourceFormat.format(_ID=bulletInfo.id)
        name = f"{BulletEntity.__name__}_{BulletEntity.__count}"
        self.speed = bulletInfo.speed
        RenderEntity.__init__(self, name, pos, EntityType.Bullet, resource, PriorityType.Third)
        MoveComponent.__init__(self, self, self.speed)
        
        rect = bulletInfo.collisionRect.copy()
        rect.center = pos
        CollisionComponent.__init__(self, self, rect, {})
        
        self.setAngle(angle)
        self.bulletID = bulletInfo.id
        BulletEntity.__count += 1

    def prepareDelete(self):
        CollisionComponent.prepareDelete(self)
        MoveComponent.prepareDelete(self)
        RenderEntity.prepareDelete(self)
        
    
    def postRender(self, delta) -> None:
        RenderEntity.postRender(self, delta)
        MoveComponent.postRender(self, delta)
        CollisionComponent.postRender(self, delta)

    def setAngle(self, angle):
        super().setAngle(angle)
        CollisionComponent.rotateCollisionRect(self, angle)

    def onCollision(self, other:BaseEntity) -> bool:
        pass 

    def getBulletID(self) -> str:
        return self.bulletID
    