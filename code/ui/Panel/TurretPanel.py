
from typing import Dict, Optional, Union
import pygame
import pygame_gui
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface

from pygame_gui.elements import *
from pygame_gui.core import ObjectID, UIElement
from common.Interfaces import IInput

from common.info import TurretInfo
from manager.GameSetting import GameSetting
from manager.UIManager import UIManager

class TurretButton(UIButton):

    def __init__(self, rect:pygame.Rect, manager, container, turretInfo:TurretInfo):
        self.objectID = turretInfo.getUIResource()
        self.turretInfo = turretInfo

        UIButton.__init__(self, rect, "", manager, container,
                          object_id=ObjectID(object_id=self.objectID, class_id="@item_buttons"))
        lableRect = pygame.Rect( 0, rect.height - 30, rect.width , 30)
        lableRect.x += rect.x
        self.costLevel = UILabel(lableRect, str(self.turretInfo.cost), manager, container)
    
    def getCost(self) -> int:
        return self.turretInfo.cost
    
    def getTurretInfo(self) -> TurretInfo:
        return self.turretInfo
    
    def setVisible(self, visible:int):
        self.costLevel._set_visible(visible)
        super()._set_visible(visible)

class TurretPanel(UIPanel, IInput):
    __Instance = None

    def __init__(self, turretInfoList:list[TurretInfo]):
        if TurretPanel.__Instance != None:
            return
        
        TurretPanel.__Instance = self

        manager = UIManager.getInstance().getGUIManager()

        turretPanel_X = GameSetting.getInt("UI", "TurretPanel_X")
        turretPanel_Y= GameSetting.getInt("UI", "TurretPanel_Y")
        turretPanel_Width = GameSetting.getInt("UI", "TurretPanel_Width")
        turretPanel_Height = GameSetting.getInt("UI", "TurretPanel_Height")
        rect = pygame.Rect(turretPanel_X, turretPanel_Y, turretPanel_Width, turretPanel_Height)

        self.uiPanel = UIPanel(rect, 0, manager, element_id="panel",\
                            object_id= ObjectID(class_id="@BasePanel", object_id="#bottomPanel"))
        self.selectedButton:TurretButton = None

        
        IInput.__init__(self, {pygame_gui.UI_BUTTON_PRESSED, pygame.MOUSEBUTTONUP})
        buttonSize = GameSetting.getInt("UI", "TurretButtonSize")
        buttonRect = pygame.Rect(0, 0, buttonSize, buttonSize)
        self.buttonList:list[TurretButton] = []
        for element in turretInfoList:
            button = TurretButton(buttonRect, manager, self.uiPanel, element)
            self.buttonList.append(button)
            buttonRect.x += buttonSize

        self.setVisible(True)

    def setVisible(self, visible:bool):
        self.uiPanel._set_visible(int(visible))
        for element in self.buttonList:
            element.setVisible(visible)
    
    def getSelectedButton() -> TurretButton:
        return TurretPanel.__Instance.selectedButton
    
    def UpdateButton (self):
        curGold = 1000
        for element in self.buttonList:
            active = element.getCost() <= curGold
            if active:
                element.enable()
            else:
                element.disable()

    def onInputEvent(self, event:pygame.event.Event):
        match(event.type):
            case pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in self.buttonList:
                    self.selectedButton = event.ui_element
                    UIManager.getInstance().setSelectedTurret(self.selectedButton.getTurretInfo())