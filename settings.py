import json

file_settings = "resources/settings.json"

prefix = "M"
owners = []
muted_role = None
verified_role = None
ignored_roles_levels = []
forbidden_words = []
channels = {}
logs_settings = {}
initial_roles = []
ranks = {}
styles = {}


def load_settings():

    global prefix
    global owners
    global muted_role
    global verified_role
    global ignored_roles_levels
    global forbidden_words
    global channels
    global logs_settings
    global initial_roles
    global ranks
    global styles

    try:
        with open(file_settings) as st:
            data = json.load(st)
    except:
        print("No settings file was found")
        exit(1)

    try:
        prefix = data["prefix"]
        owners = data["owners"]
        muted_role = data["muted_role"]
        verified_role = data["verified_role"]
        ignored_roles_levels = data["ignored_roles_levels"]
        forbidden_words = data["forbidden_words"]
        channels = data["channels"]
        logs_settings = data["logs_settings"]
        initial_roles = data["initial_roles"]
        ranks = data["ranks"]
        styles = data["styles"]
    except:
        exit(1)