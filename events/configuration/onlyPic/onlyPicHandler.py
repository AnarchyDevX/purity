import discord
from discord.ext import commands
from functions.functions import *

class onlyPicHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message, discord.Message): return
        if message.author.id == self.bot.user.id: return
        guildJSON = load_json_file(f"./configs/{message.guild.id}.json")
        if await check_id_perms(message.author, message.guild, 1): return
        if message.channel.id not in guildJSON['onlypic']: return
        if message.attachments == []: await message.delete()

async def setup(bot):
    await bot.add_cog(onlyPicHandler(bot))