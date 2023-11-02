import random
import pygame
from common.Enums import DirectionType
from common.info import StageInfo
from entity.TileEntity import TileEntity
from manager.GameSetting import GameSetting


class TileManager():
    __instance = None
    tileSize = -1
    tileMaxIndexX = 0
    tileMaxIndexY = 0
    areaWidth = 0
    areaHeight = 0

    def __init__(self) -> None:
        if not TileManager.__instance is None:
            return

        TileManager.__instance = self
        TileManager.tileSize = GameSetting.getInt("Tile", "Size")
        TileManager.tileMaxIndexX = GameSetting.getInt("Tile", "TileMaxIndexX")
        TileManager.tileMaxIndexY = GameSetting.getInt("Tile", "TileMaxINdexY")
        TileManager.areaWidth = GameSetting.getInt("Tile", "AreaWidth")
        TileManager.areaHeight = GameSetting.getInt("Tile", "AreaHeight")

        self.tileList = []
        self.curDirectionMap:dict[tuple[int, int], DirectionType] = {}

    def __clearTiles (self):
        for tile in self.tileList:
            del tile

        self.tileList.clear()

    def __makeTiles(self, data:list[list[str]]):
        self.__clearTiles()
        x = 0
        y = 0

        for row in data:
            for tileData in row:
                directionType = self.getDirectionType((x, y))
                newTile = TileEntity(tileData, directionType, (x, y))
                self.tileList.append(newTile)
                x += 1

            y += 1    
            x = 0

    def makeTiles(stageInfo:StageInfo):
        TileManager.__instance.__getnerateDirectionMap(stageInfo.startPos, stageInfo.endPos, stageInfo.getPathData())
        TileManager.__instance.__makeTiles(stageInfo.getMapData())

    def getTilePosByScreenPos(screenPos:tuple[int, int]) -> TileEntity:
        x = int(screenPos[0] / TileManager.tileSize)
        y = int(screenPos[1] / TileManager.tileSize)
        return (x, y)
    
    def getTileByTilePos(tilePos:tuple[int, int]) -> TileEntity:
        index = tilePos[1] * TileManager.tileMaxIndexX + tilePos[0]
        if -1 < index < len(TileManager.__instance.tileList):
            return TileManager.__instance.tileList[index]
    
        return None
    
    def getScreenPosByTilePos(tilePos:tuple[int, int]) ->tuple[int, int]:
        return ((tilePos[0] + 0.5) * TileManager.tileSize, (tilePos[1] + 0.5) * TileManager.tileSize)
    
    def getTileByScreenPos(screenPos:tuple[int, int]) -> TileEntity:
        tilePos = TileManager.getTilePosByScreenPos(screenPos)
        return TileManager.getTileByTilePos(tilePos)
    
    def IsInTileArea(mousePos) -> bool:
        return (0 <= mousePos[0] <= TileManager.areaWidth) and (0 <= mousePos[1] <= TileManager.areaHeight)
    
    def __getnerateDirectionMap(self, startPos:tuple[int, int], endPos:tuple[int, int], paths:list[tuple[int, int]]):
        self.curDirectionMap.clear()

        allPaths = paths.copy()
        allPaths.insert(0, startPos)
        allPaths.append(endPos)

        preTile = None
        curTile = None
        nextTile = None
        preDirection = DirectionType.NoDirection
        nextDirection = DirectionType.NoDirection
        for index in range(len(allPaths)):
            if preTile == None:
                preTile = allPaths[index]
                continue

            if index + 1 == len(allPaths):
                break

            curTile = allPaths[index]
            if preTile[0] == curTile[0]:
                if preTile[1] < curTile[1]:
                    preDirection = DirectionType.Up
                elif preTile[1] > curTile[1]:
                    preDirection = DirectionType.Down
            elif preTile[1] == curTile[1]:
                if preTile[0] < curTile[0]:
                    preDirection = DirectionType.Left
                elif preTile[0] > curTile[0]:
                    preDirection = DirectionType.Right

            nextTile = allPaths[index+1]
            if curTile[0] == nextTile[0]:
                if curTile[1] < nextTile[1]:
                    nextDirection = DirectionType.Down
                elif curTile[1] > nextTile[1]:
                    nextDirection = DirectionType.Up
            elif curTile[1] == nextTile[1]:
                if curTile[0] < nextTile[0]:
                    nextDirection = DirectionType.Right
                elif curTile[0] > nextTile[0]:
                    nextDirection = DirectionType.Left
            
            self.curDirectionMap[curTile] = preDirection | nextDirection
            preTile = allPaths[index]

    def getDirectionType(self, tileIndex:tuple[int,int]) -> DirectionType | None:
        directionType = self.curDirectionMap.get(tileIndex)
        if directionType == None:
            directionType = DirectionType.NoDirection

        return directionType
    
    def getRandomPointInTile(rect:pygame.Rect, range:int) -> tuple[int, int]:
        minX = rect.centerx - range
        maxX = rect.centerx + range
        minY = rect.centery - range
        maxY = rect.centery + range

        x = random.randint(minX, maxX)
        y = random.randint(minY, maxY)
        return (x, y)