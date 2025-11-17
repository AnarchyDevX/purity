import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class kick(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="kick", description="Expulser un membre du serveur")
    @app_commands.choices(
        dm=[
            app_commands.Choice(name='oui', value='yes'),
            app_commands.Choice(name='non', value="no")
        ]
    )
    async def kick(self, interaction: discord.Interaction, member: discord.Member, dm: str, reason: str = None) -> None:
        check: bool = await check_perms(interaction, 1)
        await logs("kick", 1, interaction)
        if check == False:
            return
        
        if dm == "yes":
            embed = embedBuilder(
                title="`🔨`・Tu as été kick",
                description=f"*Tu as été kick du serveur **{interaction.guild.name}** par {interaction.user.mention}.*",
                color=embed_color(),
                footer=footer()
            )
            if reason:
                embed.add_field(name="`📜`・Raison de l'expulsion", value=f"*{reason}*", inline=False)
            try:
                await member.send(embed=embed)    
            except discord.Forbidden:
                # Utilisateur a ses DMs désactivés
                pass
            except discord.HTTPException as e:
                await logs(f"Erreur HTTP lors de l'envoi du DM: {e}", 4, interaction)
                
        try:
            await member.kick(reason=reason)
        except discord.Forbidden:
            await logs(f"Permissions insuffisantes pour kick {member.name}", 4, interaction)
            return await err_embed(
                interaction,
                title="Impossible d'expulser le membre",
                description=f"Je n'ai pas les permissions nécessaires pour expulser {member.mention}"
            )
        except discord.HTTPException as e:
            await logs(f"Erreur HTTP lors de l'expulsion: {e}", 4, interaction)
            return await err_embed(
                interaction,
                title="Impossible d'expulser le membre",
                description=f"Une erreur est survenue lors de l'expulsion de {member.mention}"
            )

        embed: embedBuilder = embedBuilder(
            title="`🔨`・Membre expulser",
            description=f"*Le membre {member.mention} a été expulser du serveur*",
            color=embed_color(),
            footer=footer()
        )
        if reason:
            embed.add_field(name="`📜`・Raison de l'expulsion", value=f"*{reason}*", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(kick(bot))