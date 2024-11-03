import discord
from discord.ext import commands
from functions.functions import *

class botJoinAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guildJSON = load_json_file(f"./configs/{member.guild.id}.json")
        if guildJSON['antiraid']['antibot'] == True:
            if member.bot:
                try: await member.ban("Antiraid: Antibot")
                except Exception: return

async def setup(bot):
    await bot.add_cog(botJoinAntiraid(bot))