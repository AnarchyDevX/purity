import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class channelRename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="channel-rename", description="Renommer un salon du serveur")
    async def channelRename(self, interaction: discord.Interaction, channel: discord.TextChannel | discord.VoiceChannel, name: str):
        if not await check_perms(interaction, 2):
            return
        oldName = channel.name
        if isinstance(channel, discord.TextChannel):
            try: await channel.edit(name=name)
            except Exception: return await err_embed(
                interaction,
                title="Impossible de renommer le salon",
                description=f"Je n'ai pas réussi a renomme le salon {channel.name}"
            )
        elif isinstance(channel, discord.VoiceChannel):
            try: await channel.edit(name=name)
            except Exception: return await err_embed(
                interaction,
                title="Impossible de renommer le salon",
                description=f"Je n'ai pas réussi a renomme le salon {channel.name}"
            )

        embed = embedBuilder(
            title="`🔨`・Salon renommé",
            description=f"*Le salon {channel.mention} a changer de nom. `{oldName} => {name}`*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(channelRename(bot))        