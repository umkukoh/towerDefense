
from common.Interfaces import IEntity
from entity.BaseEntity import BaseEntity
from entity.EnemyEntity import EnemyEntity
from entity.RenderEntity import RenderEntity
from manager.EnemyManger import EnemyManager
from manager.GameSetting import GameSetting


class RangeComponent():
    __rangeUnitSize = None
    __resource = "./resource/range.png"
    __rangeEntity = None
    def __init__(self, entity:IEntity, rangeRate:float) :
        self.entity:IEntity = entity
        self.target:RenderEntity = None
        
        if RangeComponent.__rangeUnitSize == None:
            RangeComponent.__rangeUnitSize = GameSetting.getInt("Turret", "RangeUnitSize")

        self.rangeRate = rangeRate
        self.range = RangeComponent.__rangeUnitSize * rangeRate

    def prepareDelete(self):
        self.entity = None
        self.target = None

    def getDistance(self, entity:IEntity) -> float:
        distance = entity.getPos() - self.entity.getPos()
        return distance.magnitude()
    
    def getValue(element:tuple[int, float]):
        return element[1]
    
    def getTarget (self) -> EnemyEntity:
        if self.target != None:
            if self.target.IsPendingDelete():
                self.target = None
            
            else:
                distance = self.getDistance(self.target)
                if distance < self.range:
                    return self.target
                else:
                    self.target = None
        
        distanceList = []
        enemyList:list[EnemyEntity] = EnemyManager.getInstance().getEnemyList()
        for enemy in enemyList:
            distance = self.getDistance(enemy)
            if distance < self.range:
                distanceList.append((enemy.getID(), distance))

        if len(distanceList) == 0:
            return None
        
        distanceList.sort(key=RangeComponent.getValue, reverse=False)
        targetID = distanceList.pop(0)[0]
        for enemy in enemyList:
            if enemy.getID() == targetID:
                self.target = enemy
                return self.target
        
        return None
            