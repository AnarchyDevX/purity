import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class highMentionMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if "@everyone" in message.content or "@here" in message.content:
            logsChannel: discord.abc.GuildChannel | None = await check_if_logs(message.guild, 'raidlogs')
            if logsChannel:
                embed: embedBuilder = embedBuilder(
                    description=f"```[{time_now()}] - Raid | Message Contenant Un Mention Sensible```",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`🪡`・Informations sur le membre": (
                            f"> `🪄`・**Nom:** `{message.author.name}`\n"
                            f"> `🆔`・**Id:** `{message.author.id}`\n"
                            f"> `✨`・**Mention:** {message.author.mention}\n"
                            f"> `🔨`・**Créé le:** `{format_date('all', message.author.created_at)}`\n"
                            f"> `➕`・**Rejoint le:** `{format_date('all', message.author.joined_at)}`\n",
                            False
                        ),
                        "`✨`・Informations sur le message": (
                            f"> `🪄`・**Salon:** {message.channel.mention}\n"
                            f"> `🆔`・**Id:** `{message.id}`\n"
                            f"> `➕`・**Envoyée le:** `{format_date('all', message.created_at)}`\n",
                            False
                        )
                    }
                )
                embedContent: embedBuilder = embedBuilder(
                    title="`🛠️`・Contenu du message contenant la mention",
                    description=message.content,
                    color=embed_color()
                )
                await logsChannel.send(embeds=[embed, embedContent])

async def setup(bot: commands.Bot):
    await bot.add_cog(highMentionMessage(bot))
