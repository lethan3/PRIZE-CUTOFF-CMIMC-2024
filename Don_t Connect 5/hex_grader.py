from hex_func import *
import importlib
import os
from os.path import abspath, dirname
import json
from pathlib import Path

os.chdir(dirname(abspath(__file__)))

# Setting

WRITE = True
NGAME = 1
DEBUG = True

# file path

directory_path = Path(__file__).parent
bot_path = directory_path / "bot"
bot_mod = "bot."
save_path = directory_path / "games"

# create save path if not exist
if not os.path.exists(save_path):
    os.makedirs(save_path)

# generate bot list
bot_list = {
    name: getattr(
        importlib.import_module(bot_mod + os.path.splitext(name)[0]),
        os.path.splitext(name)[0],
    )
    for name in os.listdir(bot_path)
    if os.path.isfile(os.path.join(bot_path, name))
}
print("Bots:", list(bot_list.keys()))
# Running

for n in range(NGAME):

    gameid = str(time.time())
    path = os.path.join(save_path, gameid + ".json")

    res = run_game(bot_list)
    res["id"] = gameid

    if WRITE:
        with open(path, "w") as writer:
            json.dump(res, writer)
