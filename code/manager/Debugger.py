from enum import IntEnum

import pygame
from manager.GameSetting import GameSetting

from common.MyColor import*
from common.Interfaces import IPostRender

class DebugType(IntEnum):
    Log = 0
    Warning = 1
    Error = 2
    Fatal = 3
    Info = 4

class DebugInfo():
    def __init__(self, msg:str, debugType:DebugType) -> None:
        self.msg = msg
        self.debugType = debugType

class Debugger(IPostRender):
    __instance = None
    __maxCount = 20
    __marginY = 2
    __fontSize = 11
    __fontName = "Courier New"
    __FPSFrequency = 100

    def __init__(self) -> None:
        if not Debugger.__instance is None:
            return
        
        Debugger.__instance = self
        self.debugging = GameSetting.getBoolean("Debug", "Debugging")
        self.drawPrintScreen = GameSetting.getBoolean("Debug", "DrawPrintScreen")
        self.drawPrintOutput = GameSetting.getBoolean("Debug", "DrawPrintOutput")
        self.drawFPS = GameSetting.getBoolean("Debug", "DrawFPS")
        self.screen = None
        self.font = pygame.font.SysFont(Debugger.__fontName, Debugger.__fontSize)
        self.printlist:list[DebugInfo] = []
        self.lastDelta = 0
        self.renderCount = 0
        self.fpsStr = ""
        self.fpsRate = 1000 / Debugger.__FPSFrequency
        IPostRender.__init__(self)

    def print(msg:str, debugType = DebugType.Log):
        if Debugger.__instance.drawPrintOutput:
            print(msg)

        Debugger.__instance.printlist.append(DebugInfo(msg, debugType))
        if len(Debugger.__instance.printlist) > Debugger.__maxCount:
            Debugger.__instance.printlist.pop(0)

    def postRender(self, delta) -> None:
        if self.debugging == False:
            return
        
        if self.screen is None:
            self.screen = pygame.display.get_surface()

        if self.drawPrintScreen:
            self.__renderPrintList()

        if self.drawFPS:
            self.__renderFPS(delta)

    def __getMsgColor(self, debugType:DebugType) -> Color:
        color = WHITE
        match(debugType):
            case DebugType.Log:
                color = WHITE
            case DebugType.Warning:
                color = ORANGE
            case DebugType.Error:
                color = RED1
            case DebugType.Fatal:
                color = BLACK
            case DebugType.Info:
                color = AQUA

        return color

    def __renderPrintList(self):
        pos = pygame.Vector2(5, 5)
        for element in Debugger.__instance.printlist:
            color = self.__getMsgColor(element.debugType)
            surface = Debugger.__instance.font.render(element.msg, True, color)
            self.screen.blit(surface, pos)
            pos.y += surface.get_height () + Debugger.__marginY

    def __renderFPS(self, delta:int):
        from manager.Gametime import GameTime
        self.lastDelta += delta
        self.renderCount += 1

        if(self.lastDelta >= Debugger.__FPSFrequency):
            fps = float(self.renderCount * 1000 / self.lastDelta)

            self.fpsStr = f"{fps:3.1f} fps ({GameTime.getInstance().getCurTimeRate():1.2f})"
            self.lastDelta = 0
            self.rendrCount = 0

        surface = self.font.render(self.fpsStr, True, RED1)
        labelSize = surface.get_size()
        screenSize = self.screen.get_size()
        self.screen.blit(surface, pygame.Vector2(screenSize[0] - labelSize[0] - 5, 5))


