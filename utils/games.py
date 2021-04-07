from pathlib import Path

root_dir = str(Path(__file__).parent.parent)

GAMES_PATH = f"{root_dir}/resources/games_status.md"


def load_games():
    with open(GAMES_PATH, "r") as f:
        games = f.read()
    return games.split("\n")


def dump_games(games):

    with open(GAMES_PATH, "w") as f:
        games = "\n".join(games)
        f.write(games)
