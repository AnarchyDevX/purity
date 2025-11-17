import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import json
import re

class badwordsLearning(commands.Cog):
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
        if guildJSON is None:
            return
        
        # Vérifier si le learning est activé
        if not guildJSON.get('badwords_learning', {}).get('enabled', False):
            return
        
        # Ignorer si l'utilisateur a des permissions élevées
        if await check_id_perms(message.author, message.guild, 1):
            return
        
        # Détecter les suspicions de mots
        await self._detect_suspicious_words(message, guildJSON)
    
    async def _detect_suspicious_words(self, message: discord.Message, guildJSON: dict):
        """Détecter et compter les mots suspects basés sur des patterns linguistiques"""
        content = message.content.lower()
        
        # Nettoyer le contenu : enlever la ponctuation mais garder les espaces
        # Garder uniquement lettres, chiffres et espaces
        cleaned_content = re.sub(r'[^\w\s]', ' ', content)
        
        # Diviser le message en mots
        words = cleaned_content.split()
        
        # Filtrer les mots suspects basés sur plusieurs critères
        suspicious_words = []
        for word in words:
            if len(word) < 4:
                continue
            
            # Score de suspicion
            suspicion_score = 0
            
            # Pattern 1: Lettres répétées (ex: "fuuuuck", "niiiggeer")
            if re.search(r'(.)\1{2,}', word):
                suspicion_score += 2
            
            # Pattern 2: Mélange de lettres et chiffres suspect (ex: "fuck1", "n1gger")
            if re.search(r'\d', word) and re.search(r'[a-z]{3,}', word):
                suspicion_score += 1
            
            # Pattern 3: Caractères spéciaux pour contourner (ex: "f_u_c_k", "n!gger")
            # On les a déjà enlevés, mais on peut vérifier si le mot original en avait
            
            # Pattern 4: Mots très courts avec beaucoup de consonnes (peu probable en français/anglais normal)
            consonants = len(re.findall(r'[bcdfghjklmnpqrstvwxyz]', word))
            vowels = len(re.findall(r'[aeiouy]', word))
            if len(word) <= 6 and consonants > vowels * 2 and vowels > 0:
                suspicion_score += 1
            
            # Pattern 5: Mots contenant des combinaisons de lettres rares
            rare_combinations = ['ck', 'gg', 'xx', 'zz', 'ff', 'kk']
            if any(combo in word for combo in rare_combinations):
                suspicion_score += 1
            
            # Pattern 6: Mots avec trop peu de voyelles pour leur longueur
            if len(word) >= 5 and vowels == 0:
                suspicion_score += 2
            
            # Si le score de suspicion est suffisant, ajouter le mot
            if suspicion_score >= 1:
                suspicious_words.append((word, suspicion_score))
        
        for word_data in suspicious_words:
            # Extraire le mot et le score
            if isinstance(word_data, tuple):
                word, suspicion_score = word_data
            else:
                word = word_data
                suspicion_score = 1
            # Vérifier si ce n'est pas déjà un badword
            if word in guildJSON.get('badwords', []):
                continue
            
            # Initialiser les suspicions si nécessaire
            if 'badwords_learning' not in guildJSON:
                guildJSON['badwords_learning'] = {
                    'enabled': False,
                    'suspicion_channel': None,
                    'threshold': 3,
                    'suspicions': {}
                }
            
            if 'suspicions' not in guildJSON['badwords_learning']:
                guildJSON['badwords_learning']['suspicions'] = {}
            
            # Incrémenter le compteur
            if word not in guildJSON['badwords_learning']['suspicions']:
                guildJSON['badwords_learning']['suspicions'][word] = {
                    'count': 0,
                    'last_seen': None,
                    'first_seen_by': None,
                    'first_seen_message': None,
                    'alerted': False
                }
            
            guildJSON['badwords_learning']['suspicions'][word]['count'] += 1
            guildJSON['badwords_learning']['suspicions'][word]['last_seen'] = message.created_at.isoformat()
            
            # Enregistrer les informations du premier message
            if guildJSON['badwords_learning']['suspicions'][word]['first_seen_by'] is None:
                guildJSON['badwords_learning']['suspicions'][word]['first_seen_by'] = message.author.id
                guildJSON['badwords_learning']['suspicions'][word]['first_seen_message'] = message.content
            
            # Sauvegarder les suspicions
            with open(f"./configs/{message.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4, ensure_ascii=False)
            
            # Vérifier si on atteint le seuil et si on n'a pas déjà alerté
            threshold = guildJSON['badwords_learning'].get('threshold', 3)
            if guildJSON['badwords_learning']['suspicions'][word]['count'] >= threshold and not guildJSON['badwords_learning']['suspicions'][word].get('alerted', False):
                # Marquer comme alerté
                guildJSON['badwords_learning']['suspicions'][word]['alerted'] = True
                
                # Sauvegarder à nouveau avec le flag alerted
                with open(f"./configs/{message.guild.id}.json", 'w', encoding='utf-8') as f:
                    json.dump(guildJSON, f, indent=4, ensure_ascii=False)
                
                # Envoyer l'embed de suspicion
                await self._send_suspicion_alert(message, word, guildJSON)
    
    async def _send_suspicion_alert(self, message: discord.Message, word: str, guildJSON: dict):
        """Envoyer une alerte de suspicion"""
        channel_id = guildJSON['badwords_learning'].get('suspicion_channel')
        if not channel_id:
            return
        
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return
        
        suspicion_data = guildJSON['badwords_learning']['suspicions'][word]
        first_seen_by = self.bot.get_user(suspicion_data['first_seen_by'])
        
        embed = embedBuilder(
            title="`⚠️`・Suspicion de badword détectée",
            description=f"Le mot **`{word}`** a été utilisé **{suspicion_data['count']}** fois.",
            color=0xFFA500,  # Orange
            fields={
                "`📝`・Informations:": (
                    f"> `👤`・**Premier auteur:** {first_seen_by.mention if first_seen_by else 'Inconnu'}\n"
                    f"> `📜`・**Premier message:** `{suspicion_data['first_seen_message'][:100]}...`\n"
                    f"> `📅`・**Dernière apparition:** <t:{int(message.created_at.timestamp())}:R>\n"
                    f"> `🔢`・**Compteur:** `{suspicion_data['count']}`",
                    False
                )
            },
            footer=footer()
        )
        
        from views.badwords.approveSuspicion import ApproveSuspicionButton
        from views.badwords.rejectSuspicion import RejectSuspicionButton
        
        view = discord.ui.View(timeout=None)
        view.add_item(ApproveSuspicionButton(word))
        view.add_item(RejectSuspicionButton(word))
        
        await channel.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(badwordsLearning(bot))

