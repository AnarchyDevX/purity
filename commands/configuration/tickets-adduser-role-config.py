import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json

class ticketsAddUserRoleConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ticket-adduser-role-config", description="Définir le rôle autorisé à utiliser /add user")
    @app_commands.describe(role="Le rôle qui pourra ajouter des membres aux tickets (laisser vide pour réinitialiser)")
    async def ticketAddUserRoleConfig(self, interaction: discord.Interaction, role: discord.Role = None):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration du serveur n'existe pas."
            )
        
        # Initialiser la structure si nécessaire
        if 'tickets' not in guildJSON:
            guildJSON['tickets'] = {
                "logs": None,
                "transcripts": True,
                "roles": [],
                "claim": True,
                "buttons": {},
                "categories": {
                    "nouveaux": None,
                    "pris_en_charge": None,
                    "en_pause": None,
                    "fermes": None
                },
                "add_user_role": None
            }
        
        # Sauvegarder le rôle (ou None pour réinitialiser)
        guildJSON['tickets']['add_user_role'] = role.id if role else None
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
        
        if role:
            embed = embedBuilder(
                title="`✅`・Rôle configuré",
                description=f"Le rôle {role.mention} peut maintenant utiliser la commande `/add` pour ajouter des membres aux tickets.\n\n**Note :** Les administrateurs et le rôle staff des tickets peuvent toujours utiliser cette commande.",
                color=embed_color(),
                footer=footer()
            )
        else:
            embed = embedBuilder(
                title="`✅`・Rôle réinitialisé",
                description="Le rôle autorisé à utiliser `/add` a été réinitialisé.\n\nSeuls les administrateurs et le rôle staff des tickets peuvent maintenant utiliser cette commande.",
                color=embed_color(),
                footer=footer()
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ticketsAddUserRoleConfig(bot))

