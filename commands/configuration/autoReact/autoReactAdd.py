from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class autoReact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @app_commands.command(name="reaction-auto-add", description="Ajouter un autoréact")
    async def autoreactadd(self, interaction: discord.Interaction, message: str, reaction: str, channel: discord.TextChannel):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        emoji = discord.utils.get(interaction.guild.emojis, name=reaction)
        if not emoji: 
            return await err_embed(
                interaction,
                title="Emoji non valide",
                description="Le nom de l'emoji que vous avez fournit est invalide. (il faut mettre le nom de l'emojis, pas l'emoji lui meme.)"
            )
        guildJSON = load_json_file(f'./configs/{interaction.guild.id}.json')
        guildJSON['configuration']["autoreact"][str(emoji.id)] = {
            "content": message,
            "channel": channel.id
        }
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed: embedBuilder = embedBuilder(
            title="`➕`・Reaction automatique ajoutée",
            description=f"*La réaction <:{emoji.name}:{emoji.id}> sera désormais ajouter a tout les messages contenant **{message}** dans le salon {channel.mention}*",
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.defer()
        message: discord.Message = await interaction.followup.send(embed=embed)
        await message.add_reaction(emoji)


async def setup(bot: commands.Bot):
    await bot.add_cog(autoReact(bot))