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
        
        # Charger la configuration
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        
        # Vérifier si c'est une catégorie dynamique
        is_dynamic_category = False
        category_data = None
        
        if guildJSON and 'tickets' in guildJSON and 'ticket_categories' in guildJSON['tickets']:
            if selected_option in guildJSON['tickets']['ticket_categories']:
                is_dynamic_category = True
                category_data = guildJSON['tickets']['ticket_categories'][selected_option]
        
        # Si c'est une catégorie dynamique, utiliser le système de pré-formulaire
        if is_dynamic_category and category_data:
            # Vérifier d'abord si l'utilisateur a déjà un ticket de cette catégorie
            expected_ticket_name = f"{interaction.user.name}-{selected_option}"
            
            # Vérifier dans toutes les catégories de tickets
            categories_to_check = []
            
            if guildJSON and 'tickets' in guildJSON and 'categories' in guildJSON['tickets']:
                categories_to_check = [
                    guildJSON['tickets']['categories'].get('nouveaux'),
                    guildJSON['tickets']['categories'].get('pris_en_charge'),
                    guildJSON['tickets']['categories'].get('en_pause'),
                    guildJSON['tickets']['categories'].get('fermes')
                ]
                categories_to_check = [cat_id for cat_id in categories_to_check if cat_id is not None]
            
            # Ajouter aussi la catégorie dynamique
            if 'discord_category_id' in category_data:
                categories_to_check.append(category_data['discord_category_id'])
            
            # Vérifier dans toutes ces catégories (uniquement sur ce serveur)
            for cat_id in categories_to_check:
                cat = interaction.guild.get_channel(cat_id)
                if cat and isinstance(cat, discord.CategoryChannel) and cat.guild.id == interaction.guild.id:
                    for existing_channel in cat.channels:
                        # Vérifier que le channel appartient bien au même serveur
                        if existing_channel.guild.id == interaction.guild.id and existing_channel.permissions_for(interaction.user).view_channel:
                            if existing_channel.name == expected_ticket_name:
                                return await err_embed(
                                    interaction,
                                    title="Ticket déjà ouvert",
                                    description=f"Vous avez déjà un ticket **{selected_option}** ouvert: {existing_channel.mention}\n\nVeuillez fermer votre ticket existant avant d'en créer un nouveau.",
                                    followup=True
                                )
            
            # Récupérer la catégorie cible
            target_category = self.category
            if 'discord_category_id' in category_data:
                dynamic_cat = interaction.guild.get_channel(category_data['discord_category_id'])
                if dynamic_cat and isinstance(dynamic_cat, discord.CategoryChannel):
                    target_category = dynamic_cat
            
            # Utiliser le système de pré-formulaire
            from functions.preticketHandler import PreTicketHandler
            
            # Récupérer ou créer le handler
            if not hasattr(self.bot, 'preticket_handler'):
                self.bot.preticket_handler = PreTicketHandler(self.bot)
            
            await self.bot.preticket_handler.create_preticket(
                interaction,
                selected_option,
                category_data,
                target_category
            )
            return
        
        # Sinon, utiliser l'ancien système (pour les options non-dynamiques)
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
        
        # Vérifier dans toutes ces catégories (uniquement sur ce serveur)
        for cat_id in categories_to_check:
            cat = interaction.guild.get_channel(cat_id)
            if cat and isinstance(cat, discord.CategoryChannel) and cat.guild.id == interaction.guild.id:
                for existing_channel in cat.channels:
                    # Vérifier que le channel appartient bien au même serveur
                    if existing_channel.guild.id == interaction.guild.id and existing_channel.permissions_for(interaction.user).view_channel:
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
        
        # Rôle de support par défaut (hardcodé) - À ajouter en premier pour garantir son ajout
        SUPPORT_ROLE_ID = 1366762115594977300
        support_role = interaction.guild.get_role(SUPPORT_ROLE_ID)
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        
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
                        overwrites[role] = discord.PermissionOverwrite(
                            view_channel=True,
                            send_messages=True,
                            read_message_history=True
                        )

        # Utiliser la catégorie par défaut, fallback sur "nouveaux" si pas de catégorie
        target_category = self.category
        
        # Si pas de catégorie définie, utiliser "nouveaux"
        if target_category is None:
            guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
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
        # Ajouter le bouton claim pour les nouveaux tickets avec custom_id basé sur le channel
        from views.ticketView.claim import claimButtonTicket
        view.add_item(claimButtonTicket(custom_id=f"ticket_claim_{channel.id}"))
        view.add_item(closeButtonTicket(custom_id=f"ticket_close_{channel.id}"))
        message = await channel.send(embed=embed, content=interaction.user.mention, view=view)
        # Ajouter la vue au bot pour la persistance
        self.bot.add_view(view, message_id=message.id)
        await interaction.followup.send(f"Votre ticket a été ouvert {channel.mention}", ephemeral=True)