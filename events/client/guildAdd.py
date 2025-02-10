import json
from discord.ext import commands
import discord
import os
from functions.functions import *
from core.embedBuilder import embedBuilder
from models.configuration import configuration 

class guildAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        config = load_json()
        if config['guildjoin'] == False:
            for owner in config['buyer']:
                for guilds in self.bot.guilds:
                    owner = discord.utils.get(guilds.members, id=owner)
                    if owner:
                        embed = embedBuilder(
                            title="`➕`・Ajout de serveur",
                            description=f"*Un membre a essayé de m'ajouter au serveur **{guild.name}**. L'antijoin étant activé, je l'ai donc quitté*",
                            color=embed_color(),
                            footer=footer()
                        )
                        try:
                            await owner.send(embed=embed)
                        except Exception:
                            continue
                    return await guild.leave()
        else:
            with open(f"./configs/{guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(configuration, f, indent=4, ensure_ascii=False)  

            for owner in config['buyer']:
                for guilds in self.bot.guilds:
                    owner = discord.utils.get(guilds.members, id=owner)
                    if owner:
                        embed = embedBuilder(
                            title="`➕`・Ajout de serveur",
                            description=f"*J'ai été ajouté au serveur **{guild.name}***",
                            color=embed_color(),
                            footer=footer()
                        )
                        try:
                            await owner.send(embed=embed)
                        except Exception as e:
                            print(e)
                            continue

async def setup(bot):
    await bot.add_cog(guildAdd(bot))
