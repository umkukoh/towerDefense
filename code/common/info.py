import random
import pygame
from common.Enums import EnemyType
from manager.GameSetting import GameSetting

class TurretInfo():
    __uiPathFormat = "#{resource}_{level}"
    __resourceFormat = "./resource/turret/{resource}_{level}.png"
    def __init__(self, id:str, resource:str, level:int,
                 cost:int, bulletID:str, reloadTime:int, rangeRate:float,
                 firePosList:list[tuple[int, int]]) -> None:
        self.id = id
        self.resource = resource
        self.level = level
        self.cost = cost
        self.bulletID = bulletID
        self.reloadTime = reloadTime
        self.rangeRate = rangeRate
        self.firePosList = firePosList

    def getUIResource(self) -> str:
        return TurretInfo.__uiPathFormat.format(resource=self.resource,
                                                 level=self.level)
    
    def getSpriteResource(self) -> str:
        return TurretInfo.__resourceFormat.format(resource=self.resource,
                                                    level=self.level)
class EnemyCreatInfo():
    def __init__(self, data:tuple[int, str], addStartTime:int) -> None:
        self.time = data[0] + addStartTime
        self.enemyType = data[1]

class WaveInfo():
    def __init__(self, startTime:int, endTime:int, enemyList:list[str]) -> None:
        self.startTime = startTime
        self.endTime = endTime
        self.enemyList:list[EnemyCreatInfo] = [EnemyCreatInfo(eval(element), startTime) for element in enemyList]
    
    def getEnemyList(self) -> list[EnemyCreatInfo]:
        return self.enemyList
    
    def getStartTime(self) -> int:
        return self.startTime
    
    def getEndTime(self) -> int:
        return self.endTime

class StageInfo():
    def __init__(self, id:int, name:str, startPos:str, endPos:str, gold:int, hp:int, \
                turretSlots:list[str], paths:list[str], waves:list[dict]) -> None:
        self.id = id
        self.name = name
        self.startPos = eval(startPos)
        self.endPos = eval(endPos)
        self.gold = gold
        self.hp = hp
        self.turretSlots:list[tuple[int, int]] = [eval(element)for element in turretSlots]
        self.paths:list[tuple[int, int]] = [eval(element) for element in paths]
        self.waves:list[WaveInfo] = [WaveInfo(**element) for element in waves]
        self.mapData:list[list[str]] = []

        maxX = GameSetting.getInt("Tile", "TileMaxIndexX")
        maxY = GameSetting.getInt("Tile", "TileMaxIndexY")

        for y in range(maxY):
            row = []
            for x in range(maxX):
                data = 0
                index = str((x,y)).replace(" ","")
                if index in turretSlots:
                    data = 1
                elif index in paths:
                    data = 2

                row.append(data)
            
            self.mapData.append(row)
    
    def getName(self) -> str:
        return self.name

    def getEndPos(self) -> tuple[int, int]:
        return self.endPos
    
    def getMapData(self) -> list[list[str]]:
        return self.mapData.copy()
    
    def getPathData(self) -> list[tuple[int, int]]:
        return self.paths
    
    def getAllWaves(self) -> list[WaveInfo]:
        return self.waves
    
    def getWaveInfoData(self, index:int) -> WaveInfo:
        if index >= len(self.waves):
            return None
        
        return self.waves[index]
    
class BulletInfo():
    __resourceFormat = "./resource/bullet/{resource}.png"
    def __init__(self, id, resource, speed:int, maxDamage:int, minDamage:int, criticalPercent:int, criticalDamageRate:float, collisionRect:dict) -> None:
        self.id = id
        self.resource = resource
        self.speed = speed
        self.maxDamage = maxDamage
        self.minDamage = minDamage
        self.criticalPercent = criticalPercent
        self.criticalDamageRate = criticalDamageRate
        self.collisionRect = pygame.Rect(collisionRect["left"], collisionRect["top"],collisionRect["width"], collisionRect["height"])
    
    def getDamageRate(self, damage) -> float:
        return damage * 0.5
    
    def getDamage(self) -> tuple[int, bool]:
        damage = random.randint(self.minDamage,self.maxDamage)
        critical = random.randint(0,100)
        isCritical = critical <= self.criticalPercent
        if isCritical:
            damage *= self.criticalDamageRate
        return (int(damage), isCritical)
    
class EnemyInfo():
        def __init__(self, enemyType:str, scale:float, speed:float, damage:int, \
                     hp:float, reward:int, hpBarOffset:str, collisionRect:dict) -> None:
            self.enemyType = EnemyType[enemyType]
            self.scale = scale
            self.speed = speed
            self.damage = damage
            self.hp = hp
            self.hpBarOffset = eval(hpBarOffset)
            self.reward = reward
            self.collisionRect = pygame.Rect(collisionRect["left"], collisionRect["top"], \
                                             collisionRect["width"], collisionRect["height"])