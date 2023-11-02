from common.Enums import GameEvent
from common.Interfaces import IEvent
from common.stage import Stage


class User(IEvent):
    __instance = None
    
    def __init__(self) -> None:
        if User.__instance != None:
            return
        
        User.__instance = self
        IEvent.__init__(self, GameEvent.set())
        self.curGold = 0
        
    def getCurGold() -> int:
        return User.__instance.curGold
    
    def addGold(gold:int):
        User.__instance.curGold += gold
        IEvent.sendEvent(GameEvent.UpdateStage)
    
    def onEvent(self, event: int, **kwargs):
        match(event):
            case GameEvent.StageInitComplete:
                stage:Stage = kwargs.get("stage")
                if stage != None:
                    User.__instance.curGold = stage.stageInfo.gold
            case GameEvent.EnemyDie:
                reward = kwargs.get("reward")
                if reward != None:
                    User.addGold(reward)
                    IEvent.sendEvent(GameEvent.UpdateStage)