import discord
from discord.ext import commands

class botMentionned(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.user.mention in message.content:
            await message.reply(f"{message.author.mention}, tu peux afficher la liste de mes commandes avec `/help`.")

async def setup(bot):
    await bot.add_cog(botMentionned(bot))