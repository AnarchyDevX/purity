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
                except discord.Forbidden:
                    # Bot n'a pas les permissions
                    pass
                except discord.HTTPException:
                    # Erreur Discord API
                    pass
            else:
                depractatedRoles.append(roles)
        
        # Créer une copie pour éviter de modifier la liste pendant l'itération
        for role in depractatedRoles[:]:
            roleList.remove(role)        

        with open(f'./configs/{member.guild.id}.json', 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autoRole(bot))