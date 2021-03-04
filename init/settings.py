import json
                                                     

class Settings():
    
    __instance = None

    def __new__(cls, file_settings="resources/settings.json") :

        if cls.__instance is None :
            cls.__instance = object.__new__(cls)

            try:
                with open(file_settings) as st:
                    data = json.load(st)
            except:
                print("No settings file was found")
                exit(1)

            try:
                cls.__instance.prefix = data["prefix"]
                cls.__instance.owners = data["owners"]
                cls.__instance.muted_role = data["muted_role"]
                cls.__instance.verified_role = data["verified_role"]
                cls.__instance.ignored_roles_levels = data["ignored_roles_levels"]
                cls.__instance.forbidden_words = data["forbidden_words"]
                cls.__instance.channels = data["channels"]
                cls.__instance.logs_settings = data["logs_settings"]
                cls.__instance.initial_roles = data["initial_roles"]
                cls.__instance.ranks = data["ranks"]
                cls.__instance.game_status = data["game_status"]
                cls.__instance.styles = data["styles"]
            except:
                exit(1)

        if cls.__instance.game_status == []:
            cls.__instance.game_status = ["Why i'm here ?"]

        return cls.__instance