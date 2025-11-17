import discord
import asyncio
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class giveawayReactionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # Ignorer les réactions du bot
        if payload.user_id == self.bot.user.id:
            return
        
        # Vérifier si c'est un giveaway actif (tout est persistant, rien en mémoire)
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        guildJSON = load_json_file(f"./configs/{guild.id}.json")
        if guildJSON is None:
            return
        
        if 'giveaways' not in guildJSON:
            return
        
        giveaway_data = guildJSON['giveaways'].get(str(payload.message_id))
        if not giveaway_data:
            return
        
        config = giveaway_data.get('config', {})
        
        # Vérifier si c'est le bon emoji (l'emoji est dans giveaway_data, pas dans config)
        emoji = giveaway_data.get("emoji", config.get("emoji", "🎉"))
        reaction_emoji = str(payload.emoji)
        if reaction_emoji != emoji:
            return
        
        # Récupérer le membre
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        
        member = guild.get_member(payload.user_id)
        if not member:
            return
        
        # Vérifier les conditions
        can_participate, reason = self._check_giveaway_conditions(member, guild, config)
        
        # Envoyer un message éphémère (en DM ou message temporaire dans le channel)
        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return
        
        if can_participate:
            embed = embedBuilder(
                title="`✅`・Inscription confirmée",
                description=f"Vous avez bien été inscrit au giveaway **{config.get('gain', 'Giveaway')}** !",
                color=0x00FF00,  # Vert
                footer=footer()
            )
            
            # Essayer d'envoyer en DM d'abord
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                # Si les DMs sont désactivés, envoyer dans le channel et supprimer après
                try:
                    msg = await channel.send(f"{member.mention}", embed=embed)
                    await asyncio.sleep(5)
                    await msg.delete()
                except:
                    pass
        else:
            embed = embedBuilder(
                title="`❌`・Inscription refusée",
                description=f"Vous ne pouvez pas participer à ce giveaway.\n\n**Raison:** {reason}",
                color=0xFF0000,  # Rouge
                footer=footer()
            )
            
            # Essayer d'envoyer en DM d'abord
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                # Si les DMs sont désactivés, envoyer dans le channel et supprimer après
                try:
                    msg = await channel.send(f"{member.mention}", embed=embed)
                    await asyncio.sleep(5)
                    await msg.delete()
                except:
                    pass
            
            # Retirer la réaction
            try:
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, member)
            except:
                pass
    
    def _check_giveaway_conditions(self, member: discord.Member, guild: discord.Guild, config: dict) -> tuple[bool, str]:
        """Vérifie si un membre peut participer au giveaway. Retourne (can_participate, reason)"""
        
        # Rôle obligatoire
        if config.get("role_obligatoire"):
            role = guild.get_role(config["role_obligatoire"])
            if role and role not in member.roles:
                # Utiliser le nom du rôle au lieu de la mention pour les DMs
                return False, f"Vous devez avoir le rôle **{role.name}** pour participer."
        
        # Rôle interdit
        if config.get("role_interdit"):
            role = guild.get_role(config["role_interdit"])
            if role and role in member.roles:
                # Utiliser le nom du rôle au lieu de la mention pour les DMs
                return False, f"Vous ne pouvez pas participer avec le rôle **{role.name}**."
        
        # Présence en vocal
        if config.get("presence_vocal"):
            if not member.voice or not member.voice.channel:
                return False, "Vous devez être présent en vocal pour participer."
        
        # TODO: Vérifier niveau et invitations si système implémenté
        # Pour l'instant, on retourne True si les conditions de base sont respectées
        
        return True, ""

async def setup(bot):
    await bot.add_cog(giveawayReactionHandler(bot))

