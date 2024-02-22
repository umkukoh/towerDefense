import pygame
from common.Enums import GameEvent, GameStateType
from common.Interfaces import IEvent, IUpdate
from common.info import StageInfo, WaveInfo
from manager.TileManager import TileManager


class Stage(IEvent):
    def __init__(self, stageInfo:StageInfo) -> None:
        self.stageInfo = stageInfo
        self.curWaveIndex = 0
        self.curDeltaTime = 0
        self.lastWaveDeltaTime = 0
        self.curHP = self.stageInfo.hp
        IEvent.__init__(self, {GameEvent.EnemyDie, GameEvent.EnemyExit, GameEvent.GameOver})

    def prepareDelete(self):
        del self.stageInfo
        IEvent.prepareDelete(self)

    def getCurHP(self) -> int:
        return self.curHP

    def getStageInfo(self) -> StageInfo:
        return self.stageInfo

    def getMapData(self) -> list[list[str]]:
        return self.stageInfo.getMapData()

    def getPathData(self) -> list[tuple[int, int]]:
        return self.stageInfo.getPathData()

    def IsIntimeBtwCurAndLast(element:WaveInfo, curDelta, lastDelta) -> bool:
        return lastDelta < element.time <= curDelta
    
    def update(self, delta) -> None:
        self.curDeltaTime += delta

        waveData = self.stageInfo.getWaveInfoData(self.curWaveIndex)
        if waveData != None:
            enemyList = waveData.getEnemyList()
            shouldMakeEnemyData = [element for element in enemyList\
                                            if Stage.IsIntimeBtwCurAndLast(element, self.curDeltaTime, self.lastWaveDeltaTime)]
            startPos = TileManager.getScreenPosByTilePos(self.stageInfo.startPos)
            # startPos = (100,100)
            from manager.EnemyManger import EnemyManager
            for element in shouldMakeEnemyData:
                EnemyManager.getInstance().createEnemyEntity(element.enemyType, pygame.Vector2(startPos))
                
            if self.curDeltaTime > waveData.getEndTime():
                nextWaveIndex = self.curWaveIndex + 1
                if self.stageInfo.getWaveInfoData(nextWaveIndex) != None:
                    self.curWaveIndex += 1
                    IEvent.sendEvent(GameEvent.UpdateStage, stage=self)
        self.lastWaveDeltaTime = self.curDeltaTime
    
    def onEvent(self, event:int, **kwargs):
        match(event):
            case GameEvent.EnemyExit:
                damage = kwargs.get("damage")
                if damage == None:
                    return
                
                if self.curHP > 0:
                    self.curHP -= damage
                    IEvent.sendEvent(GameEvent.UpdateStage, satge=self)
                else:
                    self.curWaveIndex = len(self.stageInfo.getAllWaves())
                    IEvent.sendEvent(GameEvent.ChangeState, nextState=GameStateType.GameOver)
        

        