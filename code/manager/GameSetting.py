import configparser

class GameSetting:
    __instance = None

    def __init__(self) -> None:
        if not GameSetting.__instance is None:
            return

        GameSetting.__instance = self
        self.config = configparser.ConfigParser()
        list = self.config.read("./config/config.ini")
        print(f"Succeed in loading '{list[0]}")

    def getBoolean(section:str, option:str) -> bool:
        if GameSetting.__instance is None:
            return False

        return GameSetting.__instance.config.getboolean(section, option)
    
    def getInt(section:str, option:str) -> int:
        if GameSetting.__instance is None:
            return -1

        return GameSetting.__instance.config.getint(section, option)
    
    def getFloat(section:str, option:str) -> float:
        if GameSetting.__instance is None:
            return 0.0

        return GameSetting.__instance.config.getfloat(section, option)


