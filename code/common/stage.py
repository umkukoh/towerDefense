from common.info import StageInfo, WaveInfo
from manager.TileManager import TileManager


class Stage():
    def __init__(self, stageInfo:StageInfo) -> None:
        self.stageInfo = stageInfo
        self.curWaveIndex = 0
        self.curDeltaTime = 0
        self.lastWaveDeltaTime = 0
        self.curHP = self.stageInfo.hp

    def prepareDelete(self):
        del self.stageInfo

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
                                            if Stage.IsInTimeBtwCurAndLast(element, self.curDeltaTime, self.lastWaveDeltaTime)]
            startPos = TileManager.getScreenPosBytilePos(self.stageInfo.startPos)
            
            

        