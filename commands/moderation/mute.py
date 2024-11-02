import discord
from datetime import timedelta
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class mute(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="mute", description="Permet de rendre muet un utilisateur")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None) -> None:
        check: bool = await check_perms(interaction, 1)
        await logs("mute", 1, interaction)
        if check == False:
            return

        try:
            await member.timeout(discord.utils.utcnow() + timedelta(minutes=duration), reason=reason)
        except Exception as e:
            await logs(e, 4, interaction)
            return await err_embed(
                interaction,
                title="Impossible de rendre le membre muet",
                description=f"Je n'ai pas réussi à rendre muet le membre {member.mention}"
            )

        embed: embedBuilder = embedBuilder(
            title="`✅`・Membre rendu muet",
            description=f"*Le membre {member.mention} a été rendu muet pendant `{duration} minutes`*",
            color=embed_color(),
            footer=footer()
        )
        if reason:
            embed.add_field(name="`📜`・Raison du mute", value=f"*{reason}*", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(mute(bot))