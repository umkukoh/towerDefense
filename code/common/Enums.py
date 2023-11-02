

from enum import IntEnum

class ExtendedEnum(IntEnum):

    @classmethod
    def set(cls) -> set:
        return set(map(lambda c: c.value, cls))
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    

class PriorityType(ExtendedEnum):
    First = 0
    Second = 1
    Third = 2
    Fourth = 3
    Max = 15

class EntityType(ExtendedEnum):
    Stage = 0
    Tile = 1
    Selector = 2
    Turret = 3
    Bullet = 4
    Enemy = 5
    Range = 6
    Deco = 7
    UI = 15

class ResourceType(ExtendedEnum):
    image = 0
    text = 1
    sound = 2

class DirectionType(ExtendedEnum):
    NoDirection = 0
    Up = 1 << 0
    Down = 1 << 1
    Left = 1 << 2
    Right = 1 << 3

class TileType(ExtendedEnum):
    unbuildable = 0
    buildable = 1
    path = 2

    built = 5

class EnemyType (ExtendedEnum):
    small = 0
    medium = 1
    big = 2

class RenderCenterType(ExtendedEnum):
    Center = 0
    Bottom = 1

class BoxCollisionArea(ExtendedEnum):
    #   *---*
    #   |   |
    #   *---*
    
    #--------------------------------------------------------------
    #   __top_left     |  __top_both       |  __top_right         -
    #--------------------------------------------------------------
    #  __left_both     |                   |  __right_both        -
    #--------------------------------------------------------------
    #  __bottom_left   |  __bottom_both    |  __bottom_right      -
    #--------------------------------------------------------------
    
    Top_Left =      0b0001
    Top_Right =     0b0010
    Bottom_Left =   0b0100
    Bottom_Right =  0b1000
    
    Top_Both =      0b0011
    Bottom_Both =   0b1100
    Left_Both =     0b0101
    Right_Both =    0b1010
    All =           0b1111
    
class GameStateType(ExtendedEnum):
    AppInit = 0
    StageList = 1
    StageLoading = 2
    Stage = 3
    StageClear = 4
    StageEnd = 5
    
    Invalid = 7
    
class GameEvent(ExtendedEnum):
    StageLoadComplete = 0
    StageInitComplete = 1
    StageClear = 2
    WaveClear = 3
    EnemyDie = 4
    EnemyExit = 5
    UpdateStage = 6
    ChangeState = 7
    GameOver = 256
    
    