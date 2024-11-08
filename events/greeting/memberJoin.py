import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class greetMember(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guildJSON = load_json_file(f'./configs/{member.guild.id}.json')
        if guildJSON['greeting']['active'] == False: return
        channel = discord.utils.get(member.guild.channels, id=guildJSON['greeting']['channel'])
        if not channel: return
        mention = f"***{member.mention}***"        
        if guildJSON['greeting']['mention'] == True:
            mention = member.mention 
        if guildJSON['greeting']['type'] == "embed":
            embed = embedBuilder(
                title=f"`✨`・Bienvenue {member.name}",
                description=f"*{mention} vient de rejoindre le serveur ! Nous sommes maintenant {member.guild.member_count} sur le serveur.*",
                color=embed_color(),
                footer=footer()
            )
            return await channel.send(embed=embed, content=member.mention if guildJSON['greeting']['mention'] == True else None)
        elif guildJSON['greeting']['type'] == 'message':
            await channel.send(content=f"*{mention} vient de rejoindre le serveur ! Nous sommes maintenant {member.guild.member_count} sur le serveur.*")

async def setup(bot):
    await bot.add_cog(greetMember(bot))
