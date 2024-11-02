import discord
from discord.ext import commands
from functions.functions import *

class autoRole(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guildJSON = load_json_file(f'./configs/{member.guild.id}.json')
        roleList: list[int] = guildJSON['configuration']['autorole']
        depractatedRoles: list[int] = []
        for roles in roleList:
            role: discord.Role | None = discord.utils.get(member.guild.roles, id=roles)
            if role:
                try:
                    await member.add_roles(role)
                except Exception:
                    pass
            else:
                depractatedRoles.append(roles)
        
        for role in depractatedRoles:
            roleList.remove(role)        

        json.dump(guildJSON, open(f'./configs/{member.guild.id}.json', 'w'), indent=4)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autoRole(bot))