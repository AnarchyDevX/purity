import json
from discord.ext import commands
import discord
import os
from functions.functions import *
from core.embedBuilder import embedBuilder

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
                            description=f"*Un membre a essayer de m'ajouter au serveur **{guild.name}**. L'antijoin etant activé, je l'ai donc quitté*",
                            color=embed_color(),
                            footer=footer()
                        )
                        try:
                            await owner.send(embed=embed)
                        except Exception as e:
                            pass
                    return await guild.leave()
        else:
            payload = """{
    "ownerlist": [],
    "whitelist": [],
    "badwords": [],
    "lockedvoice": [],
    "logs": {
        "modlogs": {
            "alive": false,
            "channel": null
        },
        "msglogs": {
            "alive": false,
            "channel": null
        },
        "raidlogs": {
            "alive": false,
            "channel": null
        },
        "voicelogs": {
            "alive": false,
            "channel": null
        },
        "ranklogs": {
            "alive": false,
            "channel": null
        },
        "joinleavelogs": {
            "alive": false,
            "channel": null
        }
    },
    "antiraid": {
        "antibot": false,
        "antilien": false,
        "badwords": false,
        "channels": {
            "create": false,
            "edit": false,
            "delete": false
        },
        "roles": {
            "create": false,
            "edit": false,
            "delete": false
        },
        "rank": {
            "up": false,
            "down": false
        },
        "webhook": false
    },
    "configuration": {
        "autoreact": {},
        "rolereact": {},
        "autorole": [],
        "tempvoices": {
            "active": [],
            "configs": {}
        }
    },
    "warndb": {
        "maxwarn": 10,
        "sanction": "kick",
        "users": {}
    },
    "tickets": {
        "logs": 101010010101,
        "transcripts": true,
        "roles": [],
        "claim": true,
        "buttons": {}
    },
    "onlypic": [],
    "greeting": {
        "active": true,
        "type": "message",
        "channel": 1300941717821853737,
        "mention": true
    },
    "greetmsg": {
        "alive": false,
        "content": ""
    }, 
    "soutien": {
        "active": false,
        "needed": "rien",
        "role": null
    }
}
"""
            with open(f"./configs/{guild.id}.json", 'w', encoding='utf-8') as f:
                f.write(payload)
                f.close()

            for owner in config['buyer']:
                for guilds in self.bot.guilds:
                    owner = discord.utils.get(guilds.members, id=owner)
                    if owner:
                        embed = embedBuilder(
                            title="`➕`・Ajout de serveur",
                            description=f"*j'ai été ajouter au serveur **{guild.name}***",
                            color=embed_color(),
                            footer=footer()
                        )
                        try:
                            await owner.send(embed=embed)
                        except Exception as e:
                            pass

async def setup(bot):
    await bot.add_cog(guildAdd(bot))