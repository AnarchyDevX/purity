import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.jailView.enable import enableButtonView
from views.jailView.disable import disableButtonJail

class jailConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="jail-config", description="Configurer la commande prison")
    async def jailconfig(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        embed = embedBuilder(
            title=f"`🔨`・Jail",
            color=embed_color(),
            footer=footer(),
            fields={
                "`🟢`・Status": (
                    '`activé`' if guildJSON['jail']['active'] == True else '`désactivé`',
                    True
                ),
                "`👑`・Role prison": (
                    f"<@&{guildJSON['jail']['role']}>",
                    True
                )
            }
        )
        view = discord.ui.View(timeout=None)
        view.add_item(enableButtonView(interaction.user.id, self.bot) if guildJSON['jail']['active'] == False else disableButtonJail(self.bot, interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(jailConfig(bot))