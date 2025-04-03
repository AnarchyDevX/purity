import json
import os

for file in os.listdir("./configs"):
    with open(f"./configs/{file}", "r") as f:
        data = json.load(f)
        data["greeting"]["message"] = ""
        with open(f"./configs/{file}", "w") as f:
            json.dump(data, f, indent=4)

