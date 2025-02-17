import asyncio
import discord
from discord.ext import commands, tasks

class PresenceStart(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.statusRotator.start()

    @tasks.loop(minutes=35)
    async def statusRotator(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.activity.Streaming(name=f"{len(self.bot.guilds)} servers", url="https://twitch.tv/ivyenlive"))
        await asyncio.sleep(15)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".gg/purity-dev"))
        await asyncio.sleep(15)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="73 commands"))

async def setup(bot: commands.Bot):
    await bot.add_cog(PresenceStart(bot))
