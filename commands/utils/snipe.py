import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class snipeDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped = {"delete": {}, "edit": {}}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        
        self.sniped["delete"][message.channel.id] = {
            "content": message.content,
            "author": message.author.id,
            "time": format_date("all", message.created_at)
        }

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        
        self.sniped["edit"][before.channel.id] = {
            "before": before.content,
            "after": after.content,
            "author": before.author.id,
            "time": format_date("all", after.edited_at)
        }

    @app_commands.command(name="snipe", description="Obtenir le dernier message supprimé ou modifier dans un salon aux choix")
    @app_commands.choices(
        action=[
            app_commands.Choice(name="Supprimé", value="delete"),
            app_commands.Choice(name="Modifié", value="edit")
        ]
    )
    async def snipe(self, interaction: discord.Interaction, action: str, channel: discord.TextChannel = None):
        channel = interaction.channel if channel == None else channel
        if channel.id in self.sniped[action]:
            if action == "delete":
                embed = embedBuilder(
                    title="`🔭`・Message supprimé",
                    description=f"Voici le dernier message supprimé dans le salon {channel.mention}",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`💭`・Contenu du message:": (
                            f"```" + str(self.sniped['delete'][channel.id]['content']) + "```",
                            False  
                        ),
                        "`🖊️`・Auteur": (
                            f"<@" + str(self.sniped['delete'][channel.id]['author']) + ">",
                            True
                        ),
                        "`🕗`・Heure et date": (
                            f"`" + self.sniped['delete'][channel.id]["time"] + "`",
                            True
                        )
                    }
                )
                await interaction.response.send_message(embed=embed)
            else: 
                embed = embedBuilder(
                    title="`🔭`・Message modifié",
                    description=f"Voici le dernier message modifié dans le salon {channel.mention}",
                    color=embed_color(),
                    footer=footer(),
                    fields={
                        "`💭`・Avant la modification:": (
                            f"```" + str(self.sniped['edit'][channel.id]['before']) + "```",
                            False  
                        ),
                        "`💭`・Après la modification:": (
                            f"```" + str(self.sniped['edit'][channel.id]['after']) + "```",
                            False  
                        ),
                        "`🖊️`・Auteur": (
                            f"<@" + str(self.sniped['edit'][channel.id]['author']) + ">",
                            True
                        ),
                        "`🕗`・Heure et date": (
                            f"`" + self.sniped['edit'][channel.id]["time"] + "`",
                            True
                        )
                    }
                )
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Il n'y as aucun message modifier / supprimé dans ce salon.", ephemeral=True)
            
async def setup(bot):
    await bot.add_cog(snipeDelete(bot))
