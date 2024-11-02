import discord
from typing import Dict, Any
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class tempVoiceAdd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="tempvoice-add", description="Configurer un salon de creations de vocal temporaires")
    @app_commands.describe(
        channel="Le salon vocal où la commande sera appliquée",
        catergory="La catégorie où sera créé le salon vocal temporaire"
    )
    async def tempVoiceAdd(self, interaction: discord.Interaction, channel: discord.VoiceChannel, catergory: discord.CategoryChannel):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        guildJSON: Dict[str, Any] = load_json_file(f'./configs/{interaction.guild.id}.json')
        channelId: bool = False
        for item in guildJSON['configuration']['tempvoices']['configs']:
            if int(item) == channel.id:
                channelId = True
                break
        
        if channelId == True:
            return await err_embed(
                interaction,
                title="Salon déja utilisé",
                description=f"Le salon {channel.mention} est déjà utilisé comme salon pour crée des vocales temporaires"
            )
        
        payloads: dict[str, int] = {
            "category": catergory.id
        }
        guildJSON['configuration']['tempvoices']['configs'][str(channel.id)] = payloads
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)

        embed: embedBuilder = embedBuilder(
            title="`🔊`・Vocale temporaires configurée",
            description=f"*Le salon {channel.mention} à été configuré comme salon de création de vocaux temporaires.*\n*Les salon seronts crées dans la categorie **{catergory.name}***",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(tempVoiceAdd(bot))