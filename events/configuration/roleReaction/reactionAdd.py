import discord
from discord.ext import commands
from functions.functions import *

class reactionAddRole(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        guildJSON = load_json_file(f"./configs/{payload.guild_id}.json")
        for element in guildJSON['configuration']['rolereact']:
            reactConfig = guildJSON['configuration']['rolereact'][element]
            if int(element) == payload.message_id:
                if reactConfig['emojiId'] == payload.emoji.id:
                    guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)
                    if guild:
                        role = discord.utils.get(guild.roles, id=reactConfig['roleId'])
                        if role:
                            try:
                                await payload.member.add_roles(role)
                            except Exception as e:
                                return

async def setup(bot: commands.Bot):
    await bot.add_cog(reactionAddRole(bot))