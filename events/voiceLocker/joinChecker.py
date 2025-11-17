import discord
from discord.ext import commands
from functions.functions import *

class joinChecker(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guildJSON = load_json_file(f"./configs/{member.guild.id}.json")
        if not guildJSON:
            return
        if after.channel != None:
            if guildJSON.get('ownerlist') and member.id in guildJSON['ownerlist']:
                return
            if guildJSON.get('lockedvoice') and after.channel.id in guildJSON['lockedvoice']:
                try:
                    await member.move_to(None)
                except discord.Forbidden:
                    # Bot n'a pas les permissions
                    return
                except discord.HTTPException:
                    # Erreur Discord API
                    return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(joinChecker(bot))