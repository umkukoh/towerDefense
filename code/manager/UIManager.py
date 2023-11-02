import pygame
import pygame_gui
from common.Enums import EntityType, GameEvent, GameStateType, PriorityType, TileType
from common.Interfaces import IEvent, IInput
from common.info import TurretInfo
from entity.RenderEntity import RenderEntity
from entity.TurretEntity import TurretEntity
from manager.GameSetting import GameSetting
from manager.TileManager import TileManager
from manager.TurretManager import TurretManager


class UIManager(IInput, IEvent):
    __instance = None
    __rangeUnitSize = None
    def __init__(self, screenSize) -> None:
        if UIManager.__instance != None:
            return
        
        UIManager.__instance = self
        IInput.__init__(self, {pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP})
        IEvent.__init__(self, GameEvent.set())
        self.ui_manager = pygame_gui.UIManager(screenSize, "./data/ui/theme.json")
        self.ui_manager.set_visual_debug_mode(True)
    
        pos = pygame.Vector2(0, 0)
        self.selector = RenderEntity("Selector", pos, EntityType.Selector, "./resource/selector.png", PriorityType.Second, active=False)
        self.selector.setAlpha(150)

        turretscale = pygame.Vector2(1, 1) * GameSetting.getFloat("Turret", "Scale")
        self.selectedTurret = RenderEntity("Selectedturret", pygame.Vector2(), EntityType.Selector, "./resource/turret/single_Artillery_0.png", PriorityType.Second, turretscale, False)
        self.selectedTurret.setAlpha(100)
        self.selectedTurretInfo:TurretInfo = None
        self.selectedTurretEntity:TurretEntity = None

        if UIManager.__rangeUnitSize == None:
            UIManager.__rangeUnitSize = GameSetting.getInt("Turret", "RangeUnitSize")
        
        self.rangeEntity = RenderEntity(f"RangeEntity", pygame.Vector2(), EntityType.Range, "./resource/range.png", PriorityType.Third, active=False)

        from ui.Panel.TurretPanel import TurretPanel
        from ui.Panel.MainPanel import MainPanel
        
        self.mainPanel = MainPanel()
        self.turretPanel = TurretPanel(TurretManager.getTurretInfoList())


    def getInstance():
        return UIManager.__instance
    
    def __setSelector(self, active, pos:pygame.Vector2):
        self.selector.setActive(active)
        self.selector.setPos(pos)

    def getGUIManager(self):
        return self.ui_manager
    
    def setSelectedTurretEntity(self, turret:TurretEntity):
        self.selectedTurretEntity = turret
        # if turret != None:
        #     self.setRangeEntity(turret.rangeRate, turret.getPos() ,True)
        # else:
        #     self.setRangeEntity(1.0, pygame.Vector2(0, 0), False)

    def setRangeEntity(self, rate:float, pos:pygame.Vector2, active:bool):
        range = UIManager.__rangeUnitSize * rate
        targetRangeSize = range * 2.0
        rangeResourceSize = self.rangeEntity.getResourceSize()
        targetScale = pygame.Vector2(targetRangeSize / rangeResourceSize[0], targetRangeSize / rangeResourceSize[1])
        self.rangeEntity.setScale(targetScale)
        self.rangeEntity.setPos(pos)
        self.rangeEntity.setActive(active)

    def setActiveRangeEntity(self, active:bool):
        if self.rangeEntity == None:
            return
        
        self.rangeEntity.setActive(active)


    def setSelectedTurret(self, turretInfo:TurretInfo):
        self.selectedTurretInfo = turretInfo
        self.selectedTurret.setActive(turretInfo != None)
        if turretInfo != None:
            self.selectedTurret.setResource(turretInfo.getSpriteResource())
            
    def setGameStatePanel(self, gameState:GameStateType):
        self.mainPanel.setVisible(GameStateType.Stage == gameState)
        self.turretPanel.setVisible(GameStateType.Stage == gameState)
    
    
    def onInputEvent(self, event:pygame.event.Event):
        match(event.type):
            case pygame.MOUSEMOTION:
                
                mousePos = pygame.mouse.get_pos()
                tile = TileManager.getTileByScreenPos(mousePos)
                isInTileArea = TileManager.IsInTileArea(mousePos)
                pos = pygame.Vector2(0,0)
                if isInTileArea and tile != None:
                    pos = tile.getPos ()

                if self.selectedTurretInfo != None:
                    self.selectedTurret.setActive(True)
                    self.selectedTurret.setPos(pos)
                    self.__setSelector(False, pos)
                else:
                    self.selectedTurret.setActive(False)
                    self.__setSelector(isInTileArea, pos)

            case pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                tilePos = TileManager.getTilePosByScreenPos(mousePos)
                tile = TileManager.getTileByScreenPos(mousePos)
                isInTileArea = TileManager.IsInTileArea(mousePos)
                if isInTileArea:
                    if self.selectedTurretInfo != None and tile.getTileType() == TileType.buildable:
                        turret = TurretManager.getInstance().creatTurretEntity(tilePos, self.selectedTurretInfo.id)
                        if turret != None:
                            tile.setTileType(TileType.built)
                            self.setSelectedTurretEntity(turret)
                            # User.addGold(-self.selectedTurretInfo.cost)

                        elif self.selectedTurretInfo == None and tile.getTileType() == TileType.built:
                            turret = TurretManager.getInstance().getTurretEntity(tilePos)
                            self.setSelectedTurretEntity(turret)
                        else:
                            self.setSelectedTurretEntity(None)
                else:
                    self.setSelectedTurretEntity(None)

                self.setSelectedTurret(None)
                        
                
                

        