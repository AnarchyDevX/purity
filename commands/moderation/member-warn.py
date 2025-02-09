import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class memberWarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="warn-member", description="Afficher les informations de warn sur un membre")
    async def warnmember(self, interaction: discord.Interaction, member: discord.Member):
        check = await check_perms(interaction, 1)
        if check == False:
            return

        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        try:
            memberConfig = guildJSON['warndb']['users'][str(member.id)]
        except KeyError:
            return await err_embed(
                interaction,
                title="Membre sans warn",
                description=f"Le membre {member.mention} n'as aucun warn pour le moment"
            )
        
        warnsList = [
            f"> `🛑`・**Warn le:** `{item['date']}`\n"
            f"> `📜`・**Raison:** `{item['reason']}`\n"
            f"> `👘`・**Par:** <@{item['moderator']}>\n"
            for data, item in memberConfig.items()
        ]

        embed = embedBuilder(
            title=f"`🥏`・Informations sur les warns de {member.name}",
            description=f"\n".join(warnsList),
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(memberWarn(bot))