import pygame
import datetime
from manager.GameSetting import GameSetting
from manager.Debugger import Debugger
from common.Interfaces import IInput


class GameTime(IInput):
    __instance = None

    def __init__(self) -> None:
        if not GameTime.__instance is None:
            return
    
        GameTime.__instance = self
        self.clock = pygame.time.Clock()
        self.targetFPS = GameSetting.getInt("Screen", "TargetFPS")
        self.curTimeRate = 1.0
        self.lastTimeRate = 1.0
        self.adjustTimeRate = GameSetting.getFloat("Debug", "AdjustTimeRate")
        self.maxTimeRate = GameSetting.getFloat("Debug", "MaxTimeRate")
        IInput.__init__(self, {pygame.K_9, pygame.K_0, pygame.K_SPACE})

    def getTick(self) -> int:
        dt = int(self.clock.tick(self.targetFPS) * self.curTimeRate)
        return dt
    
    def getCurrentTime(self) -> str:
        return str(datetime.datetime.now())

    def getCurTimeRate(self) -> str:
        return self.curTimeRate

    def getInstance():
        if GameTime.__instance is None:
            GameTime()

        return GameTime.__instance

    def onInputEvent(self, event: pygame.event.Event) :
        match event.key:
            case pygame.K_9:
                if event.type == pygame.KEYUP:
                    self.curTimeRate +=self.adjustTimeRate
                    if self.curTimeRate > self.maxTimeRate:
                        self.curTimeRate = self.maxTimeRate

                    Debugger.print(f"curtimeRate : {self.curTimeRate}")
            
            case pygame.K_0:
                if event.type == pygame.KEYUP:
                    self.curTimeRate -= self.adjustTimeRate
                    if self.curTimeRate < self.adjustTimeRate:
                        self.curTimeRate = self.adjustTimeRate

                    Debugger.print(f"curtimeRate : {self.curTimeRate}")

            case pygame.K_SPACE:
                if event.type == pygame.KEYUP:
                    if self.curTimeRate == 0.0:
                        self.curTimeRate = self.lastTimeRate
                    else:
                        self.lastTimeRate = self.curTimeRate
                        self.curTimeRate = 0.0