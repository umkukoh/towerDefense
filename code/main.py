import pygame
from common.Enums import GameEvent, GameStateType
from common.Interfaces import ICollision, IEntity, IEvent, IInput, IMove, IPostRender, IRender, IUpdate
from common.User import User
from manager.BulletManager import BulletManager
from manager.Debugger import Debugger
from manager.EnemyManger import EnemyManager
from manager.GameSetting import GameSetting
from manager.GameStateMachine import GameStateMachine
from manager.Gametime import GameTime
from manager.ResourceManager import ResourceManager
from manager.StageManager import StageManager
from manager.TileManager import TileManager
from manager.TurretManager import TurretManager
from manager.UIManager import UIManager

def main():
    pygame.init()
    GameSetting()
    GameTime()
    StageManager()
    Debugger()
    ResourceManager()
    TileManager()
    TurretManager()
    BulletManager()
    EnemyManager()
    User()


    screenWidth = GameSetting.getInt("Screen", "Width")
    screenHeight = GameSetting.getInt("Screen", "Height")
    cation = "Tower Defense"
    screenSize = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption(cation)

    UIManager(screenSize)
    ui_manager = UIManager.getInstance().getGUIManager()
    GameStateMachine()
    
    # if StageManager.getInstance().loadStage(0) == False:
    #     Debugger.print(f"Can't load Stage with stageIndex({0})")

    # testManager = EnemyManager.getInstance()
    # startPos = StageManager.getInstance ().getCurrentStage().getStageInfo().startPos
    # startPos = TileManager.getScreenPosByTilePos(startPos)
    
    # IEvent.sendEvent(GameEvent.ChangeState, nextState=GameStateType.StagePlay)
    # IEvent.sendEvent(GameEvent.StageInitComplete, stage=StageManager.getInstance().getCurrentStage())
        

    running = True
    while running:
        deltaTime = GameTime.getInstance().getTick()
        for event in pygame.event.get():
            match(event.type):
                case pygame.QUIT:
                    running = False

            IInput.processEvents(event)
            ui_manager.process_events(event)

        # update
        IUpdate.updateAll(deltaTime)
        IMove.moveAll(deltaTime)
        ICollision.checkCollisionAll()
        
        ui_manager.update(deltaTime)
    


        # render
        IRender.renderAll()
        IPostRender.postRenderAll(deltaTime)

        ui_manager.draw_ui(screen)

        pygame.display.update()
    
    pygame.quit()
    
if __name__ == "__main__":
    main()