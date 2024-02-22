from common.Enums import GameEvent
from common.Interfaces import IEvent
from ui.state.StateMachine import StateMachine
from ui.state.GameStates import *


class GameStateMachine(StateMachine, IEvent):
    __instance = None
    
    def __init__(self) -> None:
        if GameStateMachine.__instance != None:
            return
        
        GameStateMachine.__instance = self
        StateMachine.__init__(self)
        IEvent.__init__(self, GameEvent.set())
        self.addState(AppInitState())
        self.addState(StageListState())
        self.addState(StageLoadingState())
        self.addState(StagePlayState())
        self.addState(StageClearState())
        self.addState(GameOverState())
        self.addState(StageUnloadingState())
        
        IEvent.sendEvent(GameEvent.ChangeState, nextState=GameStateType.AppInit)
        
    def prepareDelete(self) -> None:
        StateMachine.prepareDelete(self)
        
    def getInstance():
        return GameStateMachine.__instance
    
    def onEvent(self, event: int, **kwargs):
        match(event):
            case GameEvent.ChangeState:
                nextState = kwargs.get("nextState")
                self.setNext(nextState)
