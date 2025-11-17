import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class guildWebhookCreateAntiraid(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel):
        guildJSON = load_json_file(f"./configs/{channel.guild.id}.json")
        if guildJSON is None: return  # Config n'existe pas
        if guildJSON['antiraid']['webhook'] == True:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create):
                if isinstance(entry.target, discord.Webhook) and getattr(entry.target, 'channel', None):
                    if entry.target.channel.id == channel.id:
                        if entry.user.id == self.bot.user.id:
                            return
                        if await check_id_perms(entry.user, entry.user.guild, 3): return
                        
                        # Vérification de timing pour éviter les race conditions
                        time_diff = (discord.utils.utcnow() - entry.created_at).total_seconds()
                        if time_diff > 5:  # Ignorer les entries anciennes de plus de 5 secondes
                            continue
                            
                        try:
                            await entry.user.ban(reason="Antiraid: Webhook Créé")
                        except discord.Forbidden:
                            # Bot n'a pas les permissions pour bannir
                            pass
                        except discord.HTTPException:
                            # Erreur Discord API
                            pass
                            
                        try:
                            await entry.target.delete(reason="Antiraid: Webhook")
                        except discord.Forbidden:
                            return
                        except discord.NotFound:
                            # Webhook déjà supprimé
                            return
                        except discord.HTTPException:
                            return
                        break

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(guildWebhookCreateAntiraid(bot))
