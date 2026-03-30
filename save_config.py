import json

def save_cfg(data):
    with open("config.txt","w") as file:
        file.write(str(data))