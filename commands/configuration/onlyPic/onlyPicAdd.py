import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class onlyPicAdd(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="onlypic-enable", description="Active le mode image uniquement dans un salon")
    async def onlypicadd(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        onlypicList = guildJSON['onlypic']

        if channel.id in onlypicList:
            return await err_embed(
                interaction,
                title="Salon déja configurer",
                description=f"Le salon {channel.mention} possède déjà le mode `onlypic` activé"
            )
        
        onlypicList.append(channel.id)
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        embed = embedBuilder(
            title="`🥏`・Onlypic",
            description=f"*Le mode `onlypic` a été activé dans le salon {channel.mention}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(onlyPicAdd(bot))