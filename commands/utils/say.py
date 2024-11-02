from discord.ext import commands
from discord import app_commands
from functions.functions import *

class say(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="say", description="Envoyer un message via le bot")
    async def say(self, interaction: discord.Interaction, message: str) -> None:
        check: bool = await check_perms(interaction, 1)
        await logs("say", 1, interaction)
        if check == False:
            return
        
        await interaction.response.send_message('*Votre message va être envoyer avec le bot*', ephemeral=True)
        await interaction.channel.send(content=message)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(say(bot))