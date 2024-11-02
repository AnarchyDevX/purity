import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class ban(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="ban", description="Bannir un membre du serveur")
    @app_commands.choices(
        dm=[
            app_commands.Choice(name='oui', value='yes'),
            app_commands.Choice(name='non', value="no")
        ]
    )
    async def ban(self, interaction: discord.Interaction, member: discord.Member, dm: str, reason: str = None) -> None:
        check: bool = await check_perms(interaction, 1)
        await logs("ban", 1, interaction)
        if check == False:
            return
        
        if dm == "yes":
            embed: embedBuilder = embedBuilder(
                title="`🔨`・Tu as été banni",
                description=f"*Tu as été banni du serveur **{interaction.guild.name}** par {interaction.user.mention}.*",
                color=embed_color(),
                footer=footer()
            )
            if reason:
                embed.add_field(name="`📜`・Raison du bannisement", value=f"*{reason}*", inline=False)
            try:
                await member.send(embed=embed)    
            except Exception as e:
                print(e)
                await logs(e, 4, interaction)
        
        try:
            await member.ban(reason=reason, delete_message_days=7)
        except Exception as e:
            await logs(e, 4, interaction)
            
            return await err_embed(
                interaction,
                title="Impossible de bannir le membre",
                description=f"Je n'ai pas réussi à bannir le membre {member.mention}"
            )
        

        embed: embedBuilder = embedBuilder(
            title="`🔨`・Membre banni",
            description=f"*Le membre {member.mention} a été banni du serveur et tout ses messages depuis les 7 derniers jours ont été supprimés*",
            color=embed_color(),
            footer=footer()
        )
        if reason:
            embed.add_field(name="`📜`・Raison du bannisement", value=f"*{reason}*", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ban(bot))