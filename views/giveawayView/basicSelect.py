import discord
import asyncio
from discord.ui import Select
from discord import SelectOption
from functions.functions import *

class basicGiveawaySelect(Select):
    def __init__(self, bot, userId, config):
        self.bot = bot
        self.userId = userId
        self.config = config
        options = [
            SelectOption(label="Gain", value="gain", description="Définir le prix du giveaway", emoji="🎉"),
            SelectOption(label="Durée", value="duree", description="Définir la durée du giveaway", emoji="📅"),
            SelectOption(label="Salon", value="salon", description="Définir le salon où envoyer le giveaway", emoji="💬"),
            SelectOption(label="Nombre de gagnants", value="gagnants", description="Définir le nombre de gagnants", emoji="👥"),
            SelectOption(label="Émoji", value="emoji", description="Définir l'émoji de réaction", emoji="😀"),
            SelectOption(label="Rôle Obligatoire", value="role_obligatoire", description="Définir un rôle obligatoire", emoji="✅"),
            SelectOption(label="Rôle Interdit", value="role_interdit", description="Définir un rôle interdit", emoji="❌"),
            SelectOption(label="Niveau requis", value="niveau_requis", description="Définir un niveau requis", emoji="⬆️"),
            SelectOption(label="Invitations requises", value="invitations_requises", description="Définir un nombre d'invitations", emoji="📨"),
            SelectOption(label="Gagnants imposés", value="gagnants_imposes", description="Forcer certains gagnants", emoji="🏷️"),
            SelectOption(label="Présence en vocal", value="presence_vocal", description="Activer/désactiver la présence en vocal", emoji="🔊"),
            SelectOption(label="Ajouter condition custom", value="condition_custom_add", description="Ajouter une condition personnalisée", emoji="➕"),
            SelectOption(label="Supprimer condition custom", value="condition_custom_remove", description="Supprimer une condition personnalisée", emoji="➖")
        ]
        super().__init__(
            placeholder="Options",
            max_values=1,
            min_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        value = self.values[0]
        
        if value == "gain":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Gain** - Entrez le prix du giveaway (maximum 256 caractères):*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                gain_value = message.content
                if len(gain_value) > 256:
                    await interaction.followup.send("*Le gain dépasse la limite de 256 caractères. Veuillez essayer à nouveau.*", ephemeral=True)
                    await message.delete()
                    return
                
                self.config["gain"] = gain_value
                await self._update_embed(interaction)
                try:
                    await message.delete()
                except:
                    pass
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "duree":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Durée** - Entrez la durée (ex: `5` pour le nombre, puis `day` pour l'unité):*", ephemeral=True)
            await interaction.followup.send("*Format: nombre puis unité (sec/min/hour/day/week) séparés par un espace*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                content = message.content.strip().split()
                if len(content) != 2:
                    await interaction.followup.send("*Format invalide. Utilisez: `nombre unite` (ex: `5 day`)*", ephemeral=True)
                    await message.delete()
                    return
                
                try:
                    duree = int(content[0])
                    unite = content[1].lower()
                    
                    if unite not in ["sec", "min", "hour", "day", "week"]:
                        await interaction.followup.send("*Unité invalide. Utilisez: sec, min, hour, day, ou week.*", ephemeral=True)
                        await message.delete()
                        return
                    
                    self.config["duree"] = duree
                    self.config["unite"] = unite
                    await self._update_embed(interaction)
                    try:
                        await message.delete()
                    except:
                        pass
                except ValueError:
                    await interaction.followup.send("*La durée doit être un nombre.*", ephemeral=True)
                    await message.delete()
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "salon":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("Mentionnez le salon où envoyer le giveaway.", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
                if message.channel_mentions:
                    self.config["salon"] = message.channel_mentions[0].id
                    await self._update_embed(interaction)
                    try:
                        await message.delete()
                    except:
                        pass
                else:
                    await interaction.followup.send("Aucun salon mentionné.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "gagnants":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Nombre de gagnants** - Entrez le nombre de gagnants (nombre entier):*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                try:
                    gagnants = int(message.content)
                    if gagnants < 1:
                        await interaction.followup.send("*Le nombre de gagnants doit être supérieur à 0.*", ephemeral=True)
                        await message.delete()
                        return
                    
                    self.config["gagnants"] = gagnants
                    await self._update_embed(interaction)
                    try:
                        await message.delete()
                    except:
                        pass
                except ValueError:
                    await interaction.followup.send("*Le nombre de gagnants doit être un nombre.*", ephemeral=True)
                    await message.delete()
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "emoji":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Émoji** - Entrez l'émoji de réaction (maximum 10 caractères):*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                emoji_value = message.content.strip()
                if len(emoji_value) > 10:
                    await interaction.followup.send("*L'émoji dépasse la limite de 10 caractères.*", ephemeral=True)
                    await message.delete()
                    return
                
                self.config["emoji"] = emoji_value
                await self._update_embed(interaction)
                try:
                    await message.delete()
                except:
                    pass
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "presence_vocal":
            # Toggle
            await interaction.response.defer(ephemeral=True)
            self.config["presence_vocal"] = not self.config.get("presence_vocal", False)
            await self._update_embed(interaction)
            await interaction.followup.send(f"Présence en vocal: {'✅ Actif' if self.config['presence_vocal'] else '❌ Inactif'}", ephemeral=True)
        elif value == "role_obligatoire" or value == "role_interdit":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("Mentionnez le rôle.", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
                if message.role_mentions:
                    self.config[value] = message.role_mentions[0].id
                    await self._update_embed(interaction)
                    try:
                        await message.delete()
                    except:
                        pass
                else:
                    await interaction.followup.send("Aucun rôle mentionné.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "niveau_requis":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Niveau requis** - Entrez le niveau requis (nombre entier):*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                try:
                    niveau = int(message.content)
                    self.config["niveau_requis"] = niveau
                    await self._update_embed(interaction)
                    try:
                        await message.delete()
                    except:
                        pass
                except ValueError:
                    await interaction.followup.send("*Le niveau doit être un nombre.*", ephemeral=True)
                    await message.delete()
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "invitations_requises":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Invitations requises** - Entrez le nombre d'invitations requises (nombre entier):*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                try:
                    invitations = int(message.content)
                    self.config["invitations_requises"] = invitations
                    await self._update_embed(interaction)
                    try:
                        await message.delete()
                    except:
                        pass
                except ValueError:
                    await interaction.followup.send("*Le nombre d'invitations doit être un nombre.*", ephemeral=True)
                    await message.delete()
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "gagnants_imposes":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Gagnants imposés** - Entrez les IDs des gagnants séparés par des virgules (ex: `123456789,987654321`):*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                ids_str = message.content.strip()
                ids = [int(x.strip()) for x in ids_str.split(",") if x.strip().isdigit()]
                
                if ids:
                    self.config["gagnants_imposes"] = ids
                else:
                    await interaction.followup.send("*Aucun ID valide trouvé. Format: `123456789,987654321`*", ephemeral=True)
                    await message.delete()
                    return
                
                await self._update_embed(interaction)
                try:
                    await message.delete()
                except:
                    pass
            except ValueError:
                await interaction.followup.send("*Format invalide. Utilisez des IDs séparés par des virgules.*", ephemeral=True)
                await message.delete()
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "condition_custom_add":
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("***Condition personnalisée** - Entrez le texte de votre condition (maximum 200 caractères):*", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                condition_text = message.content.strip()
                if len(condition_text) > 200:
                    await interaction.followup.send("*La condition dépasse la limite de 200 caractères.*", ephemeral=True)
                    await message.delete()
                    return
                
                if len(condition_text) < 1:
                    await interaction.followup.send("*La condition ne peut pas être vide.*", ephemeral=True)
                    await message.delete()
                    return
                
                # Initialiser la liste si nécessaire
                if "conditions_custom" not in self.config:
                    self.config["conditions_custom"] = []
                
                self.config["conditions_custom"].append(condition_text)
                await self._update_embed(interaction)
                try:
                    await message.delete()
                except:
                    pass
            except asyncio.TimeoutError:
                await interaction.followup.send("Temps écoulé.", ephemeral=True)
        elif value == "condition_custom_remove":
            await interaction.response.defer(ephemeral=True)
            
            if not self.config.get("conditions_custom") or len(self.config["conditions_custom"]) == 0:
                return await interaction.followup.send("*Aucune condition personnalisée à supprimer.*", ephemeral=True)
            
            # Créer un select avec les conditions
            options = []
            for i, condition in enumerate(self.config["conditions_custom"]):
                # Tronquer si trop long pour l'affichage
                display_text = condition[:50] + "..." if len(condition) > 50 else condition
                options.append(discord.SelectOption(
                    label=f"Condition {i+1}",
                    description=display_text,
                    value=str(i)
                ))
            
            # Créer une vue avec le select
            from views.giveawayView.removeConditionSelect import removeConditionSelect
            view = discord.ui.View(timeout=60.0)
            view.add_item(removeConditionSelect(self.bot, self.userId, self.config))
            
            await interaction.followup.send("*Sélectionnez la condition à supprimer:*", view=view, ephemeral=True)
    
    async def _update_embed(self, interaction):
        from views.giveawayView.updateHelper import update_giveaway_embed
        await update_giveaway_embed(self.bot, self.userId, self.config, interaction)

