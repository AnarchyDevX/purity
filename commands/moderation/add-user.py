import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class addUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="add", description="Ajouter un membre au ticket")
    @app_commands.describe(user="Le membre à ajouter au ticket")
    async def addUser(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=True)
        
        # Charger la configuration
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Erreur de configuration",
                description="La configuration du serveur n'a pas été trouvée.",
                followup=True
            )
        
        # Vérifier les permissions
        has_permission = False
        
        # 1. Vérifier si l'utilisateur est administrateur
        if interaction.user.guild_permissions.administrator:
            has_permission = True
        
        # 2. Vérifier si l'utilisateur a le rôle whitelist hardcodé
        WHITELISTED_ROLE_ID = 1366762115594977300
        if not has_permission and interaction.user.get_role(WHITELISTED_ROLE_ID):
            has_permission = True
        
        # 3. Vérifier si l'utilisateur a le rôle autorisé pour /add user
        if not has_permission and 'tickets' in guildJSON and 'add_user_role' in guildJSON['tickets']:
            add_user_role_id = guildJSON['tickets']['add_user_role']
            if add_user_role_id and interaction.user.get_role(add_user_role_id):
                has_permission = True
        
        # 4. Vérifier si l'utilisateur a le rôle staff des tickets
        if not has_permission and 'tickets' in guildJSON and 'staff_role' in guildJSON['tickets']:
            staff_role_id = guildJSON['tickets']['staff_role']
            if staff_role_id and interaction.user.get_role(staff_role_id):
                has_permission = True
        
        if not has_permission:
            return await err_embed(
                interaction,
                title="Permissions insuffisantes",
                description="Vous n'avez pas la permission d'utiliser cette commande.\n\nCette commande est réservée aux administrateurs et aux membres autorisés.",
                followup=True
            )
        
        # Vérifier que c'est un channel texte
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            return await err_embed(
                interaction,
                title="Erreur",
                description="Cette commande ne peut être utilisée que dans un salon de texte.",
                followup=True
            )
        
        # Vérifier que c'est un ticket
        is_ticket = False
        ticket_categories = []
        
        if 'tickets' in guildJSON and 'categories' in guildJSON['tickets']:
            ticket_categories = [
                guildJSON['tickets']['categories'].get('nouveaux'),
                guildJSON['tickets']['categories'].get('pris_en_charge'),
                guildJSON['tickets']['categories'].get('en_pause'),
                guildJSON['tickets']['categories'].get('fermes')
            ]
            ticket_categories = [cat_id for cat_id in ticket_categories if cat_id is not None]
        
        # Vérifier si le channel est dans une catégorie de tickets
        if channel.category_id in ticket_categories:
            is_ticket = True
        
        # Vérifier aussi les catégories dynamiques
        if not is_ticket and 'tickets' in guildJSON and 'ticket_categories' in guildJSON['tickets']:
            for cat_name, cat_data in guildJSON['tickets']['ticket_categories'].items():
                if 'discord_category_id' in cat_data and channel.category_id == cat_data['discord_category_id']:
                    is_ticket = True
                    break
        
        if not is_ticket:
            return await err_embed(
                interaction,
                title="Ce n'est pas un ticket",
                description="Cette commande ne peut être utilisée que dans un salon de ticket.",
                followup=True
            )
        
        # Vérifier que le membre n'est pas déjà dans le ticket
        permissions = channel.permissions_for(user)
        if permissions.view_channel:
            return await err_embed(
                interaction,
                title="Membre déjà présent",
                description=f"{user.mention} a déjà accès à ce ticket.",
                followup=True
            )
        
        # Ajouter le membre au ticket
        try:
            await channel.set_permissions(
                user,
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True
            )
            
            # Message de confirmation
            embed = embedBuilder(
                title="`✅`・Membre ajouté",
                description=f"{user.mention} a été ajouté au ticket par {interaction.user.mention}.",
                color=embed_color(),
                footer=footer()
            )
            
            await channel.send(embed=embed)
            await interaction.followup.send(
                embed=embedBuilder(
                    title="`✅`・Succès",
                    description=f"{user.mention} a été ajouté au ticket.",
                    color=embed_color(),
                    footer=footer()
                ),
                ephemeral=True
            )
            
        except discord.Forbidden:
            return await err_embed(
                interaction,
                title="Erreur de permissions",
                description="Je n'ai pas les permissions nécessaires pour modifier les permissions de ce salon.",
                followup=True
            )
        except discord.HTTPException as e:
            return await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue lors de l'ajout du membre: {str(e)}",
                followup=True
            )

async def setup(bot):
    await bot.add_cog(addUser(bot))

