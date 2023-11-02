

import pygame

from common.Enums import ResourceType
from manager.Debugger import Debugger
from manager.GameSetting import GameSetting


class ResourceManager:
    __instance = None
    _drawLoadingResource = False
    def __init__(self) -> None:
        if not ResourceManager.__instance is None:
            return
        
        ResourceManager.__instance = self
        self.resourceDic = {}
        ResourceManager.__drawLoadingResource = GameSetting.getBoolean("Debug", "DrawLoadingResource")

    def GetResource(resource:str, type:ResourceType = ResourceType.image) -> object:
        if ResourceManager.__instance == None:
            Debugger.print("Make sure ResourceManager was initialized")
            return None
        
        if ResourceManager.__instance.resourceDic.get(resource) == None:
            val = ResourceManager.__loadResource(resource, type)
            ResourceManager.__instance.resourceDic[resource] = val
        
        return ResourceManager.__instance.resourceDic[resource]

    def __loadResource(resource:str, type:ResourceType)-> object:
        val = None
        match(type):
            case ResourceType.image:
                val = pygame.image.load(resource)
            case ResourceType.sound:
                val = pygame.mixer.Sound(resource)

        if ResourceManager.__drawLoadingResource:
            Debugger.print("Loading is {succeed}: {resourceName}".format(succeed = (val !=None), resourceName = resource))
        
        return val