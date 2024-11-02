import json
import discord
from discord.ext import commands
from functions.functions import *

class createVoice(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel != None:
            guildJSON = load_json_file(f'./configs/{member.guild.id}.json')
            for element in guildJSON['configuration']['tempvoices']['configs']:
                if after.channel.id == int(element):
                    category = discord.utils.get(member.guild.categories, id=guildJSON['configuration']['tempvoices']['configs'][element]['category'])
                    if category:
                        try:
                            toMoveChannel = await category.create_voice_channel(name=f"vocal-de-{member.name}")
                        except Exception: return
                        try:
                            await member.move_to(toMoveChannel)
                            activeList = guildJSON['configuration']['tempvoices']['active']
                            activeList.append(toMoveChannel.id)
                            json.dump(guildJSON, open(f'./configs/{member.guild.id}.json', 'w'), indent=4)
                        except Exception: return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(createVoice(bot))