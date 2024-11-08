import requests
import discord
from typing import Dict
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class getUpdate(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.url: str = "http://154.51.39.87:20014/db/update/last"
        self.authorization: str = "Bearer 0WcTvBYRsdR0y0aUKMlN1MVl8"

    @app_commands.command(name="bot-get-update", description="Obtenir la derniere mise a jour du bot")
    async def getUpdate(self, interaction: discord.Interaction) -> None:
        req: requests.Response = requests.get(url=self.url, headers={"Authorization": self.authorization})
        if req.status_code == 200:
            response: Dict[str, str | int] = req.json()
            embed: embedBuilder = embedBuilder(
                title="`📌`・Derniere mise a jour",
                description=(
                    f"> `🪡`・**Date:** `{response[2]}`\n" 
                    f"> `✨`・**Nom:** `{response[0]}`\n"
                    f"> `🪄`・**Auteur:** `{response[3]}`\n"
                    f"> `📜`・**Message:**\n ```{response[1]}```\n"
                ),
                color=embed_color(),
                footer=footer()
            )
            return await interaction.response.send_message(embed=embed)
        else:
            return await interaction.response.send_message(content="Une erreur est survenu lors de la récupération des informations")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(getUpdate(bot))