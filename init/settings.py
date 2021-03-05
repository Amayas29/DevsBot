import json
                                                     

class Settings():
    
    __instance = None

    def __new__(cls, file_settings="resources/settings.json", file_config="config.json") :

        if not cls.__instance is None :
            return cls.__instance

        cls.__instance = object.__new__(cls)

        try:
            with open(file_settings) as st:
                data = json.load(st)
            
            with open(file_config) as ct:
                config = json.load(ct)
        except:
            print("No settings file was found")
            exit(1)

        try:
            cls.__instance._prefix = data["prefix"]
            cls.__instance._owners = data["owners"]
            cls.__instance._muted_role = data["muted_role"]
            cls.__instance._verified_role = data["verified_role"]
            cls.__instance._ignored_roles_levels = data["ignored_roles_levels"]
            cls.__instance._forbidden_words = data["forbidden_words"]
            cls.__instance._channels = data["channels"]
            cls.__instance._logs_settings = data["logs_settings"]
            cls.__instance._initial_roles = data["initial_roles"]
            cls.__instance._ranks = data["ranks"]
            cls.__instance._game_status = data["game_status"]
            cls.__instance._styles = data["styles"]
            cls.__instance._embeds = data["embeds"]
            cls.__instance._images_generator = data["images_generator"]
            cls._config = config
        except:
            exit(1)

        if cls.__instance._game_status == []:
            cls.__instance._game_status = ["Why i'm here ?"]

        return cls.__instance

    @property
    def prefix(self):
        return self._prefix

    @property
    def owners(self):
        return self._owners

    @property
    def muted_role(self):
        return self._muted_role

    @property
    def verified_role(self):
        return self._verified_role

    @property
    def ignored_roles_levels(self):
        return self._ignored_roles_levels

    @property
    def forbidden_words(self):
        return self._forbidden_words

    @property
    def channels(self):
        return self._channels

    @property
    def logs_settings(self):
        return self._logs_settings

    @property
    def initial_roles(self):
        return self._initial_roles

    @property
    def ranks(self):
        return self._ranks

    @property
    def game_status(self):
        return self._game_status

    @property
    def styles(self):
        return self._styles

    @property
    def embeds(self):
        return self._embeds

    @property
    def images_generator(self):
        return self._images_generator
        
    @property
    def config(self):
        return self._config