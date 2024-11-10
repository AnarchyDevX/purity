import discord
from discord.ext import commands
from functions.functions import *

class deleteVoice(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel != None:
            guildJSON = load_json_file(f'./configs/{member.guild.id}.json')
            if before.channel.id in guildJSON['configuration']['tempvoices']['active'] and len(before.channel.members) == 0:
                try:
                    await before.channel.delete(reason="Tempvoice ended")
                    activeList = guildJSON['configuration']['tempvoices']['active']
                    activeList.remove(before.channel.id)
                    json.dump(guildJSON, open(f'./configs/{member.guild.id}.json', 'w'), indent=4)
                except Exception: return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(deleteVoice(bot))