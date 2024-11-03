import json
from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class badWordsListener(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if not isinstance(message, discord.Message):
            return
        badwordsJSON = json.load(open(f'./configs/{message.guild.id}.json', 'r'))
        badwordsList = badwordsJSON['badwords']
        if badwordsList == []:
            return
        logsChannel = await check_if_logs(message.guild, 'modlogs')
        if logsChannel != None:
            for badwords in badwordsList:
                if badwords in message.content:
                    embed = embedBuilder(
                        description=f"```[{time_now()}] - Mods | Message Contenant Un Badword```",
                        color=embed_color(),
                        footer=footer(),
                        fields={
                            "`🪡`・Informations sur le membre:": (
                                f"> `🪄`・**Nom:** `{message.author.name}`\n"
                                f"> `🆔`・**Id:** `{message.author.id}`\n"
                                f"> `✨`・**Mention:** {message.author.mention}\n"
                                f"> `🔨`・**Créé le:** `{format_date('all', message.author.created_at)}`\n"
                                f"> `➕`・**Rejoint le:** `{format_date('all', message.author.joined_at)}`",
                                False
                            ),
                            "`✨`・Informations sur le badword:": (
                                f"> `🎯`・**Badword Ciblé:** `{badwords}`\n"
                                f"> `🆔`・**Id:** `{message.id}`\n"
                                f"> `✨`・**Channel:** {message.channel.mention}\n"
                                f"> `📜`・**Conten du Message:**\n"
                                f"```{message.content}```",
                                False
                            ),
                        }
                    )
                    await logsChannel.send(embed=embed)
                    break

async def setup(bot):
    await bot.add_cog(badWordsListener(bot))