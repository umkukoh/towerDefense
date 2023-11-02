import pygame
from pygame_gui.elements import *
from common.Enums import GameEvent
from common.Interfaces import IEvent
from common.User import User
from common.stage import Stage
from manager.GameSetting import GameSetting
from manager.ResourceManager import ResourceManager
from manager.StageManager import StageManager


class MainPanel(IEvent):
    __goldResource = "./resource/ui/coin.png"
    
    def __init__(self):
        IEvent.__init__(self, {GameEvent.StageInitComplete, GameEvent.UpdateStage})
        
        from manager.UIManager import UIManager
        manager = UIManager.getInstance().getGUIManager()
        
        mainPanel_X = GameSetting.getInt("UI", "MainPanel_X")
        mainPanel_Y = GameSetting.getInt("UI", "MainPanel_Y")
        mainPanel_Width = GameSetting.getInt("UI", "MainPanel_Width")
        mainPanel_Height = GameSetting.getInt("UI", "MainPanel_Height")
        
        self.stageNumLabel = UILabel(pygame.Rect(20, 20, 300, 40), "test text 012345678", manager, object_id="#label_24", visible=0)
        self.stageNumLabel.text_horiz_alignment = "left"
        self.stageNumLabel.rebuild()
        
        marginX = 300
        marginY = 30
        hpBarHeight = 20
        self.maxStageHP = 100
        self.curStageHP = self.maxStageHP
        hpBarRect = pygame.Rect(mainPanel_X + marginX, mainPanel_Y + marginY, mainPanel_Width - (marginX * 2), hpBarHeight)
        self.uiHPBar = UIStatusBar(hpBarRect, manager, percent_method= self.getPercent)

        self.waveNumLabel = UILabel(pygame.Rect(20, 60, 300, 30), "0/0", manager, object_id="#label_24")
        self.waveNumLabel.text_horiz_alignment = "left"
        self.waveNumLabel.rebuild()  
        
        goldSurface = ResourceManager.GetResource(MainPanel.__goldResource) 
        self.goldUIImage = UIImage(pygame.Rect((mainPanel_Width - 40, 20), goldSurface.get_size()), goldSurface, manager)           
        self.goldLabel = UILabel(pygame.Rect(mainPanel_Width - 200, 20, 250, 30), "0", manager, object_id="#label_24")
        self.goldLabel.text_horiz_alignment = "right"
        
        self.setVisible(False)
        
    def prepareDelete(self) -> None:
        self.goldLabel.kill()
        self.goldUIImage.kill()
        self.waveNumLabel.kill
        self.uiHPBar.kill()
        self.stageNumLabel.kill()
        IEvent.prepareDelete(self)
        
    def setVisible(self, visible:bool):
        self.goldLabel._set_visible(int(visible))
        self.goldUIImage._set_visible(int(visible))
        self.waveNumLabel._set_visible(int(visible))
        self.uiHPBar._set_visible(int(visible))
        self.stageNumLabel._set_visible(int(visible))
    
    def getPercent(self) -> float:
        return self.curStageHP / self.maxStageHP
    
    def setUpStageInfo(self, stage:Stage):
        stageInfo = stage.getStageInfo()
        self.maxStageHP = stageInfo.hp
        self.curStageHP = stage.curHP
        self.updateStageNum(stageInfo.getName())
        self.updateWaveNum(stage)
        self.updateGold(User.getCurGold())
        
    def updateWaveNum(self, stage:Stage):
        self.waveNumLabel.set_text(f"{stage.curWaveIndex + 1} / {len(stage.stageInfo.waves)} Wave")

    def updateStageNum(self, stageName):
        self.stageNumLabel.set_text(stageName)
        self.stageNumLabel._set_visible(1)
        
    def updateGold(self, gold:int):
        self.goldLabel.set_text(str(gold))

    def onEvent(self, event:int, **kwargs):
        match(event):
            case GameEvent.StageInitComplete | GameEvent.UpdateStage:
                curStage = kwargs.get("stage")
                if curStage == None:
                    curStage = StageManager.getInstance().getCurrentStage()
                self.setUpStageInfo(curStage)    

        
        