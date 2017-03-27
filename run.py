import json
from bot import Bot

if __name__ == "__main__":
    with open("configurations.json", 'r') as conF, open("secrets.json", 'r') as sF:
        configs = json.load(conF)
        secrets = json.load(sF)
    LoveBot = Bot(**secrets, configurations = configs)
    LoveBot.run()
