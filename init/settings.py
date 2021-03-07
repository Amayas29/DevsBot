import json
from os import sep
import re
from sys import prefix


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
            cls.__instance.file_settings = file_settings
            cls.__instance.file_config = file_config
            cls.__instance._prefix = data["prefix"]
            cls.__instance._owners = data["owners"]
            cls.__instance._muted_role = data["muted_role"]
            cls.__instance._verified_role = data["verified_role"]
            cls.__instance._ignored_roles_levels = data["ignored_roles_levels"]
            cls.__instance._forbidden_words = data["forbidden_words"]
            cls.__instance._verification_message = data["verification_message"]
            cls.__instance._verification_emoji = data["verification_emoji"]      
            cls.__instance._channels = data["channels"]
            cls.__instance._logs_settings = data["logs_settings"]
            cls.__instance._initial_roles = data["initial_roles"]
            cls.__instance._ranks = data["ranks"]
            cls.__instance._game_status = data["game_status"]
            cls.__instance._styles = data["styles"]
            cls.__instance._embeds = data["embeds"]
            cls.__instance._images_generator = data["images_generator"]
            cls.__instance._ignored_roles_display = data["ignored_roles_display"]
            cls.__instance._level_up_message = data["level_up_message"]
            cls.__instance._min_time = data["min_time"]
            cls._config = config
        except:
            exit(1)

        if cls.__instance._game_status == []:
            cls.__instance._game_status = ["Why i'm here ?"]

        return cls.__instance


    def refresh_data(self):
        try:
            with open(self.file_settings) as st:
                data = json.load(st)

            data["prefix"] = self._prefix
            data["owners"] = self._owners
            data["muted_role"] = self._muted_role
            data["verified_role"] = self._verified_role
            data["ignored_roles_levels"] = self._ignored_roles_levels
            data["forbidden_words"] = self._forbidden_words
            data["verification_message"] = self._verification_message
            data["verification_emoji"] = self._verification_emoji      
            data["channels"] = self._channels
            data["logs_settings"] = self._logs_settings
            data["initial_roles"] = self._initial_roles
            data["ranks"] = self._ranks
            data["game_status"] = self._game_status
            data["styles"] = self._styles
            data["embeds"] = self._embeds
            data["images_generator"] = self._images_generator
            data["ignored_roles_display"] = self._ignored_roles_display
            data["level_up_message"] = self._level_up_message
            data["min_time"] = self._min_time
            
            with open(self.file_settings, "w") as file:
                json.dump(data, file ,indent=4)

        except:
            pass


    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        if value != None and value != "":
            self._prefix = value

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
    def verification_message(self):
        return self._verification_message

    @verification_message.setter
    def verification_message(self, value):
        self._verification_message = value

    @property
    def verification_emoji(self):
        return self._verification_emoji

    @verification_emoji.setter
    def verification_emoji(self, value):
        self._verification_emoji = value

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
    def ignored_roles_display(self):
        return self._ignored_roles_display
    
    @property
    def level_up_message(self):
        return self._level_up_message

    @property
    def min_time(self):
        return self._min_time
        
    @property
    def config(self):
        return self._config