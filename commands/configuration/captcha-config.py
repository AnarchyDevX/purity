import discord
import json
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
        message = await channel.send(embed=embed, view=view)
        
        # Sauvegarder les informations du captcha pour la persistance
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Erreur",
                description="La configuration du serveur n'a pas été trouvée.",
                ephemeral=True
            )
        
        # Initialiser la structure captcha si elle n'existe pas
        if 'captcha' not in guildJSON:
            guildJSON['captcha'] = {}
        
        # Sauvegarder les informations du captcha
        guildJSON['captcha'] = {
            'channel_id': channel.id,
            'message_id': message.id,
            'role_id': role.id
        }
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        
        # Ajouter la vue au bot pour la persistance
        self.bot.add_view(view)
        
        return await interaction.response.send_message(f"L'embed de captcha à été envoyé dans {channel.mention}", ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(captchaConfig(bot))