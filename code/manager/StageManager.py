import json
import os
from common.info import StageInfo
from common.stage import Stage
from manager.TileManager import TileManager


class StageManager():
    __instance = None
    __path = "./data/stage"

    def __init__(self) -> None:
        if StageManager.__instance != None:
            return
        
        StageManager.__instance = self
        self.stageFileList = self.__loadStageFiles(StageManager.__path)
        self.curStage:Stage = None
        self.stageInfoDic = self.__loadAllStageInfo()

    def getInstance():
        return StageManager.__instance
    
    def getStageInfoList(self):
        return list(self.stageInfoDic.values())
    
    def __loadStageFiles(self, path:str) -> list[str]:
        files = os.listdir(path)
        files = [f"{path}/{file}" for file in files if file.endswith(".json")]
        files.sort()
        return files

    def __getStageFile(self, stageIndex:int) -> str:
        if 0 <= stageIndex < len(self.stageFileList):
            return self.stageFileList[stageIndex]

        return None
    
    def __unloadStage(self):
        if self.curStage!= None:
            self.curStage.prepareDelete()
            del self.curStage

    def __loadAllStageInfo(self) -> dict[int, StageInfo]:
        stageInfoDict = {}

        for stageFile in self.stageFileList:
            file = open(stageFile)
            if not file is None:
                data = json.load(file)
            
            stageInfo = StageInfo(**data["stage"])
            stageInfoDict[stageInfo.id] = stageInfo

        return stageInfoDict

    def loadStage(self, stageID:int) -> bool:
        self.__unloadStage()
        stageFile = self.__getStageFile(stageID)
        if stageFile == None:
            return False
    
        file = open(stageFile)
        if not file is None:
            data = json.load(file)
        
        stageInfo = StageInfo(**data ["stage"])
        self.curStage = Stage(stageInfo)
        TileManager.makeTiles(self.curStage.getStageInfo())
        return True
    
    def getCurrentStage(self) -> Stage:
        return self.curStage