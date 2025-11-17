import asyncio
import discord
from discord.ext import commands
from functions.functions import *

class badwordsAntiraid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message, discord.Message):
            return
        if message.author.id == self.bot.user.id:
            return
        if message.author.bot:
            return
        guildJSON = load_json_file(f"./configs/{message.guild.id}.json")
        if guildJSON is None: return  # Config n'existe pas
        if await check_id_perms(message.author, message.guild, 1): return

        # Vérifier que l'antiraid badwords est activé
        if not guildJSON.get('antiraid', {}).get('badwords', False):
            return
        
        # Vérifier que la liste des badwords n'est pas vide
        badwords_list = guildJSON.get('badwords', [])
        if not badwords_list:
            return
        
        # Convertir le message en minuscules pour une détection insensible à la casse
        content_lower = message.content.lower()
        
        for element in badwords_list:
            # Vérifier en minuscules pour être insensible à la casse
            if element.lower() in content_lower:
                try:
                    await message.delete()
                    response = await message.channel.send(f"{message.author.mention} Vous n'avez pas le droit d'utiliser ce mot ici !")
                    await asyncio.sleep(2)
                    await response.delete()
                except discord.Forbidden:
                    # Bot n'a pas les permissions pour supprimer
                    pass
                except discord.NotFound:
                    # Message déjà supprimé
                    pass
                except discord.HTTPException:
                    # Erreur Discord API
                    pass
                return
                
async def setup(bot):
    await bot.add_cog(badwordsAntiraid(bot))
