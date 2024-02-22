import json
import os
from common.info import StageInfo
from common.stage import Stage
from manager.Debugger import Debugger
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
        self.selectedStageInfo:StageInfo = None

    def getInstance():
        return StageManager.__instance
    
    def setSelectedStageInfo(self, selectedStageInfo:StageInfo):
        self.selectedStageInfo = selectedStageInfo
    
    def getStageInfoList(self):
        return list(self.stageInfoDic.values())
    
    def getStageID(stageFileName:str) -> int:
        return int(stageFileName.split('.')[0])
    
    def __loadStageFiles(self, path:str) -> list[str]:
        files = os.listdir(path)
        files = [file for file in files if file.endswith(".json")]
        files.sort(key = StageManager.getStageID)
        files = [f"{path}/{file}" for file in files]
        return files

    def __getStageFile(self, stageIndex:int) -> str:
        if 0 <= stageIndex < len(self.stageFileList):
            return self.stageFileList[stageIndex]

        return None
    
    def unloadStage(self):
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

    def _loadStage(self, stageID:int) -> bool:
        self.unloadStage()
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
    
    def loadSelectedStage(self) -> bool:
        if self.selectedStageInfo == None:
            Debugger.print("SelectedStageInfo is None")
            return False
        
        return self._loadStage(self.selectedStageInfo.id)