import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
import aiohttp

class EmojiCloner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="emojis-add", description="Cloner un emojis venant d'un autre serveur")
    @app_commands.checks.has_permissions(manage_emojis=True)
    async def clone_emoji(self, interaction: discord.Interaction, emoji: str, name: str):
        await interaction.response.defer()
        try:

            if not (emoji.startswith('<') and emoji.endswith('>')):
                return await err_embed(
                    interaction, 
                    title="Emojis Invalide",
                    description="Vous devez fournir un emojis valide",
                    followup=True
                )

            splited = emoji.replace('<', '').replace('>', '').split(':')
            emojiId = int(splited[-1])
            is_animated = emoji.startswith('<a:')

            emojiUrl = f"https://cdn.discordapp.com/emojis/{emojiId}.{'gif' if is_animated else 'png'}"

            async with aiohttp.ClientSession() as session:
                async with session.get(emojiUrl) as response:
                    if response.status != 200:
                        return await err_embed(
                            interaction, 
                            title="Erreur la recuperation de l'emojis",
                            description="Je n'ai pas reussi a récuprer l'emojis",
                            followup=True
                        )
                    image = await response.read()

            new_emoji = await interaction.guild.create_custom_emoji(
                name=name, 
                image=image
            )

            embed = embedBuilder(
                title="`✨`・Emoji crée",
                description=f"*L'emojis {new_emoji} a été ajouté au serveur en tant que **{name}***",
                footer=footer(),
                color=embed_color()
            )
            await interaction.followup.send(embed=embed)

        except discord.Forbidden:
            return await err_embed(
                interaction, 
                title="Impossible de créer l'emoji",
                description="Je n'ai pas réussi à créer l'emoji. Permission manquante.",
                followup=True
            )
        except discord.HTTPException:
            return await err_embed(
                interaction, 
                title="Impossible de créer l'emoji",
                description="Je n'ai pas réussi à créer l'emoji. Erreur Discord API.",
                followup=True
            )
        
async def setup(bot):
    await bot.add_cog(EmojiCloner(bot))