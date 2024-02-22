import pygame
from common.Enums import EntityType, GameEvent, PriorityType
from common.Interfaces import IEvent
from entity.RenderEntity import RenderEntity
from manager.GameSetting import GameSetting
from pygame_gui.elements import *


class EndPanel(IEvent):
    def __init__(self):
        IEvent.__init__(self, {GameEvent.StageInitComplete, GameEvent.GameOver})
        
        mainPanel_Width = GameSetting.getInt("UI", "MainPanel_Width")
        margin = 60
        
        from manager.UIManager import UIManager
        manager = UIManager.getInstance().getGUIManager()
        
        self.gameOverImage = RenderEntity("YouDied", pygame.Vector2(512, 448), EntityType.UI,\
                                           "./resource/ui/youDied.png", PriorityType.Max, pygame.Vector2(1, 1))
        
        # self.gameOverLabel = UILabel(pygame.Rect(margin, margin, mainPanel_Width - margin, 80), "", manager, object_id="#label_24")
        # self.gameOverLabel.set_image()
        # self.gameOverLabel.text_horiz_alignment = "center"
        # self.gameOverLabel.rebuild()
        
        self.setActive(False)
        
    def prepareDelete(self) -> None:
        # self.gameOverLabel.kill()
        IEvent.prepareDelete(self)
        
    def setActive(self, active:bool) -> None:
        self.gameOverImage.setActive(active)
        # self.gameOverLabel._set_visible(int(active))
        
        
    def onEvent(self, event: int, **kwargs):
        match(event):
            case GameEvent.StageInitComplete:
                self.setActive(False)
                
            case GameEvent.GameOver:
                self.setActive(True)
                
        
        