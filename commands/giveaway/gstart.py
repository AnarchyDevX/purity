import time
import random
import asyncio
import json
import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta, datetime
from functions.functions import *
from core.embedBuilder import embedBuilder

class gstart(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    async def reload_active_giveaways(self):
        """Recharge les giveaways actifs au démarrage du bot"""
        import os
        from datetime import datetime
        
        configs_dir = "./configs"
        if not os.path.exists(configs_dir):
            return
        
        reloaded_count = 0
        for filename in os.listdir(configs_dir):
            if not filename.endswith('.json'):
                continue
            
            try:
                guild_id = int(filename[:-5])
                guildJSON = load_json_file(f"{configs_dir}/{filename}")
                
                if guildJSON is None:
                    continue
                
                guild = self.bot.get_guild(guild_id)
                if guild is None:
                    continue
                
                if 'giveaways' not in guildJSON:
                    continue
                
                giveaways = guildJSON['giveaways']
                if not isinstance(giveaways, dict):
                    continue
                
                for giveaway_id, giveaway_data in giveaways.items():
                    try:
                        message_id = giveaway_data.get('message_id')
                        channel_id = giveaway_data.get('channel_id')
                        end_timestamp = giveaway_data.get('end_timestamp')
                        config = giveaway_data.get('config', {})
                        
                        if not all([message_id, channel_id, end_timestamp]):
                            continue
                        
                        channel = guild.get_channel(channel_id)
                        if channel is None:
                            continue
                        
                        # Vérifier que le message existe encore
                        try:
                            message = await channel.fetch_message(message_id)
                        except (discord.NotFound, discord.Forbidden):
                            # Le message n'existe plus, supprimer du JSON
                            del guildJSON['giveaways'][giveaway_id]
                            with open(f"{configs_dir}/{filename}", 'w', encoding='utf-8') as f:
                                json.dump(guildJSON, f, indent=4)
                            continue
                        
                        # Calculer le temps restant
                        now = datetime.now().timestamp()
                        time_remaining = end_timestamp - now
                        
                        # Si le giveaway est déjà terminé, le finaliser immédiatement
                        if time_remaining <= 0:
                            gagnants = giveaway_data.get('gagnants', 1)
                            gain = giveaway_data.get('gain', '')
                            emoji = giveaway_data.get('emoji', '🎉')
                            await self._giveaway_timer(message, 0, gagnants, gain, emoji, config)
                            continue
                        
                        # Relancer le timer
                        gagnants = giveaway_data.get('gagnants', 1)
                        gain = giveaway_data.get('gain', '')
                        emoji = giveaway_data.get('emoji', '🎉')
                        
                        # Relancer le timer (tout est persistant, rien en mémoire)
                        asyncio.create_task(self._giveaway_timer(message, int(time_remaining), gagnants, gain, emoji, config))
                        reloaded_count += 1
                        
                    except Exception as e:
                        print(f"[GIVEAWAY] Erreur lors du rechargement du giveaway {giveaway_id}: {e}")
                        continue
                        
            except (ValueError, KeyError):
                continue
        
        if reloaded_count > 0:
            print(f"[GIVEAWAY] Giveaways actifs rechargés: {reloaded_count}")

    @app_commands.command(name="giveaway-start", description="Commencer la configuration d'un giveaway")
    async def gstar(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        # Configuration par défaut
        giveaway_config = {
            "_guild_id": interaction.guild.id,  # Stocker l'ID du serveur pour les mentions
            "_channel_id": interaction.channel.id,  # Stocker l'ID du channel
            "gain": None,
            "duree": None,
            "unite": None,
            "salon": None,
            "gagnants": 1,
            "emoji": "🎉",
            "role_obligatoire": None,
            "role_interdit": None,
            "niveau_requis": None,
            "invitations_requises": None,
            "gagnants_imposes": None,
            "presence_vocal": False,
            "conditions_custom": []  # Liste des conditions personnalisées
        }
        
        # Créer l'embed de configuration
        embed = self._create_config_embed(giveaway_config)
        
        # Créer la vue avec les selects et boutons
        from views.giveawayView.basicSelect import basicGiveawaySelect
        from views.giveawayView.sendButton import sendGiveawayButton
        
        view = discord.ui.View(timeout=None)
        view.add_item(basicGiveawaySelect(self.bot, interaction.user.id, giveaway_config))
        view.add_item(sendGiveawayButton(self.bot, interaction.user.id, giveaway_config))
        
        await interaction.response.send_message(embed=embed, view=view)
        # Récupérer le message envoyé
        async for msg in interaction.channel.history(limit=5):
            if msg.author.id == self.bot.user.id and msg.embeds and msg.embeds[0].title == "Giveaway":
                giveaway_config["_message_id"] = msg.id
                break
    
    def _create_config_embed(self, config):
        """Crée l'embed de configuration du giveaway"""
        # Fonction pour formater les valeurs
        def format_value(value):
            if value is None:
                return "Pas défini"
            return str(value)
        
        # Calculer la durée formatée si disponible
        duree_text = "Pas défini"
        if config.get("duree") and config.get("unite"):
            unite_map = {
                "sec": "s", "min": "m", "hour": "h", 
                "day": "d", "week": "w"
            }
            duree_text = f"{config['duree']}{unite_map.get(config['unite'], config['unite'])}"
        
        # Formatage du salon
        salon_text = "Pas défini"
        if config.get("salon"):
            salon_text = f"<#{config['salon']}>"
        
        # Présence vocal (toggle)
        vocal_text = "✅ Actif" if config.get("presence_vocal") else "❌ Inactif"
        
        # Formater les rôles
        role_obligatoire_text = "Pas défini"
        if config.get("role_obligatoire"):
            guild_id = config.get("_guild_id")
            if guild_id:
                guild = self.bot.get_guild(guild_id)
                if guild:
                    role = guild.get_role(config["role_obligatoire"])
                    role_obligatoire_text = role.mention if role else "Rôle introuvable"
        
        role_interdit_text = "Pas défini"
        if config.get("role_interdit"):
            guild_id = config.get("_guild_id")
            if guild_id:
                guild = self.bot.get_guild(guild_id)
                if guild:
                    role = guild.get_role(config["role_interdit"])
                    role_interdit_text = role.mention if role else "Rôle introuvable"
        
        # Formater les gagnants imposés
        gagnants_imposes_text = "Pas défini"
        if config.get("gagnants_imposes"):
            mentions = []
            guild_id = config.get("_guild_id")
            if guild_id:
                guild = self.bot.get_guild(guild_id)
                for uid in config["gagnants_imposes"]:
                    if guild:
                        member = guild.get_member(uid)
                        mentions.append(member.mention if member else f"<@{uid}>")
                    else:
                        mentions.append(f"<@{uid}>")
            else:
                for uid in config["gagnants_imposes"]:
                    mentions.append(f"<@{uid}>")
            gagnants_imposes_text = ", ".join(mentions) if mentions else "Pas défini"
        
        # Organiser les champs en deux colonnes comme dans l'image
        # Première colonne (gauche) - Options de base
        # Deuxième colonne (droite) - Options avancées
        embed = embedBuilder(
            title="Giveaway",
            description="Configurez votre giveaway en utilisant les menus ci-dessous.",
            color=embed_color(),
            footer=footer()
        )
        
        # Première colonne (inline=True)
        embed.add_field(name="`🎉`・Gain", value=format_value(config.get("gain")), inline=True)
        embed.add_field(name="`📅`・Durée", value=duree_text, inline=True)
        embed.add_field(name="`#`・Salon", value=salon_text, inline=True)
        embed.add_field(name="`👥`・Gagnant", value=str(config.get("gagnants", 1)), inline=True)
        embed.add_field(name="`😀`・Émoji", value=config.get("emoji", "🎉"), inline=True)
        
        # Deuxième colonne pour les options avancées (inline=True aussi pour alignement)
        embed.add_field(name="`✅`・Rôle obligatoire", value=role_obligatoire_text, inline=True)
        embed.add_field(name="`❌`・Rôle interdit", value=role_interdit_text, inline=True)
        embed.add_field(name="`⬆️`・Niveau requis", value=format_value(config.get("niveau_requis")), inline=True)
        embed.add_field(name="`📨`・Invitations requises", value=format_value(config.get("invitations_requises")), inline=True)
        embed.add_field(name="`🏷️`・Gagnant(s) imposés", value=gagnants_imposes_text, inline=True)
        embed.add_field(name="`🔊`・Présence en vocal", value=vocal_text, inline=True)
        
        # Ajouter les conditions personnalisées si présentes
        conditions_custom = config.get("conditions_custom", [])
        if conditions_custom:
            conditions_text = "\n".join(f"• {cond}" for cond in conditions_custom)
            # Tronquer si trop long (limite Discord de 1024 caractères pour field value)
            if len(conditions_text) > 1024:
                conditions_text = conditions_text[:1021] + "..."
            embed.add_field(
                name="`➕`・Conditions personnalisées",
                value=conditions_text,
                inline=False
            )
        
        return embed
    
    async def _launch_giveaway(self, interaction: discord.Interaction, config):
        """Lance le giveaway avec la configuration"""
        import time
        from datetime import timedelta, datetime
        
        timeToAdd = None
        toWait = 0
        now = datetime.now()
        
        unite = config["unite"]
        duree = config["duree"]
        
        if unite == "sec":
            timeToAdd = now + timedelta(seconds=duree)
            toWait = duree 
        elif unite == "min":
            timeToAdd = now + timedelta(minutes=duree)
            toWait = duree * 60
        elif unite == "hour":
            timeToAdd = now + timedelta(hours=duree)
            toWait = duree * 60 * 60
        elif unite == "day":
            timeToAdd = now + timedelta(days=duree)
            toWait = duree * 60 * 60 * 24
        elif unite == "week":
            toWait = duree * 60 * 60 * 24 * 7
            timeToAdd = now + timedelta(weeks=duree)

        timestamp = round(timeToAdd.timestamp())
        gain = config["gain"]
        gagnants = config.get("gagnants", 1)
        emoji = config.get("emoji", "🎉")
        
        # Construire la description avec les conditions
        description = f"*Se termine:* <t:{timestamp}:F>\n*Temps restant:* <t:{timestamp}:R>\n*Nombre de gagnants:* `{gagnants}`"
        
        # Ajouter les conditions requises
        conditions = []
        
        # Rôle obligatoire
        if config.get("role_obligatoire"):
            guild = self.bot.get_guild(config.get("_guild_id", 0)) if config.get("_guild_id") else None
            if guild:
                role = guild.get_role(config["role_obligatoire"])
                if role:
                    conditions.append(f"**Rôle requis:** {role.mention}")
        
        # Rôle interdit
        if config.get("role_interdit"):
            guild = self.bot.get_guild(config.get("_guild_id", 0)) if config.get("_guild_id") else None
            if guild:
                role = guild.get_role(config["role_interdit"])
                if role:
                    conditions.append(f"**Rôle interdit:** {role.mention}")
        
        # Niveau requis
        if config.get("niveau_requis"):
            conditions.append(f"**Niveau requis:** {config['niveau_requis']}")
        
        # Invitations requises
        if config.get("invitations_requises"):
            conditions.append(f"**Invitations requises:** {config['invitations_requises']}")
        
        # Présence en vocal
        if config.get("presence_vocal"):
            conditions.append("**Présence en vocal:** Requise")
        
        # Conditions personnalisées
        conditions_custom = config.get("conditions_custom", [])
        for custom_cond in conditions_custom:
            conditions.append(f"**Condition:** {custom_cond}")
        
        # Ajouter les conditions à la description
        if conditions:
            description += "\n\n**`⚠️`・Conditions requises:**\n" + "\n".join(f"• {cond}" for cond in conditions)
        
        # Créer l'embed du giveaway
        embed = embedBuilder(
            title=f"`{emoji}`・{gain}",
            description=description,
            color=embed_color(),
            footer=footer()
        )
        
        # Envoyer dans le salon configuré
        channel = self.bot.get_channel(config["salon"])
        if not channel:
            return await err_embed(
                interaction,
                title="Erreur",
                description="Le salon configuré n'existe plus.",
                followup=True
            )
        
        message = await channel.send(embed=embed)
        await message.add_reaction(emoji)
        
        # Sauvegarder le giveaway actif dans le JSON (tout est persistant, rien en mémoire)
        guildJSON = load_json_file(f"./configs/{config.get('_guild_id')}.json")
        if guildJSON is not None:
            if 'giveaways' not in guildJSON:
                guildJSON['giveaways'] = {}
            
            # Sauvegarder avec le timestamp de fin
            guildJSON['giveaways'][str(message.id)] = {
                'channel_id': channel.id,
                'message_id': message.id,
                'end_timestamp': timestamp,
                'gagnants': gagnants,
                'gain': gain,
                'emoji': emoji,
                'config': config
            }
            
            with open(f"./configs/{config.get('_guild_id')}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
        
        # Lancer le timer en arrière-plan
        asyncio.create_task(self._giveaway_timer(message, toWait, gagnants, gain, emoji, config))
    
    async def _giveaway_timer(self, message: discord.Message, toWait: int, gagnants: int, gain: str, emoji: str, config: dict):
        """Timer pour le giveaway"""
        await asyncio.sleep(toWait)
        
        # Retirer le giveaway du JSON (tout est persistant)
        try:
            guildJSON = load_json_file(f"./configs/{message.guild.id}.json")
            if guildJSON is not None and 'giveaways' in guildJSON:
                if str(message.id) in guildJSON['giveaways']:
                    del guildJSON['giveaways'][str(message.id)]
                    with open(f"./configs/{message.guild.id}.json", 'w', encoding='utf-8') as f:
                        json.dump(guildJSON, f, indent=4)
        except Exception:
            pass
        
        try:
            # Recharger le message pour avoir les réactions
            message = await message.channel.fetch_message(message.id)
            users = []
            
            for reaction in message.reactions:
                if str(reaction.emoji) == emoji:
                    async for user in reaction.users():
                        if user.id != self.bot.user.id:
                            # Vérifier les conditions optionnelles
                            if self._check_giveaway_conditions(user, message.guild, config):
                                users.append(user)
            
            if len(users) < gagnants:
                return await message.channel.send(f"❌ Il n'y a pas assez de participants au giveaway. ({len(users)}/{gagnants})")
            
            # Gagnants imposés ou random
            if config.get("gagnants_imposes"):
                winners = [self.bot.get_user(uid) for uid in config["gagnants_imposes"] if self.bot.get_user(uid) in users]
                if len(winners) < gagnants:
                    # Compléter avec des users random
                    remaining = [u for u in users if u not in winners]
                    for _ in range(gagnants - len(winners)):
                        if remaining:
                            winner = random.choice(remaining)
                            winners.append(winner)
                            remaining.remove(winner)
            else:
                winners = random.sample(users, min(gagnants, len(users)))
            
            if gagnants == 1:
                winner = winners[0]
                await message.channel.send(f"🎉 Le gagnant est {winner.mention} ! Il remporte donc ***{gain}***")
            else:
                winners_mentions = ", ".join(w.mention for w in winners)
                await message.channel.send(f"🎉 Les gagnants sont {winners_mentions} ! Ils remportent donc ***{gain}***")
        except discord.NotFound:
            pass
        except Exception as e:
            print(f"[GIVEAWAY] Erreur lors de la fin du giveaway: {e}")
    
    def _check_giveaway_conditions(self, user: discord.Member, guild: discord.Guild, config: dict) -> bool:
        """Vérifie si un utilisateur respecte les conditions du giveaway"""
        # Rôle obligatoire
        if config.get("role_obligatoire"):
            role = guild.get_role(config["role_obligatoire"])
            if role and role not in user.roles:
                return False
        
        # Rôle interdit
        if config.get("role_interdit"):
            role = guild.get_role(config["role_interdit"])
            if role and role in user.roles:
                return False
        
        # Présence en vocal
        if config.get("presence_vocal"):
            if not user.voice or not user.voice.channel:
                return False
        
        # TODO: Vérifier niveau et invitations si système implémenté
        # Pour l'instant, on retourne True si les conditions de base sont respectées
        
        return True

async def setup(bot):
    await bot.add_cog(gstart(bot))
