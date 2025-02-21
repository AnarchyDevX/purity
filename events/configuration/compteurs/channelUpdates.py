import discord
from discord.ext import commands, tasks
from functions.functions import *
from core.embedBuilder import embedBuilder

class channelUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.compteurUpdate.start()

    @tasks.loop(minutes=6)
    async def compteurUpdate(self):

        toDeleteList = []
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            guildJSON = load_json_file(f"./configs/{guild.id}.json")
            for element in guildJSON['compteurs']:
                channel = guild.get_channel(int(element))
                if channel:
                    channelName = ""
                    role = guild.get_role(int(guildJSON['compteurs'][element]['role'])) if guildJSON['compteurs'][element]['role'] else None
                    match guildJSON['compteurs'][element]['channelType']:
                        case 'member':
                            channelName = channel.name.split(":")[0] + ": " + str(guild.member_count)
                        case 'onlinemember':
                            counts = sum(1 for member in guild.members if member.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd])
                            channelName = channel.name.split(":")[0] + ": " + str(counts)
                        case 'memberrole':
                            channelName = channel.name.split(":")[0] + ": " + str(len(role.members))
                        case 'boost':
                            channelName = channel.name.split(":")[0] + ": " + str(guild.premium_subscription_count)
                        case "membervoice":
                            counts = sum(1 for member in guild.members if member.voice)
                            channelName = channel.name.split(":")[0] + ": " + str(counts)
                    try:
                        await channel.edit(name=channelName)
                    except Exception: 
                        pass
                else:
                    toDeleteList.append(element)

            for element in toDeleteList:
                del guildJSON['compteurs'][element]
                json.dump(guildJSON, open(f'./configs/{guild.id}.json', 'w'), indent=4)
                    

async def setup(bot):
    await bot.add_cog(channelUpdate(bot))