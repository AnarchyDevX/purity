import discord
from discord.ext import commands
from discord.ui import Select
from functions.functions import *
from core.embedBuilder import embedBuilder

class selectHelp(Select):
    def __init__(self, userId, bot):
        self.bot: commands.Bot = bot
        self.userId = userId
        options = [
            discord.SelectOption(label="Menu", value="home", emoji="🏠"),
            discord.SelectOption(label="Antiraid", value="antiraid", emoji="🛡️"),
            discord.SelectOption(label="Client", value="client", emoji="🤖"),
            discord.SelectOption(label="Configuration", value="config", emoji="⚙️"),
            discord.SelectOption(label="Gestion", value="gestion", emoji="🛠️"),
            discord.SelectOption(label="Giveaway", value="gw", emoji="🎊"),
            discord.SelectOption(label="Informations", value="info", emoji="❓"),
            discord.SelectOption(label="Logs", value="logs", emoji="📂"),
            discord.SelectOption(label="Modération", value="mods", emoji="🔨"),
            discord.SelectOption(label="Utilitaire", value="utils", emoji="✨"),
            discord.SelectOption(label="Vocal", value="voice", emoji="🔊")
        ]
        super().__init__(
            placeholder="Choisissez une option",
            max_values=1,
            min_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        embed = None
        match self.values[0]:
            case "antiraid":
                embed = embedBuilder(
                    fields={
                        "`/antiraid-config`": (
                            f"Afficher l'embed de configuration de l'antiraid", 
                            False
                        )
                    }
                )
            case "client":
                embed = embedBuilder(
                    fields={
                        "`/serveur-leave`": (
                            "*Quitter un serveur depuis l'id fournit*\n-# /serveur-leave [id]",
                            False
                        ),
                        "`/owner-panel`": (
                            "*Afficher l'embed de gestion des owners bot*",
                            False
                        ),
                        "`/whitelist-panel`": (
                            "*Afficher l'embed de gestion des whitelist bot*",
                            False
                        ),
                        "`/serveur-list`": (
                            "*Afficher la liste des serveur ou le bot est présent*",
                            False
                        ),
                        "`/banner-edit`": (
                            "*Modifier la bannière du bot*\n-# /banner-edit [url]",
                            False
                        ),
                        "`/name-edit`": (
                            "*Modifier le nom du bot*\n-# /name-edit [nom]",
                            False
                        ),
                        "`/pfp-edit`": (
                            "*Modifier la photo de profil du bot*\n-# /pfp-edit [url]",
                            False
                        ),
                        "`/set-status`": (
                            "*Modifier le status et la présence du bot*\n-# /set-status [option] [texte]", 
                            False
                        )
                    }
                )
            case "config": 
                embed = embedBuilder(
                    fields={
                        "`/autorole-config`": (
                            f"*Afficher l'embed de configuration des rôles à l'arrivée*",
                            False
                        ),
                        "`/badwords-config`": (
                            f"*Afficher l'embed de configuration des mots interdits*",
                            False
                        ),
                        "`/greet-message-config`": (
                            "*Configurer le message privé envoyé à l'arrivée*\n-# /greet-message-config [option]",
                            False
                        ),
                        "`/jail-config`": (
                            f"*Afficher l'embed de configuration de la commande prison*",
                            False
                        ),
                        "`/join-message-config`": (
                            "*Afficher l'embed de configuration du message à l'arrivée*",
                            False
                        ),
                        "`/onlypic-config`": (
                            "*Afficher l'embed de configuration des salons onlypics*",
                            False
                        ),
                        "`/role-reaction`": (
                            "*Configurer et envoyer un embed de rôle réaction*\n-# /role-reaction [role] [salon]",
                            False
                        ),
                        "`/soutien-config`": (
                            "*Afficher l'embed de configuration du role et du status de soutien*",
                            False
                        ),
                        "`tempvoice-config`": (
                            "*Afficher l'embed de configuration des salons vocaux temporaires*",
                            False
                        )
                    }
                )
            case "gestion": 
                embed = embedBuilder(
                    fields={
                        "`/blacklist`": (
                            "*Ajouter un membre à la blacklist et le bannir de tout les serveur possible*\n-# /blacklist [membre]",
                            False
                        ),
                        "`/channel-rename`": (
                            "*Modifier le nom d'un salon*\n-# /channel-rename [salon] [nom]",
                            False
                        ),
                        "`/clear-target`": (
                            "*Supprimer un nombre de message spécifique d'un seul utilistaeur*\n-# /clear-target [membre] [nombre] (salon)",
                            False
                        ),
                        "`/clear`": (
                            "*Supprimer un nombre de message spécifique*\n-# /clear [nombre]",
                            False
                        ),
                        "`/derank`": (
                            "*Retirer tout les rôles d'un membre*\n-# /derank [membre]", 
                            False
                        ),
                        "`lock`": (
                            "*Verouiller un salon textuel*\n-# /lock (salon)",
                            False
                        ),
                        "`/renew`": (
                            "*Renouveler un salon*\n-# /renew (salon)",
                            False
                        ),
                        "`/unlock`": (
                            "*Déverouiller un salon textuel*\n-# /unlock (salon)",
                            False
                        )
                    }
                )
            
            case "gw": 
                embed = embedBuilder(
                    fields={
                        "`/giveaway-start`": (
                            f"*Configurer et lancer un giveaway*\n-# /giveaway-start [gain] [temps] [unité] [gagnant] (par) (condition)",
                            False
                        ),
                        "`/giveaway-reroll`": (
                            f"*Recommencer le tirage au sort d'un giveaway*\n-# /giveaway-reroll [message] [gagnants]",
                            False
                        )
                    }
                )

            case "info": 
                embed = embedBuilder(
                    fields={
                        "`/channel-info`": (
                            "*Afficher les informations d'un salon*\n-# /channel-info [salon]",
                            False
                        ),
                        "`/member-info`": (
                            "*Afficher les informations d'un membre*\n-# /member-info [membre]",
                            False
                        ),
                        "`/role-info`": (
                            "*Afficher les informations d'un role*\n-# /role-info [role]",
                            False
                        ),
                        "`/serveur-info`": (
                            "*Afficher les informations du serveur*",
                            False
                        ),
                        "`/all-admins`": (
                            "*Afficher la liste de tout les membres ayant les permissions administrateur sur le serveur*",
                            False
                        ),
                        "`/all-bans`": (
                            "*Afficher la liste de tout les membres bannis du serveur*",
                            False
                        ),
                        "`/all-bot-admin`": (
                            "*Affichier la liste de tout les bots ayant les permissions administrateur sur le serveur*",
                            False
                        ),
                        "`/all-bots`": (
                            "*Afficher la liste de tout les bots présent sur le serveur*",
                            False
                        ),
                        "`/all-booster`": (
                            "*Afficher la liste de tout les membre qui boostent le serveur*",
                            False
                        ),
                        "`all-roles-members`": (
                            "*Afficher la liste de tout les membres possèdant un rôle spécifique*\n-# /all-roles-members [role]", 
                            False
                        ),
                        "`/stats-serveur`": (
                            "*Afficher les statistique du serveur*",
                            False
                        ),
                        "`/stats-voice`": (
                            "*Afficher les statistique vocales du serveur*",
                            False
                        )
                    }
                )
            case 'logs': 
                embed = embedBuilder(
                    fields={
                        "`/logs-panel`": (
                            "*Afficher l'embed de configuration et de gestion des logs*",
                            False
                        ),
                        "`/logs-auto`": (
                            "*Configurer les logs automatiquement*", 
                            False
                        )
                    }
                )
            case "mods": 
                embed = embedBuilder(
                    fields={
                        "`/role-add`": (
                            "*Ajouter un rôle à un membre*\n-# /role-add [membre] [role]",
                            False
                        ),
                        "`/ban`": (
                            "*Bannir un membre du serveur*\n-# /ban [membre] [option] (raison)",
                            False
                        ),
                        "`/jail`": (
                            "*Envoyer un membre en prison*\n-# /jail [membre]", 
                            False
                        ),
                        "`/kick`": (
                            "*Expulser un membre du serveur*\n-# /kick [membre] [option] (raison)",
                            False
                        ),
                        "`/warn-member`": (
                            "*Afficher le status des warns d'un membre*\n-# /warn-member [membre]",
                            False
                        ),
                        "`/mute`": (
                            "*Rendre un membre muet pour un temps définit (minutes)*\n-# /mute [membre] [temps] (raison)",
                            False
                        ),
                        "`/role-remove`": (
                            "*Retirer un rôle à un membre*\n-# /role-remove [membre] [role]",
                            False
                        ),
                        "`/warn`": (
                            "*Ajouter un warn à un membre*\n-# /warn [membre] (raison)",
                            False
                        )
                    }
                )
            case "utils": 
                embed = embedBuilder(
                    fields={
                        "`/emojis-add`": (
                            "*Cloner un émoji personnalisé venant d'un autre serveur*\n-# /emojis-add [emojis] [nom]",
                            False
                        ),
                        "`/embed`": (
                            "*Configurer et envoyer un embed personnalisé*",
                            False
                        ),
                        "`/find`": (
                            "*Chercher un membre dans les salons vocaux*\n-# /find [membre]",
                            False
                        ),
                        "`/invite-link`": (
                            "*Afficher le lien d'invitation du bot*",
                            False
                        ),
                        "`/mp`": (
                            "*Envoyer un message privé à un membre*\n-# /mp [membre] [message]",
                            False
                        ),
                        "`/pic`": (
                            "*Afficher la photo de profile d'un membre*\n-# /pic [membre]",
                            False
                        ),
                        "`/ping`": (
                            "*Afficher la latence du bot*",
                            False
                        ),
                        "`/say`": (
                            "*Envoyé un message depuis le bot*\n-# /say [message]",
                            False
                        ),
                        "`/serveur-invite`": (
                            "*Crée et afficher une invitation du serveur*\n-# /serveur-invite [salon]",
                            False
                        )
                    }
                )
            case "voice": 
                embed = embedBuilder(
                    fields={
                        "`/voice-deaf`": (
                            "*Rendre un membre en sourdine*\n-# /voice-deaf [option] [membre]",
                            False
                        ),
                        "`/voice-kick`": (
                            "*Expulser un membre d'un salon vocal*\n-# /voice-kick [membre]",
                            False
                        ),
                        "`/voice-lock`": (
                            "*Verouiller un salon vocal*\n-# /voice-lock [salon]",
                            False
                        ),
                        "`/voice-move-all`": (
                            "*Déplacer tout les membres présents en vocal dans votre salon vocal actuel*",
                            False
                        ),
                        "`/voice-move`": (
                            "*Déplacer un membre dans votre salon vocal actuel*\n-# /voice-mvoe [membre]",
                            False
                        ),
                        "`/voice-mute`": (
                            "*Rendre un membre muet dans un salon vocal*\n-# /vocie-mute [option] [membre]",
                            False
                        ),
                        "`/voice-unlock`": (
                            "*Déverouiller un salon vocal*\n-# /voice-unlock [salon]",
                            False
                        ),
                        "`/voice-afk`": (
                            "**Déplacer un membre dans le salon afk du serveur\n-# /voice-afk [membre]", 
                            False
                        ),
                        "`/voice-lock-all`": (
                            "*Verouiller tout les salon vocaux du serveur*",
                            False
                        ),
                        "`/voice-unlock-all`": (
                            "*Déverouiller tout les salon vocaux du serveur*",
                            False
                        )
                    }
                )
            case "home":
                embed = embedBuilder(
                    description=f"> *Voici le panel d'aide du bot {self.bot.user.mention}*\n\n> *Utilisez les menu deroulant pour afficher les differentes options*\n\n```[] = Obligatoire \n() = Optionnel```",
                )

        embed.title = "`🪄`・Panel d'aide"
        embed.color = embed_color()
        embed.set_footer(text=footer())
        embed.set_thumbnail(url=self.bot.user.avatar)
        view = discord.ui.View(timeout=None)
        view.add_item(selectHelp(self.userId, self.bot))
        return await interaction.response.edit_message(embed=embed, view=view)