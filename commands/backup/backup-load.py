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
            
        try:
            with open(f"./backups/{name}.json", 'r', encoding='utf-8') as f:
                backup = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("❌ Backup introuvable", ephemeral=True)
            return
            
        await interaction.response.send_message("⏳ Chargement de la backup en cours...", ephemeral=True)
        await interaction.guild.edit(name=backup['name'])
        pfpUrl = backup['pfp'] if backup['pfp'] != "rien" else None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(pfpUrl) as r:
                    if r.status != 200:
                        return await err_embed(
                            interaction, 
                            title="Impossible de récuperer l'image",
                            description="Je n'ai pas réussi a lire et récuperer votre image",
                            followup=True
                        )
                    newPfp = await r.read()
                    

            await interaction.guild.edit(icon=newPfp)
        except Exception as e:
            pass
            
        if interaction.guild.premium_subscription_count >= 14:
            try:
                bannerUrl = backup['banner'] if backup['banner'] != "rien" else None
                async with aiohttp.ClientSession() as session:
                    async with session.get(bannerUrl) as r:
                        if r.status != 200:
                            return await err_embed(
                                interaction, 
                                title="Impossible de récuperer l'image",
                                description="Je n'ai pas réussi a lire et récuperer votre image",
                                followup=True
                            )
                        newBanner = await r.read()
                        
                    
                await interaction.guild.edit(icon=newBanner)
                
            except Exception as e:
                print(e)
                
        
        roles = [role for role in interaction.guild.roles if role != interaction.guild.default_role and role.position < interaction.guild.me.top_role.position]
        for role in roles:
            try:
                await role.delete()
            except Exception:
                continue

        for channel in interaction.guild.channels:
            try:
                await channel.delete()
            except Exception:
                continue        

        role_map = await self.create_roles(interaction.guild, backup['roles'])
        await self.create_categories_and_channels(interaction.guild, backup['categories'], role_map)
        try:
            await interaction.user.send("✅ Backup chargée avec succès!", ephemeral=True)
        except Exception as e:
            pass

    async def create_roles(self, guild: discord.Guild, roles_data: dict) -> dict:
        role_map = {}
        sorted_roles = sorted(roles_data.items(), key=lambda x: x[1]['permission'])
        
        everyone_data = next((data for _, data in roles_data.items() if data['name'] == '@everyone'), None)
        if everyone_data:
            try:
                await guild.default_role.edit(
                    permissions=discord.Permissions(permissions=everyone_data['permission'])
                )
                role_map['@everyone'] = guild.default_role
            except Exception:
                pass
        
        for role_id, role_data in sorted_roles:
            if role_data['name'] != '@everyone':  
                try:
                    role = await guild.create_role(
                        name=role_data['name'],
                        permissions=discord.Permissions(permissions=role_data['permission']),
                        colour=discord.Colour(int(role_data['color'], 16))
                    )
                    role_map[role_data['name']] = role
                except Exception:
                    continue
                
        return role_map

    async def create_categories_and_channels(self, guild: discord.Guild, categories_data: dict, role_map: dict):
        for category_name, category_data in categories_data.items():
            category_overwrites = await self.create_overwrites(category_data.get('overwrites', {}), role_map)
            
            try:
                category = await guild.create_category(name=category_name, overwrites=category_overwrites)
                
                for channel_name, channel_data in category_data.items():
                    if channel_name == 'overwrites':
                        continue
                        
                    channel_overwrites = await self.create_overwrites(channel_data.get('perms', {}), role_map)
                    
                    channel_type = channel_data.get('type', 'text')
                    if channel_type == 'text':
                        await guild.create_text_channel(name=channel_data['name'], category=category, overwrites=channel_overwrites)
                    elif channel_type == 'voice':
                        await guild.create_voice_channel(name=channel_data['name'], category=category, overwrites=channel_overwrites)
                    elif channel_type == 'stage':
                        await guild.create_stage_channel(name=channel_data['name'], category=category, overwrites=channel_overwrites)
                    elif channel_type == 'forum':
                        await guild.create_forum(name=channel_data['name'], category=category, overwrites=channel_overwrites)
                        
            except Exception as e:
                continue

    async def create_overwrites(self, overwrites_data: dict, role_map: dict) -> dict:
        try:
            overwrites = {}
            for role_name, perm_data in overwrites_data.items():
                role = role_map.get(role_name)
                if role:
                    overwrite = discord.PermissionOverwrite()
                    for perm_name, value in perm_data['perms'].items():
                        setattr(overwrite, perm_name, value)
                    overwrites[role] = overwrite
            return overwrites
        except Exception as e:
            pass
            

async def setup(bot):
    await bot.add_cog(BackupLoad(bot))