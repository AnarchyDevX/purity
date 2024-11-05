import os
import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *

class GuildRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        os.remove(f'./configs/{guild.id}.json')
        return
    
async def setup(bot):
    await bot.add_cog(GuildRemove(bot))