import discord
import os
import json
from typing import List
from discord.ext import commands
from core._colors import Colors
from loaders.commandsLoader import commandsLoader
from loaders.eventsLoader import eventsLoader
from functions.functions import load_json_file

class ready(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.C: Colors = Colors()

    async def commands_load(self):
        a: commandsLoader = commandsLoader(self.bot)
        await a.load_commands()

    async def events_load(self):
        a: eventsLoader = eventsLoader(self.bot)
        eventsCount = await a.load_events()
        return eventsCount

    async def commands_count(self, commandsList: List[discord.app_commands.Command]):
        commandsCount = sum(1 for _ in commandsList)
        return commandsCount

    async def reload_persistent_views(self):
        """Recharge les vues persistantes des tickets et captchas au démarrage du bot"""
        from views.ticketView.ticketSelectButton import ticketSelectButton
        from views.captchaView.verify import startVerify
        
        configs_dir = "./configs"
        if not os.path.exists(configs_dir):
            return
        
        reloaded_count = 0
        for filename in os.listdir(configs_dir):
            if not filename.endswith('.json'):
                continue
            
            try:
                guild_id = int(filename[:-5])  # Enlever .json
                guildJSON = load_json_file(f"{configs_dir}/{filename}")
                
                if guildJSON is None:
                    continue
                
                # Vérifier si le serveur existe et si le bot y est
                guild = self.bot.get_guild(guild_id)
                if guild is None:
                    continue
                
                # Recharger les vues des tickets
                updated_buttons = False

                if 'tickets' in guildJSON and 'buttons' in guildJSON['tickets']:
                    buttons = guildJSON['tickets']['buttons']
                    if isinstance(buttons, dict):
                        for panel_id, panel_data in buttons.items():
                            try:
                                channel_id = panel_data.get('channel_id')
                                message_id = panel_data.get('message_id')
                                category_id = panel_data.get('category_id')
                                options_list = panel_data.get('options_list', [])
                                custom_id = panel_data.get('custom_id')

                                if not all([channel_id, message_id, category_id]):
                                    continue
                                
                                # Récupérer le channel et la catégorie
                                channel = guild.get_channel(channel_id)
                                category = guild.get_channel(category_id)
                                
                                if channel is None or category is None:
                                    continue
                                
                                # Vérifier que le message existe encore
                                try:
                                    message = await channel.fetch_message(message_id)
                                except (discord.NotFound, discord.Forbidden):
                                    # Le message n'existe plus, on peut le supprimer de la config
                                    continue
                                
                                if not custom_id:
                                    custom_id = f"ticket_select_{message_id}"
                                    panel_data['custom_id'] = custom_id
                                    updated_buttons = True

                                view = discord.ui.View(timeout=None)
                                view.add_item(ticketSelectButton(self.bot, None, category, options_list, custom_id=custom_id))
                                
                                # Ajouter la vue au bot pour la persistance
                                self.bot.add_view(view, message_id=message_id)
                                reloaded_count += 1
                                
                            except Exception as e:
                                print(f"{self.C.RED}[ERROR] {self.C.WHITE}Erreur lors du rechargement du panel {panel_id} pour le serveur {guild_id}: {e}")
                                continue
                
                # Recharger les vues des captchas
                if 'captcha' in guildJSON and isinstance(guildJSON['captcha'], dict):
                    captcha_data = guildJSON['captcha']
                    channel_id = captcha_data.get('channel_id')
                    message_id = captcha_data.get('message_id')
                    role_id = captcha_data.get('role_id')
                    
                    if all([channel_id, message_id, role_id]):
                        try:
                            channel = guild.get_channel(channel_id)
                            role = guild.get_role(role_id)
                            
                            if channel is None or role is None:
                                continue
                            
                            # Vérifier que le message existe encore
                            try:
                                message = await channel.fetch_message(message_id)
                            except (discord.NotFound, discord.Forbidden):
                                # Le message n'existe plus
                                continue
                            
                            # Recréer la vue
                            view = discord.ui.View(timeout=None)
                            view.add_item(startVerify(self.bot, role))
                            
                            # Ajouter la vue au bot pour la persistance
                            self.bot.add_view(view)
                            reloaded_count += 1
                            
                        except Exception as e:
                            print(f"{self.C.RED}[ERROR] {self.C.WHITE}Erreur lors du rechargement du captcha pour le serveur {guild_id}: {e}")
                            continue
                                
                if updated_buttons:
                    try:
                        with open(f"{configs_dir}/{filename}", 'w', encoding='utf-8') as f:
                            json.dump(guildJSON, f, indent=4, ensure_ascii=False)
                    except Exception as e:
                        print(f"{self.C.RED}[ERROR] {self.C.WHITE}Impossible de sauvegarder les boutons mis à jour pour {guild_id}: {e}")

            except (ValueError, KeyError):
                continue
        
        if reloaded_count > 0:
            print(f"{self.C.GREEN}[SUCCESS] {self.C.WHITE}Vues persistantes rechargées: {reloaded_count}")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"{self.C.YELLOW}[UPDATING] {self.C.WHITE}Loading commands...")
        await self.commands_load()
        eventsCount = await self.events_load()
        print(f"{self.C.GREEN}[SUCCESS] {self.C.WHITE}Commands loaded !")
        print(f"{self.C.YELLOW}[UPDATING] {self.C.WHITE}Syncing commands...")
        await self.bot.tree.sync()
        print(f"{self.C.GREEN}[SUCCESS] {self.C.WHITE}Commands synced !")
        print(f"{self.C.YELLOW}[UPDATING] {self.C.WHITE}Initialisation du système de pré-tickets...")
        # Initialiser le PreTicketHandler
        from functions.preticketHandler import PreTicketHandler
        if not hasattr(self.bot, 'preticket_handler'):
            self.bot.preticket_handler = PreTicketHandler(self.bot)
        print(f"{self.C.GREEN}[SUCCESS] {self.C.WHITE}Système de pré-tickets initialisé !")
        print(f"{self.C.YELLOW}[UPDATING] {self.C.WHITE}Rechargement des vues persistantes...")
        await self.reload_persistent_views()
        print(f"{self.C.YELLOW}[UPDATING] {self.C.WHITE}Rechargement des giveaways actifs...")
        # Recharger les giveaways actifs
        giveaway_cog = self.bot.get_cog('gstart')
        if giveaway_cog:
            await giveaway_cog.reload_active_giveaways()
        print(f"{self.C.BLUE}[LOGGED] {self.C.WHITE}Logged as {self.bot.user.name} | {self.bot.user.id}")
        cCount = await self.commands_count(self.bot.tree.walk_commands())
        print(f"{self.C.RED}[INFO] {self.C.WHITE}Commands loaded: {cCount}")
        print(f"{self.C.RED}[INFO] {self.C.WHITE}Events loaded: {eventsCount}")
    
    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        print(f"{self.C.RED}[DISCONNECT] {self.C.WHITE}Bot disconnected from Discord")
    
    @commands.Cog.listener()
    async def on_resume(self) -> None:
        print(f"{self.C.GREEN}[RESUME] {self.C.WHITE}Bot reconnected to Discord")

async def setup(bot):
    await bot.add_cog(ready(bot))