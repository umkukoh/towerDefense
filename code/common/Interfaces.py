
from abc import ABCMeta, abstractmethod
import pygame

from common.Enums import EntityType, RenderCenterType

class IEntity(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    def prepareDelete(self) -> None:
        pass
   
    @abstractmethod
    def getID(self) -> int:
        pass

    @abstractmethod
    def getName(self) -> str:
        pass
    
    @abstractmethod 
    def setScale(self, scale:pygame.Vector2):
        pass

    @abstractmethod
    def getPos(self) -> pygame.Vector2:
        pass

    @abstractmethod
    def setPos(self) -> EntityType:
        pass

    @abstractmethod
    def getActive(self) -> bool:
        pass

    @abstractmethod
    def setActive(self, active:bool):
        pass

    @abstractmethod
    def getAngle(self) -> float:
        pass

    @abstractmethod
    def setAngle(self, float):
        pass

    @abstractmethod
    def getDir(self) -> pygame.Vector2:
        pass

    @abstractmethod
    def setDir(self, dir:pygame.Vector2):
        pass
    
    @abstractmethod
    def getRenderCenter(self) -> RenderCenterType:
        pass
    
    @abstractmethod
    def IsPendingDelete(self) -> bool:
        pass





class IRender(metaclass=ABCMeta):
    __list = []
    __drawCollision = False
    __screenSurface= None

    def __init__(self, priority) -> None:
        IRender.__list.append(self)
        self.priority = priority

        if IRender.__screenSurface == None:
            IRender.__screenSurface = pygame.display.get_surface ()

    def prepareDelete(self) -> None:
        self.screen = None
        IRender.__list.remove(self)

    def getPriority(element):
        return element.priority
    
    def getScreen(self) -> pygame.Surface:
        return IRender.__screenSurface

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def getRect(self) -> pygame.Rect:
        pass
    
    def collisionRender(self) -> None:
        if IRender.__drawCollision == False:
            return

        pygame.draw.rect(IRender.__screenSurce, (20, 20, 255), self.getRect (), 1)

    def renderAll():
        IRender.__list.sort(key=IRender.getPriority, reverse=False)
        for element in IRender.__list:
            if element.getActive():
                element.render()
                element.collisionRender()
    


    
class IUpdate(metaclass=ABCMeta):
    __list = []

    def __init__(self) -> None:
        IUpdate.__list.append(self)

    def prepareDelete(self) -> None:
        IUpdate.__list.remove(self)

    @abstractmethod
    def update(self, delta) -> None:
        pass

    def updateAll(delta):
        for element in IUpdate.__list:
            element.update(delta)

class IInput (metaclass=ABCMeta):
    __listeners = {}
    def __init__(self, keys:set[int]) -> None:
        self.keys = keys
        for key in self.keys:
            self.__addListener(key)
    
    def preapreDelete(self) -> None:
        for key in self.keys:
            self.__removeListener(key)
    
    def __addListener(self, eventKey:int):
        listeners = set()
        if eventKey in IInput.__listeners:
            listeners = IInput.__listeners[eventKey]

        if not self in listeners:
            listeners.add(self)
        
        IInput.__listeners[eventKey] = listeners

    def __removeListener(self, eventKey:int):
        if eventKey in IInput.__listeners:
            listeners = IInput.__listeners[eventKey]
            if self in listeners:
                listeners.remove(self)
    
    def __getListener(key:int) -> list:
        if key in IInput.__listeners:
            return IInput.__listeners[key]

        return None

    def processEvents(event:pygame.event.Event):
        match event.type:
            case pygame.KEYDOWN | pygame.KEYUP:
                listeners = IInput.__getListener(event.key)
                if listeners != None:
                    for element in listeners:
                        element.onInputEvent(event)
            
            case _:
                listeners = IInput.__getListener(event.type)
                if listeners != None:
                    for element in listeners:
                        element.onInputEvent(event)

    @abstractmethod
    def onInputEvent(self, event:pygame.event.Event):
        pass

class IPostRender(metaclass=ABCMeta):
    __list = []
    def __init__(self) -> None:
        IPostRender.__list.append(self)

    def prepareDelete(self) -> None:
        IPostRender.__list.remove(self)

    @abstractmethod
    def postRender(self, delta) -> None:
        pass

    def postRenderAll(delta):
        for element in IPostRender.__list:
            element.postRender(delta)

class IMove (metaclass=ABCMeta):
    __list = []

    def __init__(self) -> None:
        IMove.__list.append(self)

    def prepareDelete(self) -> None:
        IMove.__list.remove(self)
    
    @abstractmethod
    def move(self, delta) -> None:
        pass

    def moveAll(delta):
        for element in IMove.__list:
            if element.getActive():
                element.move(delta)
                
class ICollision(metaclass=ABCMeta):
    __dict:dict[EntityType, list] = {}
    
    def __init__(self, entityType:EntityType) -> None:
        _list:list[ICollision] = []
        self.entityType = entityType
        if ICollision.__dict.get(self.entityType) != None:
            _list = ICollision.__dict[self.entityType]
            
        if not self.entityType in _list:
            _list.append(self)
            
        ICollision.__dict[self.entityType] = _list
    
    def prepareDelete(self) -> None:
        if ICollision.__dict.get(self.entityType) != None:
            _list = ICollision.__dict[self.entityType]
            _list.remove(self)
    
    def checkCollisionAll():
        for entityType, _list in ICollision.__dict.items():
            for element in _list:
                element.updateCollision()
                element.checkCollision()
                
    def getCandidate(checkSet:set[EntityType]) -> dict[EntityType, list]:
        _dict = {}
        if len(checkSet) > 0:
            for entityType, collisionList in ICollision.__dict.items():
                if entityType in checkSet:
                    _dict[entityType] = collisionList.copy()
                    
        return _dict
    
    @abstractmethod
    def updateCollision(self):
        pass        
    
    @abstractmethod
    def checkCollision(self):
        pass  
    
    @abstractmethod
    def getCollisionRect(self)-> pygame.Rect:
        pass  
    
    @abstractmethod
    def getCollisionRectVertices(self)-> list[tuple[int, int]]:
        pass  
    
    
class IEvent(metaclass=ABCMeta):
    __listeners:dict[int, int] = {}
    def __init__(self, events:set[int]) -> None:
        self.events = events
        for event in self.events:
            self.__addListener(event)
    
    def prepareDelete(self) -> None:
        for event in self.events:
            self.__removeListener(event)
    
    def __addListener(self, event:int):
        listeners = []
        if event in IEvent.__listeners:
            listeners = IEvent.__listeners[event]
        
        if not self in listeners:
            listeners.append(self)
        
        IEvent.__listeners[event] = listeners
    
    def __removeListener(self, event:int):
        if event in IEvent.__listeners:
            listeners = IEvent.__listeners[event]
            if self in listeners:
                listeners.remove(self)

    def __getListener(event:int) -> list:
        if event in IEvent.__listeners:
            return IEvent.__listeners[event]
        
        return None
    
    def sendEvent(event:int, **kwargs):
        listeners = IEvent.__getListener(event)
        if listeners != None:
            for element in listeners:
                    element.onEvent(event, **kwargs)
    
    @abstractmethod
    def onEvent(self, event:int, **kwargs):
        pass
    
class IState(metaclass = ABCMeta):
    def __init__(self, key) -> None:
        self.key = key 
        
    @abstractmethod
    def onEnter(self):
        pass
    
    @abstractmethod
    def onUpdate(self, delta):
        pass
    
    @abstractmethod
    def onExit(self):
        pass
    
    def getKey(self):
        return self.key
        
    
    
        
                
            
        