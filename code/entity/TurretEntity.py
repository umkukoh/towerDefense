import pygame
from common.Enums import EntityType, PriorityType
from common.Interfaces import IEntity
from common.info import BulletInfo, TurretInfo
from component.FireComponent import FireComponent
from component.RangeComponent import RangeComponent
from entity.RenderEntity import RenderEntity
from manager.BulletManager import BulletManager
from manager.GameSetting import GameSetting


class TurretEntity(RenderEntity, RangeComponent, FireComponent):
    __scale= 0

    def __init__(self, tileIndex:tuple[int, int], turretInfo:TurretInfo) -> None:
        name = str(f"{tileIndex}{turretInfo.resource}_{turretInfo.level}")
        pos = pygame.Vector2(tileIndex[0] + 0.5, tileIndex[1] + 0.5) * GameSetting.getInt("Tile", "Size")
        if TurretEntity.__scale == 0:
            TurretEntity.__scale = GameSetting.getFloat("Turret", "Scale")

        scale = pygame.Vector2(1, 1) * TurretEntity.__scale
        RenderEntity.__init__(self, name, pos, EntityType.Turret, turretInfo.getSpriteResource(), PriorityType.Second, scale)
        FireComponent.__init__(self, turretInfo.bulletID )
        RangeComponent.__init__(self, self, turretInfo.rangeRate )
        self.level = turretInfo.level

        self.originFirePosList = []
        for element in turretInfo.firePosList:
            firePos = eval(element) + self.pos
            self.originFirePosList.append(pygame.Vector2(firePos[0], firePos[1]))
        self.curFirePosList:list[pygame.Vector2] = self.originFirePosList.copy()
        self.reloadTime = turretInfo.reloadTime
        self.curDelayForFire = self.reloadTime
        self.selected = False

    def prepareDelete(self):
        RenderEntity.prepareDelete(self)


    def setAngle(self, angle):
        super().setAngle(angle)
        self.curFirePosList = [TurretEntity.rotateFirePos(firePos, self.pos, angle) for firePos in self.originFirePosList]

    def rotateFirePos(firePos:pygame.Vector2, center:pygame.Vector2, angle) -> pygame.Vector2:
        dirToDestFirePos = firePos - center
        length = dirToDestFirePos.length()
        dirToDestFirePos = dirToDestFirePos.normalize()
        dirToDestFirePos = dirToDestFirePos.rotate(-angle)
        return center + dirToDestFirePos * length 

 
    def update(self, delta:int) -> None:
        # mousePos = pygame.mouse.get_pos() 
        # mousePos = pygame.Vector2(mousePos)
        # myPos = self.getPos()
        # disVec = mousePos - myPos
        # dir = disVec.normalize()
        # angle = dir.angle_to(pygame.Vector2(0,-1))
        # self.setAngle(angle)

        # buttons = pygame.mouse.get_pressed()
        # if buttons[0]:
        #     self.curDelayForFire += delta
        #     if self.curDelayForFire >= self.reloadTime:
        #         self.curDelayForFire = 0
        #         for element in self.curFirePosList:
        #             self.fire(element)
        # else:
        #     self.curDelayForFire += delta
        target = RangeComponent.getTarget(self)
        self.curDelayForFire += delta
        if self.curDelayForFire >= self.reloadTime:
            target = RangeComponent.getTarget(self)
            if target != None:
                self.curDelayForFire = 0
                bulletInfo = BulletManager.getBulletInfo(self.bulletID)
                targetPos = target.getCollisionCenter()
                vecToTarget = targetPos - self.getPos()
                distance = vecToTarget.magnitude()
                estimateTime = distance / bulletInfo.speed
                
                targetDirAndSpeed = target.getDir() * target.getSpeed()
                targetPos += targetDirAndSpeed * estimateTime
                
                dirToTarget = targetPos - self.getPos()
                dirToTarget = dirToTarget.normalize()
                angle = dirToTarget.angle_to(pygame.Vector2(0,-1))
                self.setAngle(angle)
                for element in self.curFirePosList:
                    self.fire(element)

            
            
        
    
        


        