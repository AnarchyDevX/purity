import discord
from typing import List
from discord.ext import commands
from core._colors import Colors
from loaders.commandsLoader import commandsLoader
from loaders.eventsLoader import eventsLoader

class ready(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.C: Colors = Colors()

    async def commands_load(self):
        a: commandsLoader = commandsLoader(self.bot)
        await a.load_commands()

    async def events_load(self):
        a: eventsLoader = eventsLoader(self.bot)
        eventsCount = await a.load_events()
        return eventsCount

    async def commands_count(self, commandsList: List[discord.app_commands.Command]):
        commandsCount = sum(1 for _ in commandsList)
        return commandsCount

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"{self.C.YELLOW}[UPDATING] {self.C.WHITE}Loading commands...")
        await self.commands_load()
        eventsCount = await self.events_load()
        print(f"{self.C.GREEN}[SUCCESS] {self.C.WHITE}Commands loaded !")
        print(f"{self.C.YELLOW}[UPDATING] {self.C.WHITE}Syncing commands...")
        await self.bot.tree.sync()
        print(f"{self.C.GREEN}[SUCCESS] {self.C.WHITE}Commands synced !")
        print(f"{self.C.BLUE}[LOGGED] {self.C.WHITE}Logged as {self.bot.user.name} | {self.bot.user.id}")
        cCount = await self.commands_count(self.bot.tree.walk_commands())
        print(f"{self.C.RED}[INFO] {self.C.WHITE}Commands loaded: {cCount}")
        print(f"{self.C.RED}[INFO] {self.C.WHITE}Events loaded: {eventsCount}")

async def setup(bot):
    await bot.add_cog(ready(bot))