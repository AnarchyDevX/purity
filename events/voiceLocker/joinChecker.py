import discord
from discord.ext import commands
from functions.functions import *

class joinChecker(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guildJSON = load_json_file(f"./configs/{member.guild.id}.json")
        if after.channel != None:
            if after.channel.id in guildJSON['lockedvoice']:
                try: await member.move_to(None)
                except Exception: return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(joinChecker(bot))