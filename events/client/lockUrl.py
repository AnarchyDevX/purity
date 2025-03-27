import discord
from discord.ext import commands
from core.embedBuilder import embedBuilder 

class LockUrl(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        print(before.vanity_url)
        print(after.vanity_url)
        if before.vanity_url != after.vanity_url:
            splited = before.vanity_url.split("/")
            code = splited[2]
            try:
                await after.edit(vanity_code=code)
            except Exception as e:
                print(e)
                pass
        

async def setup(bot):
    await bot.add_cog(LockUrl(bot))
