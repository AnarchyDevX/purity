import json
from discord.ext import commands
from functions.functions import *
from datetime import timedelta
from core.embedBuilder import embedBuilder

class messageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if message.content == "" and message.embeds != []:
            return
        logsChannel = await check_if_logs(message.guild, 'msglogs')
        if logsChannel:
            embedInformations = embedBuilder(
                description=f"```[{time_now()}] - Messages | Message Supprimé ```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Auteur du message:": (
                        f"> `🪄`・**Nom:** `{message.author.name}`\n"
                        f"> `✨`・**Mention:** {message.author.mention}\n"
                        f"> `🆔`・**Id:** `{message.author.id}`\n"
                        f"> `🪄`・**Créé le:** `{format_date('all', message.author.created_at)}`\n"
                        f"> `➕`・**Rejoint le:** `{format_date('all', message.author.joined_at)}`",
                        False
                    ),
                    "`✨`・Informations sur le message:": (
                        f"> `🆔`・**Id:** `{message.id}`\n"
                        f"> `🪄`・**Salon:** {message.channel.mention}\n"
                        f"> `✨`・**Envoyé Ppar:** {message.author.mention}\n"
                        f"> `➕`・**Envoyé le:** `{format_date('all', message.created_at)}`",
                        False
                    ),
                }
            )

            embedMessageContent = embedBuilder(
                title="`🛠️`・Contenu du message",
                description=message.content,
                color=embed_color()
            )
            async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                is_recent = discord.utils.utcnow() - entry.created_at < timedelta(seconds=3)
                if entry.target.id == message.author.id and entry.extra.channel.id == message.channel.id and is_recent:
                    embedInformations.add_field(
                        name="`🛠️`・Membre ayant supprimé le message:",
                        value=(
                            f"> `🪄`・**Nom:** `{entry.user.name}`\n"
                            f"> `✨`・**Mention:** {entry.user.mention}\n"
                            f"> `🆔`・**Id:** `{entry.user.id}`\n"
                            f"> `🪄`・**Créé le:** `{format_date('all', entry.user.created_at)}`"
                        ),
                        inline=False
                    )
                    break
            await logsChannel.send(embeds=[embedInformations, embedMessageContent])

async def setup(bot):
    await bot.add_cog(messageDelete(bot))