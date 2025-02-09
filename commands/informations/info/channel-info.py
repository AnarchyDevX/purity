import discord
from typing import Literal
from functions.functions import *
from discord import app_commands
from discord.ext import commands
from core.embedBuilder import embedBuilder

class channelInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="channel-info", description="Obtenir les informations sur un channel")
    async def channelinfo(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel) -> None:
        await logs("channel-info", 1, interaction)
        isNsfw: Literal['oui', 'non'] = "oui" if channel.nsfw == True else "non"

        if isinstance(channel, discord.TextChannel):
            lastMessageFetched: discord.Message = await channel.fetch_message(channel.last_message_id)
            lastMessageContent: str = lastMessageFetched.content if lastMessageFetched.embeds == [] and lastMessageFetched.content != "" else "Le dernier message est un embed." 
            title: str = f"`🔎`・Informations sur le salon {channel.name}"
            description: str = f"> `➕`・**Position:** `{channel.position}`\n> `✨`・**Type:** `textuel`\n> `🔞`・**Nsfw:** `{isNsfw}`\n> `💭`・**Dernier Message:** ```{lastMessageContent}```"
        
        elif isinstance(channel, discord.VoiceChannel):
            title: str = f"`🔎`・Informations sur le salon {channel.name}"
            description: str = f"> `➕`・**Position:** `{channel.position}`\n> `🔊`・**Connectés:** `{len(channel.members)}`\n> `✨`・**Type:** `vocal`\n> `🔞`・**Nsfw:** `{isNsfw}`\n> `🔇`・**Limite:** `{channel.user_limit}`\n> `🌍`・**RTC Region:** `{channel.rtc_region}`"

        elif isinstance(channel, discord.CategoryChannel):
            title: str = f"`🔎`・Informations sur la catégorie {channel.name}"
            description: str = f"> `➕`・**Position:** `{channel.position}`\n> `📜`・**Salons Textuel:** `{len(channel.text_channels)}`\n> `🔊`・**Salons Vocal:** `{len(channel.voice_channels)}`\n> `🔇`・**Salons Conférences:** `{len(channel.stage_channels)}`"

        else:
            title: Literal['Type de salon inconnu'] = "Type de salon inconnu"
            description: Literal['Aucune informations'] = "Aucune informations"
            
        embed: embedBuilder = embedBuilder(
            title=title,
            description=f"> `🛠️`・**Nom:** `{channel.name}`\n> `🆔`・**Id:** `{channel.id}`\n> `🪄`・**Créer le:** `{format_date('all', channel.created_at)}`\n" + description,
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(channelInfo(bot))