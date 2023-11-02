import pygame
from common.Interfaces import IEntity
from common.MyColor import BLUE2, PINK
from manager.Debugger import Debugger
from manager.GameSetting import GameSetting
from manager.StageManager import StageManager
from manager.TileManager import TileManager


class PathFindComponent():
    __drawPath = None
    __pathRange = None

    def __init__(self, entity:IEntity) -> None:
        if PathFindComponent.__drawPath == None:
            PathFindComponent.__drawPath = GameSetting.getBoolean("Debug", "Debugging") and GameSetting.getBoolean("Debug", "DrawPath")

        if PathFindComponent.__pathRange == None:
            PathFindComponent.__pathRange = GameSetting.getInt("Path", "PathRange")

        self.entity = entity
        self.path = self.__generatePath()
        self.curPathIndex = 0

    def prepareDelete(self):
        self.entity = None  

    def __generatePath(self) -> list[tuple[int, int]]:
        path = []
        startPos = self.entity.getPos()
        path.append ((int(startPos.x), int(startPos.y)))
        pathData = StageManager.getInstance ().getCurrentStage().getPathData()

        for tileIndex in pathData:
            tileEntity = TileManager.getTileByTilePos((tileIndex[0], tileIndex[1]))
            if tileEntity == None:
                Debugger.print(f"Can't Find TileEntity with tileIndex{tileIndex}")
                continue

            path.append(TileManager.getRandomPointInTile(tileEntity.getRect(), PathFindComponent.__pathRange))
        
        endPos = StageManager.getInstance ().getCurrentStage().getStageInfo ().getEndPos()
        path.append(TileManager.getScreenPosByTilePos(endPos))
        return path

    def getCurTargetPos(self) -> pygame.Vector2:
        if self.curPathIndex >= len(self.path):
            return None
        
        return pygame.Vector2(self.path[self.curPathIndex])
    
    def NextTarget(self):
        self.curPathIndex += 1

    def postRender(self, delta):
        if PathFindComponent.__drawPath == False:
            return
        
        for index in range(len(self.path) - 1):
            start = self.path[index]
            end = self.path[index + 1]
            pygame.draw.line(self.screen, PINK, start, end)
            pygame.draw.circle(self.screen, BLUE2, end, 2)
          