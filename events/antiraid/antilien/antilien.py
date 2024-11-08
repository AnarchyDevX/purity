import re
import discord
from discord.ext import commands
from functions.functions import *
from datetime import timedelta

class antilienAntiraid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.linkRegex = r"(https?://[^\s]+)"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message, discord.Message): return
        if message.author.id == self.bot.user.id: return
        if message.content.startswith("https://tenor.com/"): return
        guildJSON = load_json_file(f"./configs/{message.guild.id}.json")
        if await check_id_perms(message.author, message.guild, 1): return
        if guildJSON['antiraid']['antilien'] == True:
            if bool(re.search(self.linkRegex, message.content)) == True:
                try: await message.delete()
                except Exception: pass
                try: 
                    await message.author.timeout(discord.utils.utcnow() + timedelta(minutes=1))
                except Exception: pass
            
async def setup(bot):
    await bot.add_cog(antilienAntiraid(bot))