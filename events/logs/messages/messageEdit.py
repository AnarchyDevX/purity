import json
from functions.functions import *
from discord.ext import commands
from core.embedBuilder import embedBuilder

class messageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.id == self.bot.user.id:
            return
        if before.embeds == [] and after.embeds != []:
            return
        if before.embeds != []:
            return
        logsChannel = await check_if_logs(before.guild, 'msglogs')
        if logsChannel != None:
            embed = embedBuilder(
                description=f"```[{time_now()}] - Messages | Message Modifié```",
                color=embed_color(),
                footer=footer(),
                fields={
                    "`🪡`・Auteur du message:": (
                        f"> `🪄`・**Nom:** `{before.author.name}`\n"
                        f"> `✨`・**Mention:** {before.author.mention}\n"
                        f"> `🆔`・**Id:** `{before.author.id}`\n"
                        f"> `🪄`・**Créé le:** `{format_date('all', before.author.created_at)}`\n"
                        f"> `➕`・**Rejoint le:** `{format_date('all', after.author.joined_at)}`",
                        False
                    ),
                    "`✨`・Informations sur le message:": (
                        f"> `🆔`・**Id:** `{after.id}`\n"
                        f"> `🪄`・**Salon:** {after.channel.mention}\n"
                        f"> `✨`・**Envoyé par:** {after.author.mention}\n"
                        f"> `➕`・**Envoyé le:** `{format_date('all', after.created_at)}`",
                        False
                    ),
                }
            )
            embedBefore = embedBuilder(
                title="`🛠️`・Contenu du message avant la modification",
                description=before.content,
                color=embed_color()
            )
            embedAfter = embedBuilder(
                title="`🛠️`・Contenu du message après la modification", 
                description=after.content,
                color=embed_color()
            )       
            await logsChannel.send(embeds=[embed, embedBefore, embedAfter])     
async def setup(bot):
    await bot.add_cog(messageEdit(bot))