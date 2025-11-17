import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class robloxConfig(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="roblox-config", description="Configurer la vérification Roblox")
    @app_commands.choices(
        action=[
            app_commands.Choice(name="Activer", value="enable"),
            app_commands.Choice(name="Désactiver", value="disable"),
            app_commands.Choice(name="Configurer le rôle", value="role")
        ]
    )
    async def robloxconfig(self, interaction: discord.Interaction, action: str, role: discord.Role = None):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration de ce serveur n'existe pas."
            )
        
        if action == "enable":
            if role is None:
                return await err_embed(
                    interaction,
                    title="Rôle requis",
                    description="Veuillez spécifier un rôle à attribuer lors de la vérification."
                )
            
            guildJSON['roblox_verification']['active'] = True
            guildJSON['roblox_verification']['role'] = role.id
            
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
            
            embed = embedBuilder(
                title="`✅`・Vérification Roblox activée",
                description=f"*La vérification Roblox a été activée avec succès.*\n*Rôle attribué: {role.mention}*",
                color=embed_color(),
                footer=footer()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        elif action == "disable":
            guildJSON['roblox_verification']['active'] = False
            
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
            
            embed = embedBuilder(
                title="`❌`・Vérification Roblox désactivée",
                description=f"*La vérification Roblox a été désactivée avec succès.*",
                color=embed_color(),
                footer=footer()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        elif action == "role":
            if role is None:
                return await err_embed(
                    interaction,
                    title="Rôle requis",
                    description="Veuillez spécifier un rôle."
                )
            
            guildJSON['roblox_verification']['role'] = role.id
            
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
            
            embed = embedBuilder(
                title="`🪄`・Rôle configuré",
                description=f"*Le rôle de vérification a été configuré sur: {role.mention}*",
                color=embed_color(),
                footer=footer()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(robloxConfig(bot))

