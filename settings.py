import json

class Settings():
    
    def __init__(self, file_settings="resources/settings.json"):
        
        try:
            with open(file_settings) as st:
                data = json.load(st)
        except:
            print("No settings file was found")
            exit(1)

        try:
            self.prefix = data["prefix"]
            self.owners = data["owners"]
            self.muted_role = data["muted_role"]
            self.verified_role = data["verified_role"]
            self.ignored_roles_levels = data["ignored_roles_levels"]
            self.forbidden_words = data["forbidden_words"]
            self.channels = data["channels"]
            self.logs_settings = data["logs_settings"]
            self.initial_roles = data["initial_roles"]
            self.ranks = data["ranks"]
            self.game_status = data["game_status"]
            self.styles = data["styles"]
        except:
            exit(1)

        if self.game_status == []:
            self.game_status = ["Why i'm here ?"]