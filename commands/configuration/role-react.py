from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.roleReactionView.button import roleReactButton

class roleReactRemove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        
    @app_commands.command(name="role-reaction", description="Configurer et envoyé un embed de role reaction")
    async def roleReactRemove(self, interaction: discord.Interaction, role: discord.Role, channel: discord.TextChannel):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        embed = embedBuilder(
            title="`👑`・Role",
            description=f"*Merci de cliquer sur le boutton ci-dessous pour obtenir le role {role.mention}.*",
            color=embed_color(),
            footer=footer()
        )
        view = discord.ui.View(timeout=None)
        view.add_item(roleReactButton(role))
        await interaction.response.send_message(f"Le message de role reaction va être envoyé dans le salon {channel.mention}", ephemeral=True)
        return await channel.send(embed=embed, view=view)
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(roleReactRemove(bot))