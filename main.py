# Developed by scarlxrd
import discord
from core._colors import Colors
from discord.ext import commands
from functions.functions import load_json

class MyBot(commands.Bot):
    def __init__(self) -> None:
        self.C = Colors()
        super().__init__(
            command_prefix="noprefix", # you can define a prefix using config['prefix'] (also add it into config.json)
            intents=discord.Intents.all(),
            help_command=None
        )

    async def setup_hook(self):
        await self.load_extension("events.utils.ready")
        
config = load_json()
client = MyBot()
client.run(config['token'])