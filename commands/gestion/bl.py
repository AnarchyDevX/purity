import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class blackList(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="blacklist", description="Permet de bannir tout le membre de tout les serveurs ou est present le bot")
    async def bl(self, interaction: discord.Interaction, member: discord.Member):
        if not await check_perms(interaction, 3):
            return
        await interaction.response.defer()
        g = 0
        f = 0
        for guild in self.bot.guilds:
            if member in guild.members:
                try:
                    await guild.ban(member)
                    g += 1
                except discord.Forbidden:
                    # Bot n'a pas les permissions
                    f += 1
                    continue
                except discord.HTTPException:
                    # Erreur Discord API
                    f += 1
                    continue
                except discord.NotFound:
                    # Membre déjà banni
                    f += 1
                    continue
        
        embed = embedBuilder(
            title="`🔨`・Blacklist",
            description=f"*Le membre {member.mention} a été blacklist *\n\n`🟢`・*Banni de `{g}` serveurs*\n`🔴`・*Non banni de `{f}` serveurs*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(blackList(bot))