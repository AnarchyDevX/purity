import discord
from discord.ext import commands
from functions.functions import *

class greetMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guildJSON = load_json_file(f"./configs/{member.guild.id}.json")
        if guildJSON['greetmsg']["alive"] == True:
            if guildJSON['greetmsg']['content'] != "":
                try:
                    await member.send(guildJSON['greetmsg']['content'])
                except Exception:
                    pass

async def setup(bot):
    await bot.add_cog(greetMessageEvent(bot))