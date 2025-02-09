import discord
from typing import Literal
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class memberInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="member-info", description="Avoir des informations sur un membre du serveur")
    async def member_info(self, interaction: discord.Interaction, member: discord.Member) -> None:
        await logs("member-info", 1, interaction)
        isVoice: str = member.voice.channel.mention if member.voice else "`non connecter`"
        isBot: Literal['oui', 'non'] = "oui" if member.bot else "non"

        description: str = f"""
> `✨`・**Nom:** `{member.name}`
> `🆔`・**Id:** `{member.id}`
> `🛠️`・**Mention:** {member.mention}
> `👤`・**Robot:** `{isBot}`
> `🌍`・**Nom Global:** `{member.global_name}`
> `➕`・**Discriminateur:** `{member.discriminator}`
> `🪄`・**Créer le:** `{format_date('all', member.created_at)}`
> `🔊`・**En vocal:** {isVoice}
"""     
        embed: embedBuilder = embedBuilder(
            title=f"`🔎`・Informations sur {member.name}",
            description=description,
            color=member.color,
            footer=footer()
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(memberInfo(bot))