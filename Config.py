import json

class Config:

    instance = None

    @staticmethod
    def getConfig():
        if Config.instance == None:
            Config()
        return Config.instance




    def __init__(self, *args, **kwargs):
        if Config.instance != None:
            raise Exception("Error: Class is Singleton - Use getConfig()")
        else:
            Config.instance = self
        super().__init__(*args, **kwargs)

        with open("config.json") as configFile:
            self.config_dict = json.load(configFile)



    
    def getConfigVal(self, setting):
        return self.config_dict[setting]




    def printConfig(self):
        print(self.config_dict)

