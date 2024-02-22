import json
from common.Interfaces import IUpdate
from common.info import BulletInfo
from entity.BulletEntity import BulletEntity
from manager.Debugger import Debugger
from manager.GameSetting import GameSetting


class BulletManager(IUpdate):
    __instance = None
    __autoDeleteX = -1
    __autoDeleteY = -1

    def __init__(self) -> None:
        if BulletManager.__instance != None:
            return
        
        BulletManager.__instance = self
        IUpdate.__init__(self)
        self.bulletList:list[BulletEntity] = []
        self.bulletInfoDict:dict[str, BulletInfo] = self.__loadBulletInfo("./data/bullet.json")

        BulletManager.__autoDeleteX = GameSetting.getInt("Screen", "Width") * 1.1
        BulletManager.__autoDeleteY = GameSetting.getInt("Screen", "Height") * 1.1

    def getInstance():
        return BulletManager.__instance

    def getBulletInfo(bulletID) -> BulletInfo:
        return BulletManager.__instance.bulletInfoDict.get(bulletID) 
    
    def creatBulletEntity(self, bulletID:str, pos:tuple[int, int], angle:float = 0.0) -> BulletEntity:
        bulletInfo = BulletManager.getBulletInfo(bulletID)
        if bulletInfo == None:
            Debugger.print(f"Can't find bulletID({bulletID}) in bulletInfoDict")
            return None
        
        bulletEntity = BulletEntity(bulletInfo, pos, angle)
        self.bulletList.append(bulletEntity)
        return bulletEntity
    
    def deleteBulletEntity(self, bulletEntity:BulletEntity):
        self.bulletList.remove(bulletEntity)
        bulletEntity.prepareDelete()
        del bulletEntity
        
    def deleteAllBulletEntity(self):
        for bullet in self.bulletList:
            bullet.prepareDelete()
            del bullet
        
        self.bulletList.clear()
        

    def __loadBulletInfo(self, jsonPath) -> dict[str, BulletInfo]:
        bulletDict = {}
        file = open(jsonPath)
        if not file is None:
            data = json.load(file)

        for element in data["bulletList"]:
            id = element["id"]
            bulletDict[id] = BulletInfo(**element)

        return bulletDict
    
    def update(self, delta) -> None:
        for element in self.bulletList[:]:
            pos = element.pos
            if not 0 <=pos.x <= BulletManager.__autoDeleteX or \
                not 0<= pos.y <= BulletManager.__autoDeleteY:
                self.bulletList.remove(element)
                element.prepareDelete()
                del element
    