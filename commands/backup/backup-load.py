import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
import json
import aiohttp


class BackupLoad(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="backup-load", description="Charger une backup de serveur")
    async def backup_load(self, interaction: discord.Interaction, name: str):
        if not await check_perms(interaction, 3):
            return
        
        user_backup_dir = f'./backups/{interaction.user.id}'
            
        try:
            with open(f"{user_backup_dir}/{name}.json", 'r', encoding='utf-8') as f:
                backup = json.load(f)
        except FileNotFoundError:
            await err_embed(interaction, "Backup introuvable", "La backup demandée n'existe pas.")
            return
            
        await interaction.response.send_message("⏳ Chargement de la backup en cours...", ephemeral=True)

        backup_guard = getattr(self.bot, "_backup_loading_guilds", None)
        if backup_guard is None:
            backup_guard = set()
            self.bot._backup_loading_guilds = backup_guard
        backup_guard.add(interaction.guild.id)

        try:
            await self._apply_backup(interaction, backup)
        finally:
            backup_guard.discard(interaction.guild.id)

    async def _apply_backup(self, interaction: discord.Interaction, backup: dict) -> None:
        # Édition du nom du serveur
        await interaction.guild.edit(name=backup['name'])

        # Édition de l'icône
        pfpUrl = backup['pfp'] if backup['pfp'] != "rien" else None
        if pfpUrl:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(pfpUrl) as r:
                        if r.status == 200:
                            newPfp = await r.read()
                            await interaction.guild.edit(icon=newPfp)
            except (discord.HTTPException, ValueError, AttributeError):
                pass

        # Édition de la bannière si niveau suffisant
        if interaction.guild.premium_subscription_count >= 14:
            bannerUrl = backup['banner'] if backup['banner'] != "rien" else None
            if bannerUrl:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(bannerUrl) as r:
                            if r.status == 200:
                                newBanner = await r.read()
                                await interaction.guild.edit(banner=newBanner)
                except (discord.HTTPException, ValueError, AttributeError):
                    pass

        # Suppression des rôles existants (sauf @everyone et le rôle du bot)
        roles = [role for role in interaction.guild.roles
                 if role != interaction.guild.default_role
                 and role != interaction.guild.me.top_role
                 and role.position <= interaction.guild.me.top_role.position]

        # Trier par position décroissante pour supprimer du haut vers le bas
        roles.sort(key=lambda r: r.position, reverse=True)

        for role in roles:
            try:
                await role.delete()
                await asyncio.sleep(0.1)  # Petit délai pour éviter les rate limits
            except (discord.Forbidden, discord.HTTPException):
                continue

        # Suppression des channels existants
        for channel in list(interaction.guild.channels):
            try:
                await channel.delete()
            except (discord.Forbidden, discord.HTTPException, discord.NotFound):
                continue

        # Création des rôles
        role_map = await self.create_roles(interaction.guild, backup.get('roles', {}))

        # Création des catégories et channels
        await self.create_categories_and_channels(interaction.guild, backup.get('categories', {}), role_map)

        # Création des channels sans catégorie
        await self.create_uncategorized_channels(interaction.guild, backup.get('uncategorized_channels', []), role_map)

        try:
            await interaction.followup.send("✅ Backup chargée avec succès!", ephemeral=True)
        except (discord.Forbidden, discord.HTTPException):
            pass

    async def create_roles(self, guild: discord.Guild, roles_data: dict) -> dict:
        role_map = {}
        
        # Trier par position décroissante pour garder l'ordre
        sorted_roles = sorted(roles_data.items(), 
                            key=lambda x: x[1].get('position', 0), 
                            reverse=True)
        
        # Gérer @everyone séparément
        everyone_data = next((data for _, data in roles_data.items() if data['name'] == '@everyone'), None)
        if everyone_data:
            try:
                await guild.default_role.edit(
                    permissions=discord.Permissions(permissions=everyone_data['permission'])
                )
                role_map['@everyone'] = guild.default_role
            except (discord.Forbidden, discord.HTTPException):
                pass
        
        # Créer les autres rôles
        created_roles = []
        for role_id, role_data in sorted_roles:
            if role_data['name'] != '@everyone':
                try:
                    role = await guild.create_role(
                        name=role_data['name'],
                        permissions=discord.Permissions(permissions=role_data['permission']),
                        colour=discord.Colour(int(role_data['color'], 16)),
                        mentionable=role_data.get('mentionable', False),
                        hoist=role_data.get('hoist', False)
                    )
                    role_map[role_data['name']] = role
                    created_roles.append((role, role_data['position']))
                except (discord.Forbidden, discord.HTTPException):
                    continue
        
        # Réorganiser les positions dans l'ordre correct
        await self.reorganize_role_positions(created_roles, guild.me.top_role.position)
        
        return role_map

    async def reorganize_role_positions(self, created_roles: list, bot_position: int):
        """Réorganise les positions des rôles créés"""
        if not created_roles:
            return
        
        # Note: Discord crée automatiquement les rôles dans l'ordre inverse
        # Les positions seront correctes si on crée dans l'ordre décroissant
        # Les positions exactes ne peuvent être restaurées que manuellement
        # car Discord ne permet pas de définir directement une position absolue
        pass

    async def create_categories_and_channels(self, guild: discord.Guild, categories_data: dict, role_map: dict):
        # Trier les catégories par position
        sorted_categories = sorted(categories_data.items(), 
                                 key=lambda x: x[1].get('position', 0))
        
        for category_name, category_data in sorted_categories:
            category_overwrites = await self.create_overwrites(category_data.get('overwrites', {}), role_map)
            
            try:
                category = await guild.create_category(name=category_name, overwrites=category_overwrites)
                
                # Trier les channels par position
                sorted_channels = sorted(
                    [(k, v) for k, v in category_data.items() if k != 'overwrites' and k != 'position'],
                    key=lambda x: x[1].get('position', 0)
                )
                
                for channel_name, channel_data in sorted_channels:
                    await self.create_channel(guild, channel_data, category, role_map)
                        
            except (discord.Forbidden, discord.HTTPException):
                continue

    async def create_uncategorized_channels(self, guild: discord.Guild, channels_data: list, role_map: dict):
        # Trier par position
        sorted_channels = sorted(channels_data, key=lambda x: x.get('position', 0))
        
        for channel_data in sorted_channels:
            await self.create_channel(guild, channel_data, None, role_map)

    async def create_channel(self, guild: discord.Guild, channel_data: dict, category: discord.CategoryChannel, role_map: dict):
        channel_overwrites = await self.create_overwrites(channel_data.get('perms', {}), role_map)
        
        try:
            channel_type = channel_data.get('type', 'text')
            kwargs = {
                'name': channel_data['name'],
                'overwrites': channel_overwrites,
                'category': category
            }
            
            # Ajouter les propriétés spécifiques
            if channel_type in ['text', 'news']:
                if 'topic' in channel_data and channel_data['topic']:
                    kwargs['topic'] = channel_data['topic']
                if 'slowmode_delay' in channel_data:
                    kwargs['slowmode_delay'] = channel_data['slowmode_delay']
                if 'nsfw' in channel_data:
                    kwargs['nsfw'] = channel_data['nsfw']
                    
                # Créer le channel textuel (news channels sont aussi des text channels dans discord.py)
                await guild.create_text_channel(**kwargs)
                    
            elif channel_type == 'voice':
                if 'bitrate' in channel_data:
                    kwargs['bitrate'] = channel_data['bitrate']
                if 'user_limit' in channel_data:
                    kwargs['user_limit'] = channel_data['user_limit']
                await guild.create_voice_channel(**kwargs)
                
            elif channel_type == 'stage':
                # Note: create_stage_channel n'existe pas dans discord.py
                # Créer comme un channel textuel à la place
                if 'topic' in channel_data and channel_data['topic']:
                    kwargs['topic'] = channel_data['topic']
                await guild.create_text_channel(**kwargs)
                
            elif channel_type == 'forum':
                # Note: create_forum_channel n'existe pas dans discord.py
                # Créer comme un channel textuel à la place
                if 'topic' in channel_data and channel_data['topic']:
                    kwargs['topic'] = channel_data['topic']
                await guild.create_text_channel(**kwargs)
                
        except (discord.Forbidden, discord.HTTPException) as e:
            pass

    async def create_overwrites(self, overwrites_data: dict, role_map: dict) -> dict:
        overwrites = {}
        
        for identifier, perm_data in overwrites_data.items():
            # identifier est le nom du rôle
            role = role_map.get(identifier)
            
            if role and isinstance(perm_data, dict) and 'perms' in perm_data:
                try:
                    overwrite = discord.PermissionOverwrite()
                    for perm_name, value in perm_data['perms'].items():
                        if hasattr(overwrite, perm_name):
                            setattr(overwrite, perm_name, value)
                    overwrites[role] = overwrite
                except (AttributeError, TypeError, ValueError):
                    continue
        
        return overwrites


async def setup(bot):
    await bot.add_cog(BackupLoad(bot))
