import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class compteurPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="compteurs-add", description="Ajouter un salon permettant de compter une entitée")
    @app_commands.choices(
        counter=[
            app_commands.Choice(name="membres", value="member"),
            app_commands.Choice(name="membres en lignes", value="onlinemember"),
            app_commands.Choice(name="membres avec un rôle précis", value="memberrole"),
            app_commands.Choice(name="boost sur le serveur", value="boost"),
            app_commands.Choice(name="membres en vocal", value="membervoice")
        ],
        channel=[
            app_commands.Choice(name="vocal", value="voice"),
            app_commands.Choice(name="texte", value='text')
        ]
    )
    async def compteurAdd(self, interaction: discord.Interaction, counter: str, channel: str, role: discord.Role = None):
        if not await check_perms(interaction, 2): return

        channelName = ""

        match counter:
            case 'member':
                channelName = f"Membres: {interaction.guild.member_count}"
            case 'onlinemember':
                counts = sum(1 for member in interaction.guild.members if member.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd])
                channelName = f"En ligne: {counts}"
            case 'memberrole':
                channelName = f"{role.name}: {len(role.members)}"
            case 'boost':
                channelName = f"Boost: {interaction.guild.premium_subscription_count}"
            case "membervoice":
                counts = sum(1 for member in interaction.guild.members if member.voice)
                channelName = f"En Vocal: {counts}"


        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False, send_messages=False)
        }
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        countChannel = None
        if channel == "voice":
            countChannel = await interaction.guild.create_voice_channel(name=channelName, overwrites=overwrites) 
        else:
            countChannel = await interaction.guild.create_text_channel(name=channelName, overwrites=overwrites) 

        payload = {
            "channelType": counter,
            "role": None if role == None else role.id
        }
        guildJSON['compteurs'][str(countChannel.id)] = payload
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        embed = embedBuilder(
            title="`🧾`・Compteur configuré",
            description=f"*Le salon {countChannel.mention} à bien été crée.*",
            color=embed_color(),
            footer=footer()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(compteurPanel(bot))