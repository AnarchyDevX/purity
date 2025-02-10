import asyncio
import discord
from discord.ext import commands
from functions.functions import *

class ghostpingMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messagesList = []
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guildJSON = load_json_file(f"./configs/{member.guild.id}.json")
        for channelId in guildJSON['ghostping']:
            channel = member.guild.get_channel(channelId)
            if channel:
                try:
                    message = await channel.send(member.mention)
                    self.messagesList.append(message)
                except Exception:
                    continue

        await asyncio.sleep(3)
        for message in self.messagesList:
            try:
                await message.delete()
            except Exception:
                continue

async def setup(bot):
    await bot.add_cog(ghostpingMemberJoin(bot))
