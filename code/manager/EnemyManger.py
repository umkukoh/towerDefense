import json

import pygame
from common.Enums import GameEvent
from common.Interfaces import IEvent, IUpdate
from common.info import EnemyInfo
from entity.EnemyEntity import EnemyEntity
from manager.Debugger import Debugger


class EnemyManager(IUpdate):
    # class EnemyManager(IUpdate, IEvent):
    __instance = None

    def __init__(self) -> None:
        if EnemyManager.__instance != None:
            return
        
        EnemyManager.__instance = self
        self.enemyInfoDict = self.__loadEnemyInfo("./data/enemy.json")
        self.enemyCount = 0
        self.enemyList:list[EnemyEntity] = []
        self.pendingList:list[EnemyEntity] = []

        IUpdate.__init__(self)
        # IEvent.__init__(self, {GameEvent.GameOver})

    def getInstance():
        return EnemyManager.__instance
    
    def __loadEnemyInfo(self, jsonPath) -> dict[str, EnemyInfo]:
        enemyInfoDict = {}
        file = open(jsonPath)
        if not file is None:
            data = json.load(file)
        
        for element in data["enemyList"]:
            enemyType = element["enemyType"]
            enemyInfoDict[enemyType] = EnemyInfo(**element)

        return enemyInfoDict
    
    def createEnemyEntity(self, enemyID:str, pos:pygame.Vector2) -> bool:
        enemyInfo = self.enemyInfoDict.get(enemyID)
        if enemyInfo != None:
            name = str(f"EnemyEntity_{enemyID}_{self.enemyCount}")
        else:
            Debugger.print("Can't find enemyID({enemyID})")
            return False
    
        newEnemy = EnemyEntity(name, enemyInfo, pos)
        self.enemyList.append(newEnemy)
        return True
    
    def deleteEnemyEntity(self, enemyEntity:EnemyEntity) -> bool:
        if not enemyEntity in self.enemyList:
            Debugger.print(f"Can't delete enemy. {enemyEntity}")
            return False
        
        if not enemyEntity in self.pendingList:
            enemyEntity.setActive(False)
            self.pendingList.append(enemyEntity)
        
        return True
    
    def deleteAllEnemyEntity(self):
        for element in self.enemyList:
            self.deleteEnemyEntity(element)
            
    def getEnemyList(self) -> list[EnemyEntity]:
        return self.enemyList
    
    def update(self, delta) -> None:
        for enemyEntity in self.pendingList:
            enemyEntity.prepareDelete()
            self.enemyList.remove(enemyEntity)
            del enemyEntity
        
        self.pendingList.clear()
    
    # def onEvent(self, event: int, **kwargs):
    #     match(event):             
    #         case GameEvent.GameOver:
    #             for element in self.enemyList:
    #                 self.deleteEnemyEntity(element)
        