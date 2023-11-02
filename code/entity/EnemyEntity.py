import pygame
from common.Enums import EntityType, PriorityType, RenderCenterType
from common.info import EnemyInfo
from component.CollisionComponent import CollisionComponent
from component.HealthComponent import HealthComponent
from component.MoveComponent import MoveComponent
from component.PathFindComponent import PathFindComponent
from component.Renderer import RenderComponent, pygame
from entity.BaseEntity import BaseEntity
from entity.BulletEntity import BulletEntity
from entity.RenderEntity import AniEntity
from manager.BulletManager import BulletManager
from manager.Debugger import DebugType, Debugger
from manager.GameSetting import GameSetting


class EnemyEntity(AniEntity, MoveComponent, PathFindComponent, CollisionComponent, HealthComponent):
    __IMAGE_FORMAT = "./resource/enemy/{_type}"
    __distanceMin = None
    def __init__(self, name, enemyInfo:EnemyInfo, pos: pygame.Vector2) -> None:
        self.enemyInfo = enemyInfo
        resourcePath = EnemyEntity.__IMAGE_FORMAT.format(_type=enemyInfo.enemyType.name)
        AniEntity.__init__(self, name, pos, EntityType.Enemy, resourcePath, PriorityType.Second, scale=pygame.Vector2(enemyInfo.scale, enemyInfo.scale), renderCenter = RenderCenterType.Bottom)
        MoveComponent.__init__(self, self, enemyInfo.speed)
        PathFindComponent.__init__(self, self)
        HealthComponent.__init__(self, self, enemyInfo.hp, 40, 8, enemyInfo.hpBarOffset)

        rect = enemyInfo.collisionRect.copy()
        rect.center = pos
        if self.getRenderCenter() == RenderCenterType.Bottom:
            rect.bottom = pos.y
        CollisionComponent.__init__(self, self, rect, {EntityType.Bullet})
        
        if EnemyEntity.__distanceMin == None:
            EnemyEntity.__distanceMin = GameSetting.getFloat("Path", "DistanceMin")
    
    def prepareDelete(self):
        HealthComponent.prepareDelete(self)
        PathFindComponent.prepareDelete(self)
        CollisionComponent.prepareDelete(self)
        MoveComponent.prepareDelete(self)
        AniEntity.prepareDelete(self)
        self.enemyInfo = None
    
    def afterMove(self, delta):
        CollisionComponent.rotateCollisionRect(self, self.entity.getAngle())
        HealthComponent.updateHPBar(self)
    
    def onCollision(self, other:BaseEntity) -> bool:
        Debugger.print(f"onCollision : {self.name} -> {other.name}", DebugType.Info)
        self.getDamage(other)
        
    def getDamage(self, other:BaseEntity):
        if other.getType() == EntityType.Bullet:
            dir = other.getDir()
            bulletID = BulletEntity.getBulletID(other)
            bulletInfo = BulletManager.getBulletInfo(bulletID)
            damageInfo:tuple[int, bool] = bulletInfo.getDamage()
            movePos = dir * bulletInfo.getDamageRate(damageInfo[0])
            MoveComponent.setAddPos(self, movePos)
            BulletManager.getInstance().deleteBulletEntity(other)
            if HealthComponent.getDamage(self, damageInfo) == False:
                from manager.EnemyManger import EnemyManager
                EnemyManager.getInstance().deleteEnemyEntity(self)
    
    def setAngle(self, angle):
        super().setAngle(angle)
        CollisionComponent.rotateCollisionRect(self, angle)

    def postRender(self, delta) -> None:
        super().postRender(delta)
        MoveComponent.postRender(self, delta)
        CollisionComponent.postRender(self, delta)
        PathFindComponent.postRender(self, delta)

    def update(self, delta) -> None:
        super().update(delta)
        curTargetPos = PathFindComponent.getCurTargetPos(self)
        if curTargetPos != None:
            dir = curTargetPos - self.getPos()
            distanceToTargetPos = dir.magnitude()
            if distanceToTargetPos< EnemyEntity.__distanceMin:
                PathFindComponent.NextTarget(self)
            else:
                dir = dir.normalize()
                super().setDir(dir)
                RenderComponent.setFlip(self, (dir.x < 0))
        else:
            super ().setDir(pygame.Vector2(0, 0))
            from manager.EnemyManger import EnemyManager
            EnemyManager.getInstance().deleteEnemyEntity(self)