import pygame
from common.Enums import DirectionType, EntityType, PriorityType, TileType
from common.MyColor import GREEN
from entity.RenderEntity import RenderEntity
from manager.GameSetting import GameSetting


class TileEntity(RenderEntity):
    __SIZE = -1
    __IMAGE_FORMAT="./resource/tile/tile_{type}.jpg"
    __drawTile = None
    __screen = None

    def __init__(self, tileData:str, direction:DirectionType, tileIndex:tuple[int, int]) -> None:
        if TileEntity.__SIZE == -1:
            TileEntity.__SIZE = GameSetting.getInt("Tile", "Size")
        
        if TileEntity.__drawTile == None:
            TileEntity.__drawTile = GameSetting.getBoolean("Debug", "Debugging") and GameSetting.getBoolean("Debug", "DrawTile")
        
        if TileEntity.__screen == None:
            TileEntity.__screen = pygame.display.get_surface()
        
        self.__tileType = TileType(int(tileData))
        self.tileIndex = tileIndex
        if self.__tileType == TileType.buildable:
            direction = DirectionType.Up | DirectionType.Down | DirectionType.Left | DirectionType.Right

        directionStr = str(f"{direction:04b}")
        name = "{_class}[{_y}][{_x}]".format(_class = TileEntity.__name__, _y = tileIndex[0], _x = tileIndex[1])
        resource = TileEntity.__IMAGE_FORMAT.format(type = directionStr)
        pos = pygame.Vector2(self.tileIndex[0] + 0.5, self.tileIndex[1] + 0.5) * TileEntity.__SIZE
        RenderEntity.__init__(self, name, pos, EntityType.Tile, resource, PriorityType.First)

    def prepareDelete(self):
        RenderEntity.prepareDelete(self)

    def getTileType(self) -> TileType:
        return self.__tileType

    def setTileType(self, tileType:TileType):
        self.__tileType = tileType

    def postRender(self, delta) -> None:
        if TileEntity.__drawTile == True:
            pygame.draw.rect(TileEntity.__screen, GREEN, self.getRect(), 1)

        return super().postRender(delta)
    


