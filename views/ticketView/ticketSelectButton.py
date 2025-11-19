import discord
import uuid
from discord.ui import Select, View
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.close import closeButtonTicket


class ticketSelectButton(Select):
    def __init__(self, bot, userId, category, optionsList, custom_id: str | None = None):
        self.bot = bot
        self.userId = userId
        self.category: discord.CategoryChannel = category
        options = []
        for element in optionsList:
            emoji_value = element.get('emojis')
            # Valider l'emoji : doit être une chaîne non vide ou None
            if emoji_value and isinstance(emoji_value, str) and len(emoji_value.strip()) > 0:
                # Vérifier que c'est un emoji valide (Unicode ou format <:name:id>)
                if len(emoji_value.strip()) <= 100:  # Discord limite à 100 caractères
                    emoji = emoji_value.strip()
                else:
                    emoji = None
            else:
                emoji = None
            
            options.append(
                discord.SelectOption(
                    label=element['title'], 
                    description=element['description'], 
                    emoji=emoji if emoji else None, 
                    value=element['title']
                )
            )
        if custom_id is None:
            custom_id = f"ticket_select_{uuid.uuid4().hex}"

        super().__init__(
            max_values=1,
            min_values=1,
            placeholder="Selectionnez une option",
            options=options,
            custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        selected_option = self.values[0]
        expected_ticket_name = f"{interaction.user.name}-{selected_option}"
        
        # Vérifier dans toutes les catégories de tickets si l'utilisateur a déjà un ticket pour cette option
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        categories_to_check = []
        
        if guildJSON and 'tickets' in guildJSON and 'categories' in guildJSON['tickets']:
            categories_to_check = [
                guildJSON['tickets']['categories'].get('nouveaux'),
                guildJSON['tickets']['categories'].get('pris_en_charge'),
                guildJSON['tickets']['categories'].get('en_pause'),
                guildJSON['tickets']['categories'].get('fermes')
            ]
            # Retirer les None
            categories_to_check = [cat_id for cat_id in categories_to_check if cat_id is not None]
        
        # Ajouter aussi la catégorie par défaut
        categories_to_check.append(self.category.id)
        
        # Vérifier dans toutes ces catégories
        for cat_id in categories_to_check:
            cat = interaction.guild.get_channel(cat_id)
            if cat and isinstance(cat, discord.CategoryChannel):
                for existing_channel in cat.channels:
                    if existing_channel.permissions_for(interaction.user).view_channel:
                        # Vérifier si c'est exactement le même type de ticket
                        if existing_channel.name == expected_ticket_name:
                            return await err_embed(
                                interaction,
                                title="Ticket déjà ouvert",
                                description=f"Vous avez déjà un ticket **{selected_option}** ouvert: {existing_channel.mention}\n\nVeuillez fermer votre ticket existant avant d'en créer un nouveau.",
                                followup=True
                            )
        
        embed = embedBuilder(
            title="`✨`・Tickets",
            description=f"Un membre du staff va vous prendre en charge, merci de patienter",
            color=embed_color(),
            footer=footer()
        )
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),  
            interaction.user: discord.PermissionOverwrite(view_channel=True), 
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True),
        }

        for role in interaction.guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True)
        
        # Ajouter les rôles configurés pour les tickets
        guildJSON_check = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON_check and 'tickets' in guildJSON_check:
            # Ajouter le rôle staff (priorité haute)
            if 'staff_role' in guildJSON_check['tickets'] and guildJSON_check['tickets']['staff_role']:
                staff_role = interaction.guild.get_role(guildJSON_check['tickets']['staff_role'])
                if staff_role:
                    # Permissions complètes pour le staff : read, send, history, attach files
                    overwrites[staff_role] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True,
                        attach_files=True,
                        embed_links=True
                    )
            
            # Ajouter les autres rôles configurés
            if 'roles' in guildJSON_check['tickets']:
                for role_id in guildJSON_check['tickets']['roles']:
                    role = interaction.guild.get_role(role_id)
                    if role and role not in overwrites:  # Éviter les doublons
                        overwrites[role] = discord.PermissionOverwrite(view_channel=True)

        # Vérifier si la catégorie "nouveaux" est configurée, sinon utiliser la catégorie par défaut
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        target_category = self.category
        
        if guildJSON:
            nouveaux_id = guildJSON.get('tickets', {}).get('categories', {}).get('nouveaux')
            if nouveaux_id:
                nouveaux_category = interaction.guild.get_channel(nouveaux_id)
                if nouveaux_category and isinstance(nouveaux_category, discord.CategoryChannel):
                    target_category = nouveaux_category
        
        channel = await target_category.create_text_channel(
            name=expected_ticket_name,
            overwrites=overwrites
        )
        view = discord.ui.View(timeout=None)
        # Ajouter le bouton claim pour les nouveaux tickets
        from views.ticketView.claim import claimButtonTicket
        view.add_item(claimButtonTicket())
        view.add_item(closeButtonTicket())
        await channel.send(embed=embed, content=interaction.user.mention, view=view)
        await interaction.followup.send(f"Votre ticket a été ouvert {channel.mention}", ephemeral=True)