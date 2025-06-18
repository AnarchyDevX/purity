import discord
import os
from discord.ext import commands
from discord import app_commands
from typing import Union
from functions.functions import *
from core.embedBuilder import embedBuilder

class backupCreate(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="backup-create", description="Crée une backup d'un serveur et l'enregistrer dans le bot")
    async def backupCreate(self, interaction: discord.Interaction, name: str):
        if not await check_perms(interaction, 3): return

        if os.path.exists(f'./backups/{name}.json'):
            return await err_embed(
                interaction,
                title="Backup existante",
                description=f"L'id de backup que vous voulez definir existe deja."
            )
        
        pfp = interaction.guild.icon.url if interaction.guild.icon != None else "rien"
        banner = interaction.guild.banner.url if interaction.guild.banner != None else "rien"
        basedConfig = {
            "name": interaction.guild.name,
            "pfp": pfp,
            "banner": banner,
            "roles": {},
            "categories": {}
        }
        with open(f"./backups/{name}.json", 'w') as f:
            json.dump(basedConfig, f, indent=4)
            
        backupJSON = load_json_file(f"./backups/{name}.json")

        pl1  = {}
        backupJSON['name'] = interaction.guild.name
        for role in interaction.guild.roles:
            r, g, b = role.colour.to_rgb()
            hex_color = f"{r:02x}{g:02x}{b:02x}"
            pl = {
                "name": role.name,
                "permission": role.permissions.value,
                "color": hex_color
            }
            pl1[str(role.id)] = pl
        backupJSON['roles'] = pl1

        def serialize_permissions(overwrite: discord.PermissionOverwrite):
            perms = {}
            for perm, value in overwrite:
                if value is not None:
                    perms[perm] = value
            return perms

        plCategories = {}
        for category in interaction.guild.categories:
            categoryPls = {
                "overwrites": {}  
            }
            for target, overwrite in category.overwrites.items():
                categoryPls["overwrites"][str(target.name)] = {
                    "type": "role" if isinstance(target, discord.Role) else "member",
                    "perms": serialize_permissions(overwrite)
                }
            for channel in category.channels:
                channelPL = {
                    "name": channel.name,
                    "type": channel.type.name,
                    "perms": {}
                }
                for target, overwrite in channel.overwrites.items():
                    channelPL["perms"][str(target.name)] = {  
                        "type": "role" if isinstance(target, discord.Role) else "member",
                        "perms": serialize_permissions(overwrite)  
                    }
                categoryPls[channel.name] = channelPL
            plCategories[category.name] = categoryPls
        backupJSON['categories'] = plCategories
        json.dump(backupJSON, open(f"./backups/{name}.json", 'w'), indent=4)
        embed = embedBuilder(
            title="`✅`・Backup crée",
            description=f"*La backup `{name}` à été créé et enregistrée avec succès.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(backupCreate(bot))