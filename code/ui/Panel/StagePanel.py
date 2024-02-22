import pygame
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.core import ObjectID
from common.Enums import GameEvent, GameStateType
from common.Interfaces import IEvent, IInput

from common.info import StageInfo
from manager.Debugger import Debugger
from manager.GameSetting import GameSetting
from manager.StageManager import StageManager
from manager.UIManager import UIManager

class StageButton(UIButton):
    
    def __init__(self, rect:pygame.Rect, manager, container,stageInfo:StageInfo):
        UIButton.__init__(self, rect, "", manager)
        self.stageInfo = stageInfo
        
        lableRect = pygame.Rect(0, rect.height - 30, rect.width, 30)
        lableRect.center = rect.center
        self.costLabel = UILabel(lableRect, str(self.stageInfo.name), manager, container)
        
    def setVisible(self, visible:int):
        self.costLabel.visible = visible
        self.visible = visible
        
    def getStageInfo(self) -> StageInfo:
        return self.stageInfo
    
class StagePanel(IInput, IEvent):
    def __init__(self) -> None:
        manager = UIManager.getInstance().getGUIManager()
        StagePanel_Width = GameSetting.getInt("Screen", "Width")
        StagePanel_Height = GameSetting.getInt("Screen", "Height")
        
        stageButton_StartX = GameSetting.getInt("UI", "StageButton_StartX")
        stageButton_StartY = GameSetting.getInt("UI", "StageButton_StartY")
        stageButton_Width = GameSetting.getInt("UI", "StageButton_Width")
        stageButton_Height = GameSetting.getInt("UI", "StageButton_Height")
        
        rect = pygame.Rect(0, 0, StagePanel_Width, StagePanel_Height)
        
        self.uiPanel = UIPanel(rect, 0, manager, element_id="panel",\
                        object_id= ObjectID(class_id="@BasePanel", object_id="#stageListPanel"))
        
        self.stageButtonList:list[StageButton] = []
        from manager.StageManager import StageManager
        for stageInfo in StageManager.getInstance().getStageInfoList():
            rect = pygame.Rect(stageButton_StartX, stageButton_StartY, stageButton_Width, stageButton_Height)
            stageButton = StageButton(rect, manager, self.uiPanel, stageInfo)
            self.stageButtonList.append(stageButton)
            stageButton_StartY += stageButton_Height
            
        IEvent.__init__(self, {})
        IInput.__init__(self, {pygame_gui.UI_BUTTON_PRESSED, pygame.MOUSEBUTTONUP})
        
        self.setVisible(False)
        
    def setVisible(self, visible:bool):
        self.uiPanel.visible = int(visible)
        for element in self.stageButtonList:
            element.setVisible(int(visible))
            
    def onEvent(slef, event: int, **kwargs):
        pass
    
    def onInputEvent(self, event:pygame.event.Event):
        match(event.type):
            case pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in self.stageButtonList:
                    StageManager.getInstance().setSelectedStageInfo(event.ui_element.getStageInfo())
                    IEvent.sendEvent(GameEvent.ChangeState, nextState = GameStateType.StageLoading)
                    Debugger.print(f"Selected Stage: {event.ui_element}")
        