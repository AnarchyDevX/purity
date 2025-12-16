import discord
import asyncio
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.ticketView.close import closeButtonTicket

class PreTicketHandler:
    """Gestionnaire du système de pré-formulaire pour les tickets"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_pretickets = {}  # {(guild_id, user_id): {"channel": channel, "task": task}}
    
    async def create_preticket(
        self, 
        interaction: discord.Interaction, 
        selected_category: str,
        category_data: dict,
        target_category: discord.CategoryChannel
    ):
        """
        Crée un channel de pré-ticket et lance le formulaire
        
        Args:
            interaction: L'interaction Discord
            selected_category: Le nom de la catégorie sélectionnée
            category_data: Les données de la catégorie (emoji, role_id, discord_category_id)
            target_category: La catégorie Discord où créer le ticket final
        """
        
        # Vérifier si l'utilisateur a déjà un pré-ticket actif sur ce serveur
        preticket_key = (interaction.guild.id, interaction.user.id)
        if preticket_key in self.active_pretickets:
            existing_channel = self.active_pretickets[preticket_key].get("channel")
            if existing_channel:
                try:
                    # Vérifier que le channel existe toujours et qu'il est sur le même serveur
                    if existing_channel.guild.id == interaction.guild.id:
                        await existing_channel.fetch_message(existing_channel.last_message_id or 0)
                        return await err_embed(
                            interaction,
                            title="Pré-ticket actif",
                            description=f"Vous avez déjà un pré-ticket en cours: {existing_channel.mention}\n\nVeuillez le compléter ou attendre qu'il expire.",
                            followup=True
                        )
                except (discord.NotFound, discord.HTTPException):
                    # Le channel n'existe plus, on peut continuer
                    del self.active_pretickets[preticket_key]
        
        # Récupérer la configuration
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if not guildJSON or 'tickets' not in guildJSON:
            return await err_embed(
                interaction,
                title="Configuration manquante",
                description="La configuration des tickets n'a pas été trouvée.",
                followup=True
            )
        
        # Récupérer la catégorie des pré-tickets
        preticket_category_id = guildJSON['tickets'].get('preticket_category')
        if not preticket_category_id:
            return await err_embed(
                interaction,
                title="Catégorie non configurée",
                description="La catégorie des pré-tickets n'a pas été configurée.\n\nUtilisez `/tickets-config` et cliquez sur le bouton **📝 Pré-tickets** pour la configurer.",
                followup=True
            )
        
        preticket_category = interaction.guild.get_channel(preticket_category_id)
        if not preticket_category or not isinstance(preticket_category, discord.CategoryChannel):
            return await err_embed(
                interaction,
                title="Catégorie introuvable",
                description="La catégorie des pré-tickets configurée n'existe plus.\n\nUtilisez `/tickets-config` et cliquez sur le bouton **📝 Pré-tickets** pour la reconfigurer.",
                followup=True
            )
        
        # Créer le channel temporaire
        try:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            }
            
            # Ajouter les admins
            for role in interaction.guild.roles:
                if role.permissions.administrator:
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True)
            
            preticket_channel = await preticket_category.create_text_channel(
                name=f"pre-ticket-{interaction.user.name}",
                overwrites=overwrites,
                reason=f"Pré-ticket pour {interaction.user}"
            )
            
            # Notifier l'utilisateur
            await interaction.followup.send(
                embed=embedBuilder(
                    title="`✅`・Pré-ticket créé",
                    description=f"Votre pré-ticket a été créé: {preticket_channel.mention}\n\nVeuillez répondre aux questions pour continuer.",
                    color=embed_color(),
                    footer=footer()
                ),
                ephemeral=True
            )
            
            # Lancer le formulaire
            task = asyncio.create_task(
                self._run_preticket_form(
                    preticket_channel,
                    interaction.user,
                    interaction.guild,
                    selected_category,
                    category_data,
                    target_category
                )
            )
            
            preticket_key = (interaction.guild.id, interaction.user.id)
            self.active_pretickets[preticket_key] = {
                "channel": preticket_channel,
                "task": task
            }
            
        except discord.Forbidden:
            return await err_embed(
                interaction,
                title="Erreur de permissions",
                description="Je n'ai pas les permissions pour créer un channel dans cette catégorie.",
                followup=True
            )
        except discord.HTTPException as e:
            return await err_embed(
                interaction,
                title="Erreur",
                description=f"Une erreur est survenue lors de la création du pré-ticket: {str(e)}",
                followup=True
            )
    
    async def _run_preticket_form(
        self,
        channel: discord.TextChannel,
        user: discord.User,
        guild: discord.Guild,
        selected_category: str,
        category_data: dict,
        target_category: discord.CategoryChannel
    ):
        """Lance le formulaire de pré-ticket"""
        
        try:
            # Message de bienvenue
            welcome_embed = embedBuilder(
                title=f"🎫 Pré-ticket - {selected_category}",
                description=f"Bienvenue {user.mention} !\n\nAvant de créer votre ticket, merci de répondre aux questions suivantes.\n\n**⚠️ Important :** Vous avez **5 minutes** pour répondre à chaque question.",
                color=embed_color(),
                footer=footer()
            )
            await channel.send(embed=welcome_embed)
            
            # Question 1: Pseudo Roblox
            question1_embed = embedBuilder(
                title="❓ Question 1/2",
                description="**Quel est ton pseudo Roblox ?**\n\nRépondez dans ce channel.",
                color=embed_color(),
                footer=footer()
            )
            await channel.send(embed=question1_embed)
            
            # Attendre la réponse (5 minutes)
            def check_message(m):
                return m.channel.id == channel.id and m.author.id == user.id
            
            try:
                roblox_username_msg = await self.bot.wait_for('message', timeout=300.0, check=check_message)
                roblox_username = roblox_username_msg.content
                
                # Confirmer la réception
                await roblox_username_msg.add_reaction("✅")
                
            except asyncio.TimeoutError:
                timeout_embed = embedBuilder(
                    title="⏰ Temps écoulé",
                    description="Vous n'avez pas répondu à temps. Le pré-ticket va être supprimé dans 10 secondes.",
                    color=0xff0000,
                    footer=footer()
                )
                await channel.send(embed=timeout_embed)
                await asyncio.sleep(10)
                await channel.delete(reason="Pré-ticket expiré - pas de réponse")
                
                # Nettoyer
                preticket_key = (guild.id, user.id)
                if preticket_key in self.active_pretickets:
                    del self.active_pretickets[preticket_key]
                return
            
            # Question 2: Raison
            question2_embed = embedBuilder(
                title="❓ Question 2/2",
                description="**Quelle est la raison de ta demande ?**\n\nRépondez dans ce channel.",
                color=embed_color(),
                footer=footer()
            )
            await channel.send(embed=question2_embed)
            
            try:
                reason_msg = await self.bot.wait_for('message', timeout=300.0, check=check_message)
                reason = reason_msg.content
                
                # Confirmer la réception
                await reason_msg.add_reaction("✅")
                
            except asyncio.TimeoutError:
                timeout_embed = embedBuilder(
                    title="⏰ Temps écoulé",
                    description="Vous n'avez pas répondu à temps. Le pré-ticket va être supprimé dans 10 secondes.",
                    color=0xff0000,
                    footer=footer()
                )
                await channel.send(embed=timeout_embed)
                await asyncio.sleep(10)
                await channel.delete(reason="Pré-ticket expiré - pas de réponse")
                
                # Nettoyer
                preticket_key = (guild.id, user.id)
                if preticket_key in self.active_pretickets:
                    del self.active_pretickets[preticket_key]
                return
            
            # Formulaire complété, créer le ticket officiel
            processing_embed = embedBuilder(
                title="⏳ Création du ticket...",
                description="Merci pour vos réponses ! Création de votre ticket officiel en cours...",
                color=embed_color(),
                footer=footer()
            )
            await channel.send(embed=processing_embed)
            
            # Créer le ticket officiel
            await self._create_official_ticket(
                guild,
                user,
                selected_category,
                category_data,
                target_category,
                roblox_username,
                reason
            )
            
            # Supprimer le pré-ticket
            await asyncio.sleep(3)
            await channel.delete(reason="Pré-ticket complété, ticket officiel créé")
            
            # Nettoyer
            preticket_key = (guild.id, user.id)
            if preticket_key in self.active_pretickets:
                del self.active_pretickets[preticket_key]
        
        except Exception as e:
            print(f"[PRETICKET ERROR] Erreur dans le formulaire: {e}")
            try:
                error_embed = embedBuilder(
                    title="❌ Erreur",
                    description=f"Une erreur est survenue lors de la création du ticket.\n\nErreur: {str(e)}",
                    color=0xff0000,
                    footer=footer()
                )
                await channel.send(embed=error_embed)
                await asyncio.sleep(10)
                await channel.delete(reason="Erreur lors du pré-ticket")
            except:
                pass
            
            # Nettoyer
            preticket_key = (guild.id, user.id)
            if preticket_key in self.active_pretickets:
                del self.active_pretickets[preticket_key]
    
    async def _create_official_ticket(
        self,
        guild: discord.Guild,
        user: discord.User,
        selected_category: str,
        category_data: dict,
        target_category: discord.CategoryChannel,
        roblox_username: str,
        reason: str
    ):
        """Crée le ticket officiel après le formulaire"""
        
        # Récupérer la configuration
        guildJSON = load_json_file(f"./configs/{guild.id}.json")
        
        # Nom du ticket
        ticket_name = f"{user.name}-{selected_category}"
        
        # Permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True),
        }
        
        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True)
        
        # Rôle de support par défaut (fallback)
        SUPPORT_ROLE_ID = 1366762115594977300
        support_role = guild.get_role(SUPPORT_ROLE_ID)
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        
        # Ajouter les rôles configurés
        if guildJSON and 'tickets' in guildJSON:
            # Staff role
            if 'staff_role' in guildJSON['tickets'] and guildJSON['tickets']['staff_role']:
                staff_role = guild.get_role(guildJSON['tickets']['staff_role'])
                if staff_role:
                    overwrites[staff_role] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True,
                        attach_files=True,
                        embed_links=True
                    )
            
            # Autres rôles
            if 'roles' in guildJSON['tickets']:
                for role_id in guildJSON['tickets']['roles']:
                    role = guild.get_role(role_id)
                    if role and role not in overwrites:
                        overwrites[role] = discord.PermissionOverwrite(
                            view_channel=True,
                            send_messages=True,
                            read_message_history=True
                        )
        
        # Vérifier si on doit utiliser la catégorie "nouveaux" (seulement si pas de catégorie spécifique)
        # Si target_category est None ou invalide, fallback sur "nouveaux"
        if target_category is None or not isinstance(target_category, discord.CategoryChannel):
            if guildJSON:
                nouveaux_id = guildJSON.get('tickets', {}).get('categories', {}).get('nouveaux')
                if nouveaux_id:
                    nouveaux_category = guild.get_channel(nouveaux_id)
                    if nouveaux_category and isinstance(nouveaux_category, discord.CategoryChannel):
                        target_category = nouveaux_category
        
        # Créer le channel du ticket
        try:
            ticket_channel = await target_category.create_text_channel(
                name=ticket_name,
                overwrites=overwrites,
                reason=f"Ticket créé par {user}"
            )
            
            # Récupérer le template d'embed ou utiliser le template par défaut
            template = guildJSON.get('tickets', {}).get('embed_template', {})
            if not template:
                template = {
                    "title": "🎫 Ticket - {category}",
                    "description": "Un membre du staff va vous prendre en charge, merci de patienter.",
                    "color": None,
                    "footer": None,
                    "show_roblox": True,
                    "show_reason": True,
                    "show_category": True,
                    "show_user": True
                }
            
            # Construire le titre avec les variables
            emoji = category_data.get('emoji', '🎫')
            title = template.get('title', f"{emoji} Ticket - {{category}}")
            title = title.replace('{category}', selected_category)
            title = title.replace('{user}', user.mention)
            title = title.replace('{username}', user.name)
            title = title.replace('{roblox}', roblox_username)
            title = title.replace('{reason}', reason[:50])  # Limiter la longueur
            
            # Construire la description avec les variables
            description = template.get('description', 'Un membre du staff va vous prendre en charge, merci de patienter.')
            description = description.replace('{category}', selected_category)
            description = description.replace('{user}', user.mention)
            description = description.replace('{username}', user.name)
            description = description.replace('{roblox}', roblox_username)
            description = description.replace('{reason}', reason)
            
            # Couleur
            color_value = template.get('color')
            if color_value:
                try:
                    color = int(color_value, 16) if isinstance(color_value, str) else color_value
                except:
                    color = embed_color()
            else:
                color = embed_color()
            
            # Créer l'embed
            summary_embed = discord.Embed(
                title=title,
                description=description,
                color=color
            )
            
            # Ajouter les champs selon la configuration
            if template.get('show_user', True):
                summary_embed.add_field(name="👤 Utilisateur", value=user.mention, inline=True)
            
            if template.get('show_roblox', True):
                summary_embed.add_field(name="🎮 Pseudo Roblox", value=f"`{roblox_username}`", inline=True)
            
            if template.get('show_category', True):
                summary_embed.add_field(name="📁 Catégorie", value=selected_category, inline=True)
            
            if template.get('show_reason', True):
                summary_embed.add_field(name="📝 Raison", value=reason, inline=False)
            
            # Footer
            footer_text = template.get('footer')
            if footer_text:
                summary_embed.set_footer(text=footer_text)
            else:
                summary_embed.set_footer(text=footer())
            
            # Mention du rôle si configuré
            role_id = category_data.get('role_id')
            role_mention = f"<@&{role_id}>" if role_id else ""
            
            # Vue avec boutons avec custom_id basé sur le channel
            view = discord.ui.View(timeout=None)
            from views.ticketView.claim import claimButtonTicket
            view.add_item(claimButtonTicket(custom_id=f"ticket_claim_{ticket_channel.id}"))
            view.add_item(closeButtonTicket(custom_id=f"ticket_close_{ticket_channel.id}"))
            
            # Envoyer le message avec mention du rôle
            content = f"{user.mention}"
            if role_mention:
                content += f" {role_mention}"
            
            message = await ticket_channel.send(content=content, embed=summary_embed, view=view)
            # Ajouter la vue au bot pour la persistance
            self.bot.add_view(view, message_id=message.id)
            
            # Envoyer un message en DM à l'utilisateur
            try:
                dm_embed = embedBuilder(
                    title="✅ Ticket créé",
                    description=f"Votre ticket **{selected_category}** a été créé avec succès !\n\n{ticket_channel.mention}",
                    color=embed_color(),
                    footer=footer()
                )
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                pass  # L'utilisateur a désactivé les DMs
            
        except discord.Forbidden:
            print(f"[PRETICKET ERROR] Pas de permissions pour créer le ticket officiel")
        except discord.HTTPException as e:
            print(f"[PRETICKET ERROR] Erreur HTTP lors de la création du ticket: {e}")

