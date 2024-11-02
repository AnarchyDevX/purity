import discord
from functions.functions import *
from discord import app_commands
from discord.ext import commands
from core.embedBuilder import embedBuilder

class botPresence(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="change-bot-presence", description="Changer la présence du bot")
    @app_commands.choices(
        status=[
            app_commands.Choice(name="En train de jouer a...", value="playing"),
            app_commands.Choice(name="En train d'ecouter...", value="listen"),
            app_commands.Choice(name="En train de stream...", value="streaming"),
            app_commands.Choice(name="En train de regarder...", value="watching")
        ]
    )
    async def change_bot_presence(self, interaction: discord.Interaction, status: str, name: str) -> None:
        await logs('change-bot-presence', 1, interaction)
        check: bool = await check_perms(interaction, 3)
        if check == False:
            return
        
        text: None = None
        if status == "playing":
            await self.bot.change_presence(activity=discord.Game(name=name))
            text: str = f"*Le bot **{self.bot.user.name}** est maintenant en train de jouer à **{name}***"
        elif status == "listen":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))
            text: str = f"*Le bot **{self.bot.user.name}** est maintenant en train d'ecouter **{name}***"
        elif status == "streaming":
            await self.bot.change_presence(activity=discord.Streaming(name=name, url='https://www.twitch.tv/ivyenlive'))
            text: str = f"*Le bot **{self.bot.user.name}** est maintenant en train de stream **{name}***"
        elif status == "watching":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
            text: str = f"*Le bot **{self.bot.user.name}** est maintenant en train de regarder **{name}***"

        embed: embedBuilder = embedBuilder(
            title="`🚀`・Presence du bot",
            description=text,
            color=embed_color(),
            footer=footer()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(botPresence(bot))