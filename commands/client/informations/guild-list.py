import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guilds(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="serveur-list", description="Afficher tous les serveurs où le bot est présent")
    async def allGuilds(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 3): return
        
        guildList: list[str] = [
            f'> `🛠️`・**Nom:** `{guild.name}`\n'
            f"> `🆔`・**Id:** `{guild.id}`\n"
            f"> `💈`・**Membres:** `{guild.member_count}`\n"
            f"> `🪄`・**Crée le:** `{format_date('all', guild.created_at)}`\n"
            f"> `✨`・**Owner:** {guild.owner.mention}`{guild.id}`\n" 
            for guild in self.bot.guilds
        ]
        
        embed: embedBuilder = embedBuilder(
            title="`✨`・Liste des serveurs",
            description='\n'.join(guildList),
            color=embed_color(),
            footer=footer()
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(guilds(bot))