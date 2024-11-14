import random
import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class reroll(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="giveaway-reroll", description="Permet de faire un nouveau tirage d'un giveway")
    async def reroll(self, interaction: discord.Interaction, message: str, gagnants: int):
        if not await check_perms(interaction, 2): return
        try:
            message = int(message)
        except ValueError:
            return await err_embed(
                interaction,
                title="Message invalide",
                description="L'id du message que vous avez fournit est invalide."
            )
        
        message = await message.channel.fetch_message(message)
        users = 0
        for reaction in message.reactions:
            if reaction.emoji == '🎉':
                users = [user async for user in reaction.users() if user.id != self.bot.user.id]

        if len(users) < gagnants:
            return await err_embed(
                interaction,
                title="Participants insufisants",
                description="Il n'y a pas assez de participants au giveaway"
            )
        
        winners = []
        for _ in range(gagnants):
            user = random.choice(users)
            winners.append(user)
            users.remove(user)

        if gagnants == 1:
            winner = winners[0]
            return await interaction.followup.send(f"Le nouveau gagnant est {winner.mention}")
        else:
            return await interaction.followup.send(f"Les nouveaux gagnants sont {','.join(winner.mention for winner in winners)}")
        
async def setup(bot):
    await bot.add_cog(reroll(bot))