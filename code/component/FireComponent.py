import pygame
from common.Interfaces import IEntity
from manager.BulletManager import BulletManager


class FireComponent():
    def __init__(self, bulletID) -> None:
        self.entity:IEntity = self
        self.bulletID = bulletID

    def fire(self, pos:pygame.Vector2):
        angle = self.entity.getAngle()
        bulletEntity = BulletManager.getInstance().creatBulletEntity(self.bulletID, pos, angle)
        dir = pygame.Vector2(0, -1).rotate(-angle)
        if bulletEntity is None:
            print ("bullet is none")
        else:            
            bulletEntity.setDir(dir)

    def prepareDelete(self):
        self.entity = None
        