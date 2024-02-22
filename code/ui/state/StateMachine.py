from enum import Enum
from common.Enums import GameStateType
from common.Interfaces import IState, IUpdate
from manager.Debugger import Debugger


class StateMachine(IUpdate):
    def __init__(self) -> None:
        IUpdate.__init__(self)
        self.stateDic = {}
        self.curState:IState = None
        self.nextState:IState = None
        
    def prepareDelete(self) -> None:
        self.stateDic.clear()
        self.curState = None
        self.nextState = None
        return super().prepareDelete()
    
    def getCurStateKey(self) -> GameStateType:
        if self.curState == None:
            return GameStateType.Invalid
        
        return self.curState.getKey()
    
    def addState(self, state: IState):
        key = state.getKey()
        if self.stateDic.get(key) != None:
            Debugger.print(f"{str(key)} already exist in {self}")
            return
        
        self.stateDic[key] = state
        
    def update(self, delta) -> None:
        if self.nextState != None:
            if self.curState != None:
                self.curState.onExit()
            
            self.curState = self.nextState
            self.curState.onEnter()
            self.nextState = None
        
        elif self.curState != None:
            self.curState.onUpdate(delta)
            
    def setNext(self, key:Enum):
        self.nextState = self.stateDic.get(key)
        if self.nextState == None:
            Debugger.print(f"{str(key)} does not exist in {self}")