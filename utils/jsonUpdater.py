import json
import os

def main():
    for file in os.listdir("./configs/"):
        configFile = json.load(open(f"./configs/{file}", 'r'))
        configFile['compteurs'] = {}
        json.dump(configFile, open(f"./configs/{file}", 'w'), indent=4)
        print(file + " updated")

main()