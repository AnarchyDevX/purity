import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from discord import app_commands
from views.captchaView.verify import startVerify

class captchaConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="captcha-config",  description=f"Configurer le systeme de captcha")
    async def captchaconfig(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
        if not await check_perms(interaction, 2): return

        embed = embedBuilder(
            title=f"`🛡️`・Captcha - {interaction.guild.name}",
            description=f"*Merci de cliquer sur le bouton ci-dessous pour valider le captcha*",
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(startVerify(self.bot, role))
        await channel.send(embed=embed, view=view)
        return await interaction.response.send_message(f"L'embed de captcha à été envoyé dans {channel.mention}", ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(captchaConfig(bot))