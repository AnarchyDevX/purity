import discord
import os
from discord.ext import commands
from discord import app_commands
from typing import Union
from functions.functions import *
from core.embedBuilder import embedBuilder
import asyncio

class backupCreate(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="backup-create", description="Crée une backup d'un serveur et l'enregistrer dans le bot")
    async def backupCreate(self, interaction: discord.Interaction, name: str):
        try:
            if not await check_perms(interaction, 3): 
                return

            # Répondre immédiatement pour éviter le timeout
            await interaction.response.defer(ephemeral=True)

            user_backup_dir = f'./backups/{interaction.user.id}'
            # Créer le dossier de l'utilisateur s'il n'existe pas
            try:
                os.makedirs(user_backup_dir, exist_ok=True)
            except (OSError, PermissionError) as e:
                return await err_embed(
                    interaction,
                    title="Erreur",
                    description=f"Impossible de créer le dossier de backup: {str(e)}",
                    followup=True
                )
            
            if os.path.exists(f'{user_backup_dir}/{name}.json'):
                return await err_embed(
                    interaction,
                    title="Backup existante",
                    description=f"L'id de backup que vous voulez definir existe deja.",
                    followup=True
                )
            
            pfp = interaction.guild.icon.url if interaction.guild.icon != None else "rien"
            banner = interaction.guild.banner.url if interaction.guild.banner != None else "rien"
            
            backupJSON = {
                "name": interaction.guild.name,
                "pfp": pfp,
                "banner": banner,
                "roles": {},
                "categories": {},
                "uncategorized_channels": []
            }
            
            # Sauvegarde des rôles avec position
            for role in sorted(interaction.guild.roles, key=lambda r: r.position, reverse=True):
                r, g, b = role.colour.to_rgb()
                hex_color = f"{r:02x}{g:02x}{b:02x}"
                backupJSON['roles'][str(role.id)] = {
                    "name": role.name,
                    "permission": role.permissions.value,
                    "color": hex_color,
                    "position": role.position,
                    "mentionable": role.mentionable,
                    "hoist": role.hoist
                }

            def serialize_permissions(overwrite: discord.PermissionOverwrite):
                perms = {}
                for perm, value in overwrite:
                    if value is not None:
                        perms[perm] = value
                return perms

            # Sauvegarde des catégories et channels
            for category in sorted(interaction.guild.categories, key=lambda c: c.position):
                categoryPls = {
                    "overwrites": {},
                    "position": category.position
                }
                for target, overwrite in category.overwrites.items():
                    categoryPls["overwrites"][str(target.id) if isinstance(target, discord.Role) else str(target.name)] = {
                        "type": "role" if isinstance(target, discord.Role) else "member",
                        "name": target.name,
                        "perms": serialize_permissions(overwrite)
                    }
                
                # Channels dans la catégorie
                for channel in sorted(category.channels, key=lambda ch: ch.position):
                    channelPL = {
                        "name": channel.name,
                        "type": channel.type.name,
                        "position": channel.position,
                        "perms": {}
                    }
                    
                    # Propriétés spécifiques selon le type
                    if channel.type == discord.ChannelType.text or channel.type == discord.ChannelType.news:
                        channelPL["topic"] = channel.topic if channel.topic else None
                        channelPL["slowmode_delay"] = channel.slowmode_delay
                        channelPL["nsfw"] = channel.nsfw
                    elif channel.type == discord.ChannelType.voice:
                        channelPL["bitrate"] = channel.bitrate
                        channelPL["user_limit"] = channel.user_limit
                        channelPL["rtc_region"] = channel.rtc_region if channel.rtc_region else None
                    elif channel.type == discord.ChannelType.forum:
                        channelPL["topic"] = channel.topic if channel.topic else None
                    
                    for target, overwrite in channel.overwrites.items():
                        channelPL["perms"][str(target.id) if isinstance(target, discord.Role) else str(target.name)] = {
                            "type": "role" if isinstance(target, discord.Role) else "member",
                            "name": target.name,
                            "perms": serialize_permissions(overwrite)
                        }
                    categoryPls[channel.name] = channelPL
                backupJSON['categories'][category.name] = categoryPls
            
            # Sauvegarde des channels sans catégorie
            uncategorized = [ch for ch in interaction.guild.channels if ch.category is None]
            for channel in sorted(uncategorized, key=lambda ch: ch.position):
                channelPL = {
                    "name": channel.name,
                    "type": channel.type.name,
                    "position": channel.position,
                    "perms": {}
                }
                
                # Propriétés spécifiques
                if channel.type == discord.ChannelType.text or channel.type == discord.ChannelType.news:
                    channelPL["topic"] = channel.topic if channel.topic else None
                    channelPL["slowmode_delay"] = channel.slowmode_delay
                    channelPL["nsfw"] = channel.nsfw
                elif channel.type == discord.ChannelType.voice:
                    channelPL["bitrate"] = channel.bitrate
                    channelPL["user_limit"] = channel.user_limit
                    channelPL["rtc_region"] = channel.rtc_region if channel.rtc_region else None
                elif channel.type == discord.ChannelType.forum:
                    channelPL["topic"] = channel.topic if channel.topic else None
                
                for target, overwrite in channel.overwrites.items():
                    channelPL["perms"][str(target.id) if isinstance(target, discord.Role) else str(target.name)] = {
                        "type": "role" if isinstance(target, discord.Role) else "member",
                        "name": target.name,
                        "perms": serialize_permissions(overwrite)
                    }
                backupJSON['uncategorized_channels'].append(channelPL)
            
            try:
                with open(f"{user_backup_dir}/{name}.json", 'w', encoding='utf-8') as f:
                    json.dump(backupJSON, f, indent=4, ensure_ascii=False)
            except (OSError, IOError) as e:
                return await err_embed(
                    interaction,
                    title="Erreur",
                    description=f"Impossible d'enregistrer la backup: {str(e)}",
                    followup=True
                )
            
            embed = embedBuilder(
                title="`✅`・Backup crée",
                description=f"*La backup `{name}` à été créé et enregistrée avec succès.*",
                color=embed_color(),
                footer=footer()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            try:
                await err_embed(
                    interaction,
                    title="Erreur",
                    description=f"Une erreur est survenue lors de la création de la backup: {str(e)}",
                    followup=True
                )
            except:
                pass

async def setup(bot):
    await bot.add_cog(backupCreate(bot))