import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class tempVoiceRemove(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="tempvoice-remove", description="Retirer une configuration de creations de salon vocal temporaires")
    async def tempVoiceRemove(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
    
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        channelId = False
        for element in guildJSON['configuration']['tempvoices']['configs']:
            if int(element) == channel.id:
                channelId = True
                break

        if channelId == False:
            return await err_embed(
                interaction, 
                title="Salon non configuré",
                description=f"Le salon {channel.mention} n'est pas présent dans la liste des salons de créations de vocales temporaires"
            )

        del guildJSON['configuration']['tempvoices']['configs'][str(channel.id)]
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed: embedBuilder = embedBuilder(
            title="`🔊`・Configuration supprimée",
            description=f"*Le salon {channel.mention} à été supprimé des salon de creations de vocales temporaires.*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tempVoiceRemove(bot))