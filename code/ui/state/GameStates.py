from common.Enums import GameEvent, GameStateType
from common.Interfaces import IEvent, IState
from manager.BulletManager import BulletManager
from manager.Debugger import Debugger
from manager.EnemyManger import EnemyManager
from manager.StageManager import StageManager
from manager.TileManager import TileManager
from manager.TurretManager import TurretManager


class BaseGameState(IState):
    def __init__(self, key) -> None:
        IState.__init__(self, key)
        
    def onEnter(self):
        Debugger.print(f"[GameState] {self.getKey().name} Enter")
        
    def onUpdate(self, delta):
        pass
    
    def onExit(self):
        Debugger.print(f"[GameState] {self.getKey().name} Exit")
        
class AppInitState (BaseGameState):
    __initTime = 1000
    def __init__(self) -> None:
        BaseGameState.__init__(self, GameStateType.AppInit)
        self.curTime = 0 
        
    def onEnter(self):
        super().onEnter()
        self.isLoadComplete = True
        
    def onUpdate(self, delta):
        if self.curTime > AppInitState.__initTime:
            IEvent.sendEvent(GameEvent.ChangeState, nextState=GameStateType.StageList)
        else:
            self.curTime += delta
    
    def onExit(self):
        super().onEnter()
        
class StageListState (BaseGameState):
    __initTime = 1000
    def __init__(self) -> None:
        BaseGameState.__init__(self, GameStateType.StageList)
        self.curTime = 0 
        
    def onEnter(self):
        super().onEnter()
        
    # def onUpdate(self, delta):
    #     pass
        
    def onExit(self):
        super().onEnter()
        
class StageLoadingState (BaseGameState):
    __initTime = 1000
    def __init__(self) -> None:
        BaseGameState.__init__(self, GameStateType.StageLoading)
        self.isLoadComplete = False
        
    def onEnter(self):
        super().onEnter()
        self.isLoadComplete = StageManager.getInstance().loadSelectedStage()
        
    def onUpdate(self, delta):
        if self.isLoadComplete:
            IEvent.sendEvent(GameEvent.ChangeState, nextState = GameStateType.StagePlay)
        
    def onExit(self):
        super().onEnter()
        
class StagePlayState (BaseGameState):
    __initTime = 1000
    def __init__(self) -> None:
        BaseGameState.__init__(self, GameStateType.StagePlay)
        self.curStage = None
        
    def onEnter(self):
        super().onEnter()
        self.curStage = StageManager.getInstance().getCurrentStage()
        IEvent.sendEvent(GameEvent.StageInitComplete, stage=self.curStage)
        
    def onUpdate(self, delta):
        if self.curStage.update(delta) == False:
            IEvent.sendEvent(GameEvent.ChangeState, nextState=GameStateType.StageClear)
        
    def onExit(self):
        super().onEnter()
        self.curStage = None
        
class StageClearState (BaseGameState):
    __initTime = 1000
    def __init__(self) -> None:
        BaseGameState.__init__(self, GameStateType.StageClear)
        self.curTime = 0 
        
    def onEnter(self):
        super().onEnter()
        
    def onExit(self):
        super().onEnter()

class GameOverState (BaseGameState):
    __waitTime = 3000
    def __init__(self) -> None:
        BaseGameState.__init__(self, GameStateType.GameOver)
        self.curTime = 0 
        
    def onEnter(self):
        super().onEnter()
        self.curtime = 0
        
    
    def onUpdate(self, delta):
        if self.curTime > GameOverState.__waitTime:
            IEvent.sendEvent(GameEvent.ChangeState, nextState=GameStateType.StageUnloading)
        else:
            self.curTime += delta
            
    def onExit(self):
        super().onEnter()

class StageUnloadingState(BaseGameState):
    def __init__(self) -> None:
        BaseGameState.__init__(self, GameStateType.StageUnloading)
        self.curIndex = -1
        self.lambdaList = []
        self.lambdaList.append(lambda : BulletManager.getInstance().deleteAllBulletEntity())
        self.lambdaList.append(lambda : TurretManager.getInstance().deleteAllTurretEntity())
        self.lambdaList.append(lambda : EnemyManager.getInstance().deleteAllEnemyEntity())
        self.lambdaList.append(lambda : TileManager.getInstance().deleteAllTiles())
        self.lambdaList.append(lambda: StageManager.getInstance().unloadStage())
     
    def onEnter(self):
        super().onEnter()
        self.curIndex = 0
        
    def onUpdate(self, delta):
        if -1 < self.curIndex < len(self.lambdaList):
            self.lambdaList[self.curIndex]()
            self.curIndex += 1
        elif self.curIndex == len(self.lambdaList):
            IEvent.sendEvent(GameEvent.ChangeState, nextState=GameStateType.StageList)
            self.curIndex = -1
    
    def onExit(self):
        super().onExit()