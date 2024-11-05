import time
import random
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta, datetime
from functions.functions import *
from core.embedBuilder import embedBuilder

class gstart(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="giveaway-start", description="Commencer la configuration d'un giveaway")
    @app_commands.choices(
        unit=[
            app_commands.Choice(name="secondes", value="sec"),
            app_commands.Choice(name="minutes", value="min"),
            app_commands.Choice(name="heure", value="hour"),
            app_commands.Choice(name="jours", value="day"),
            app_commands.Choice(name="semaine", value="week")
        ]
    )
    async def gstar(self, interaction: discord.Interaction, gain: str, temps: int, unit: str, gagnants: int, by: discord.Member = None, condition: str = None):
        await interaction.response.defer()
        timeToAdd = None
        toWait = 0
        now = datetime.now()
        if unit == "sec":
            timeToAdd = now + timedelta(seconds=temps)
            toWait = temps 
        elif unit == "min":
            timeToAdd = now + timedelta(minutes=temps)
            toWait = temps * 60
        elif unit == "hour":
            timeToAdd = now + timedelta(hours=temps)
            toWait = temps * 60 * 60
        elif unit == "day":
            timeToAdd = now + timedelta(days=temps)
            toWait = temps * 60 * 60 * 24
        elif unit == "week":
            toWait = temps * 60 * 60 * 24 * 7
            timeToAdd = now + timedelta(weeks=temps)

        timestamp  = round(timeToAdd.timestamp())
        
        embed = embedBuilder(
            title=f"`🎉`・{gain}",
            description=f"*Se termine:* <t:{timestamp}:F>\n*Temps restant:* <t:{timestamp}:R>",
            color=embed_color(),
            footer=footer()
        )
        if by:
            embed.add_field(
                name=f"`🥏`・Par",
                value=f"{by.mention}",
                inline=False
            )
        if condition:
            embed.add_field(
                name="`🪄`・Condition",
                value=f"*{condition}*",
                inline=False
            )
        message: discord.Message = await interaction.followup.send(embed=embed)
        await message.add_reaction('🎉')
        await asyncio.sleep(toWait)
        message = await message.channel.fetch_message(message.id)
        for reaction in message.reactions:
            if reaction.emoji == '🎉':
                users = [user async for user in reaction.users() if user.id != self.bot.user.id]

        winners = []
        for _ in range(gagnants):
            user = random.choice(users)
            winners.append(user)
            users.remove(user)

        if gagnants == 1:
            winner = winners[0]
            return await interaction.followup.send(f"Le gagnant est {winner.mention} ! Il remporte donc ***{gain}***")
        else:
            return await interaction.followup.send(f"Les gagnants sont {','.join(winner.mention for winner in winners)} ! Ils remportent donc ***{gain}***")

async def setup(bot):
    await bot.add_cog(gstart(bot))