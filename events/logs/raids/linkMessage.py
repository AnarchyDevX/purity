import re
import discord
from typing import Pattern
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class linkMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.regex: Pattern[str] = re.compile(r'(?i)\b(?:https?://|www\.)[^\s/$.?#].[^\s]*\b')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message, discord.Message):
            return
        if message.author.id == self.bot.user.id:
            return
        if message.content.startswith("https://tenor.com/"): return
        
        # Vérifier si l'antilien est actif - si oui, ne pas logger ici (l'antilien le fera après suppression)
        guildJSON = load_json_file(f"./configs/{message.guild.id}.json")
        if guildJSON is not None:
            if guildJSON.get('antiraid', {}).get('antilien', False) == True:
                # Vérifier si l'utilisateur n'est pas exempté (si exempté, on peut logger)
                if not await check_id_perms(message.author, message.guild, 1):
                    # Antilien actif et utilisateur non exempté = l'antilien va gérer, ne pas logger ici
                    return

        logsChannel: discord.abc.GuildChannel | None = await check_if_logs(message.guild, "raidlogs") 
        if logsChannel:
            if bool(self.regex.search(message.content)) != False or "discord.gg" in message.content or ".gg/" in message.content:
                message_content_short = message.content[:1000] + '...' if len(message.content) > 1000 else message.content
                embed: embedBuilder = embedBuilder(
                    description=f"```[{time_now()}] - Raid | Message Contenant Un Lien```",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`👤`・Membre": (
                            f"{message.author.mention} (`{message.author.id}`) | Créé: `{format_date('year', message.author.created_at)}` | Rejoint: `{format_date('year', message.author.joined_at)}`",
                            False
                        ),
                        "`📝`・Message": (
                            f"Salon: {message.channel.mention} | ID: `{message.id}` | `{format_date('all', message.created_at)}`\n**Contenu:** {message_content_short}",
                            False
                        )
                    }
                )
                await logsChannel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(linkMessage(bot))