import json
import traceback

TEMPLATE = "database/server.template.json"
SERVERS_DATA_BASE = "database/servers.json"


def create_server():
    try:
        with open(TEMPLATE, "r") as f:
            server = json.load(f)
        return server
    except:
        traceback.print_exc()
        return None


def get_servers():
    try:
        with open(SERVERS_DATA_BASE, "r") as f:
            servers = json.load(f)
        return servers
    except:
        traceback.print_exc()
        return {}


def refresh_data(data):
    try:
        with open(SERVERS_DATA_BASE, "w") as f:
            json.dump(data, f)
    except:
        traceback.print_exc()
