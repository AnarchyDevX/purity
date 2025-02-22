# from discord.ext import commands, tasks
# from functions.functions import *

# class apiUpdater(commands.Cog):
#     def __init__(self, bot):
#         self.bot: commands.Bot = bot
#         self.apiupdater.start()

#     @tasks.loop(minutes=6)
#     async def apiupdater(self):
#         await self.bot.wait_until_ready()
#         config = load_json()
#         channel = self.bot.get_channel(config['apichannel'])
#         if channel:
#             try:
#                 await channel.edit(name=f"🟢・API: {round(self.bot.latency * 1000)}ms")
#             except Exception as e:
#                 print(e)

# async def setup(bot):
#     await bot.add_cog(apiUpdater(bot))