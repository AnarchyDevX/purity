import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class serverInvite(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="serveur-invite", description="Afficher l'invitation définitive du serveur")
    async def serverInvite(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer()
        link = None
        if interaction.guild.premium_subscription_count >= 14:
            link = interaction.guild.vanity_invite
        else:
            try: invite = await channel.create_invite()
            except Exception: return await err_embed(interaction, title="Impossible de crée l'invitation", description=f"Je n'ai pas reussi a crée d'invitation pour le salon {channel.mention}", followup=True)
            link = invite.url

        embed: embedBuilder = embedBuilder(
            title="`🪼`・Invitation du serveur",
            description=f"*Voici l'invitation permanente du serveur: {link}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(serverInvite(bot))