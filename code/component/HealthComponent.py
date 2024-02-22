import pygame
import pygame_gui
from common.Interfaces import IEntity, IUpdate
from pygame_gui.elements import *

from manager.Debugger import Debugger
from manager.GameSetting import GameSetting



class DamageText(IUpdate):
    __widthUnit = 200
    __defaultHeight = 300
    __speed = None
    __maxMoveY = 30
    __normalLabel = "#label_red_16"
    __criticalLabel = "#label_purple_24"
    def __init__(self, damageInfo:tuple[int, bool], pos:tuple[int, int]) -> None:
        IUpdate.__init__(self)
        from manager.UIManager import UIManager
        manager = UIManager.getInstance().getGUIManager()
        damage = damageInfo[0]
        width = len(str(damage)) * DamageText.__widthUnit
        rect = pygame.Rect(0, 0, width, DamageText.__defaultHeight)
        self.startY = pos[1]
        rect.center = pos
        
        if DamageText.__speed == None:
            DamageText.__speed = GameSetting.getFloat("UI", "DamageText_Speed")
        
        objecctIDForLabel = DamageText.__normalLabel
        if damageInfo[1]:
            objecctIDForLabel = DamageText.__criticalLabel
            
        self.stageNumLabel = UILabel(rect, str(damage), manager, object_id=objecctIDForLabel)

    def __del__(self):
        Debugger.print(f"Delete : {self}")
    
    def prepareDelete(self) -> None:
        self.stageNumLabel.kill()
        IUpdate.prepareDelete(self)
    
    def update(self, delta) -> None:
        curPos = self.stageNumLabel.rect.center
        moveY = curPos[1] - DamageText.__speed * delta
        
        if moveY > self.startY - DamageText.__maxMoveY:
            self.stageNumLabel.rect.center = (curPos[0], moveY)
        else:
            self.prepareDelete()
            del self
            
class HealthComponent():
    __uiResourceKey = "health_bar"
    
    def __init__(self, entity:IEntity, maxHP:int, width, height, displayOffset:tuple[int, int]) -> None:
        self.entity = entity
        self.maxHP = maxHP
        self.curHP = maxHP
        self.displayOffset = displayOffset
        pos = self.entity.getPos().copy()
        
        self.hpBarRect = pygame.Rect(pos[0] + displayOffset[0], pos[1] + displayOffset[1], width, height)
        
        from manager.UIManager import UIManager
        manager = UIManager.getInstance().getGUIManager()
        self.uiHPBar = UIStatusBar(self.hpBarRect, manager, percent_method= self.getPercent)
        
    def prepareDelete(self):
        self.uiHPBar.kill()
        del self.uiHPBar
        self.entity = None
        
    def getPercent(self) -> float:
        return self.curHP / self.maxHP
    
    def getDamage(self, damageInfo:tuple[int, bool]) -> bool:
        self.curHP -= damageInfo[0]
        pos = self.entity.getPos()
        DamageText(damageInfo, (int(pos.x), int(pos.y)))
        return self.curHP > 0 
    
    def updateHPBar(self):
        pos = self.entity.getPos().copy()
        pos.x += self.displayOffset[0]
        pos.y += self.displayOffset[1]
        self.uiHPBar.set_position(pos)
        