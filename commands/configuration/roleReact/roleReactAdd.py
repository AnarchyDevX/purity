import json
import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class roleReactAdd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="role-reaction-add", description="Ajouter un role reaction")
    async def roleReactAdd(self, interaction: discord.Interaction, role: discord.Role, mid: str, emoji: str):
        check: bool = await check_perms(interaction, 2)
        if check == False:
            return
        
        if not (emoji.startswith('<') and emoji.endswith('>')):
            return await err_embed(
                interaction, 
                title="Emoji Invalide",
                description="Vous devez fournir un emoji valide"
            )
        
        splited = emoji.replace('<', '').replace('>', '').split(':')
        emojiId = int(splited[-1])
        emojis = discord.utils.get(interaction.guild.emojis, id=emojiId)
        if not emojis:
            return await err_embed(
                interaction, 
                title="Emoji invalide",
                description="Vous devez fourni un émoji valide et présent dans le serveur."
            )
        
        try:
            mid: int = int(mid)
        except ValueError:
            return await err_embed(
                interaction,
                title="Message invalide",
                description="L'id du message que vous avez fournit est invalide."
            )
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        guildJSON['configuration']['rolereact'][str(mid)] = {
            "emojiId": emojis.id,
            "roleId": role.id
        }
        json.dump(guildJSON, open(f'./configs/{interaction.guild.id}.json', 'w'), indent=4)
        embed: embedBuilder = embedBuilder(
            title="`➕`・Role réaction configuré",
            description=f"Le role réaction a bin été configurer",
            footer=footer(),
            color=embed_color(),
            fields={
                "`✨`・Informations sur l'ajout": (
                    f"> `🎯`・**Emoji Ciblé:** {emojis}\n"
                    f"> `📀`・**Rôle Ajouté:** {role.mention}\n"
                    f"> `🪡`・**Message Ciblé:** {mid}\n",
                    False
                )
            }
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(roleReactAdd(bot))