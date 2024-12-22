import requests
import discord
from typing import Dict
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class getUpdate(commands.Cog):
    def __init__(self) -> None:
        self.url: str = "http://51.91.209.135:420/db/update/last"
        self.authorization: str = "Bearer quAyyD4uhz6ogkkZOZfVxYHXT"

    def main(self):
        req: requests.Response = requests.get(url=self.url, headers={"Authorization": self.authorization})
        if req.status_code == 200:
            print(req.status_code)
            print(req.json())

a = getUpdate()
a.main()