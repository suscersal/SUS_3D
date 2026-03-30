import json
from messanges import *

def load_cfg():
    with open("config.txt","r") as file:
        # print(json.load(file))
        try:
            # data = json.load(file)
            # data=int(data)
            return int(file.read())
        except Exception as e:
            error(f"ERROR loading config! ERROR: {e}")
            return 1