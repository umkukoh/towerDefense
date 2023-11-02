
import json

from common.info import TurretInfo
from entity.TurretEntity import TurretEntity
from manager.Debugger import Debugger

class TurretManager():
    __instance = None

    def __init__(self) -> None:
        if TurretManager.__instance != None:
            return
        
        TurretManager.__instance = self
        self.turretDict:dict[str, TurretEntity] = {}

        self.turretInfoDict:dict[str,TurretInfo] = self.__loadTurretInfo("./data/turret.json")
    
    def getInstance():
        return TurretManager.__instance
    
    def getTurretInfoList() -> list[TurretInfo]:
        return list(TurretManager.__instance.turretInfoDict.values())
    
    def getTurretInfo(self, turretID:str) -> TurretInfo:
        return self.turretInfoDict.get(turretID)
    
    def creatTurretEntity(self, tileIndex:tuple[int, int], turretID:str) -> TurretEntity:
        key = str(tileIndex)
        if key in self.turretDict:
            Debugger.print(f"[Error] there is a existing turret in the list : {key}")
            return None

        turretInfo = self.getTurretInfo(turretID)
        if turretInfo == None:
            Debugger.print(f"[Error] Can't find turretID({turretID}) in turretInfoDict")
            return None
        
        turretEntity = TurretEntity(tileIndex, turretInfo)
        self.turretDict[key] = turretEntity
        return turretEntity
    
    def getTurretEntity(self, tileIndex:tuple[int, int]) -> TurretEntity:
        key = str(tileIndex)
        return self.turretDict.get(key)
    
    def deleteTurretInfo(self, tileIndex:tuple[int,int]):
        key = str(tileIndex)
        if not key in self.turretDict:
            Debugger.print(f"[Error] there is no turret with {key} in the list.")
            return
        
        del self.turretDict[key]
        
    def __loadTurretInfo(self, jsonPath) -> dict[str, TurretInfo]:
        turretDict = {}
        file = open(jsonPath)
        if not file is None:
            data = json.load(file)

        for element in data["turretList"]:
            id = element["id"]
            turretDict[id] = TurretInfo(**element)

        return turretDict
        