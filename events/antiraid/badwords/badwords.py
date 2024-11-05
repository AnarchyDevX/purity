import asyncio
import discord
from discord.ext import commands
from functions.functions import *

class badwordsAntiraid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message, discord.Message):
            return
        if message.author.id == self.bot.user.id:
            return
        guildJSON = load_json_file(f"./configs/{message.guild.id}.json")
        if await check_id_perms(message.author, message.guild, 1): return

        if guildJSON['antiraid']['badwords'] == True:
            for element in guildJSON['badwords']:
                if element in message.content:
                    await message.delete()
                    response = await message.channel.send(f"{message.author.mention} Vous n'avez pas le droit d'utiliser ce mot ici !")
                    await asyncio.sleep(2)
                    await response.delete()
                    return
                
async def setup(bot):
    await bot.add_cog(badwordsAntiraid(bot))
