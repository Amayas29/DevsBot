FILE_PATH = "resources/games_status.md"


def load_games():
    with open(FILE_PATH, "r") as f:
        games = f.read()
    return games.split("\n")


def dump_games(games):

    with open(FILE_PATH, "w") as f:
        games = "\n".join(games)
        f.write(games)
