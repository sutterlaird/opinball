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
            Config.config_dict = json.load(configFile)




    @staticmethod
    def getConfigVal(setting):
        if Config.instance == None:
            Config()
        return Config.config_dict[setting]


    # @staticmethod
    def __getitem__(self, key):
        # if Config.instance == None:
        #     Config()
        return Config.config_dict[key]




    @staticmethod
    def printConfig():
        print(Config.config_dict)

