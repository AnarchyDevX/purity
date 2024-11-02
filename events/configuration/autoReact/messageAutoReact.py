import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *

class messageAutoReact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message, discord.Message):
            return
        if message.author.id == self.bot.user.id:
            return
        
        guildJSON = load_json_file(f'./configs/{message.guild.id}.json')
        for element in guildJSON['configuration']['autoreact']:
            if guildJSON['configuration']['autoreact'][element]['channel'] == message.channel.id:
                if guildJSON['configuration']['autoreact'][element]['content'] in message.content:
                    react = discord.utils.get(message.guild.emojis, id=int(element))
                    if react:
                        await message.add_reaction(react)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(messageAutoReact(bot))