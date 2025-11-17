import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.greetMessage.greetMessageModal import greetMessageModal

class greetMeassageConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="greet-message-config", description="Configurer le message privé envoyé a l'arrivée aux membres")
    @app_commands.choices(
        alive=[
            app_commands.Choice(name="on", value="on"),
            app_commands.Choice(name="off", value="off")
        ]
    )
    async def greetmessageconfig(self, interaction: discord.Interaction, alive: str):
        if not await check_perms(interaction, 2): return
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        alive = True if alive == "on" else False
        guildJSON['greetmsg']['alive'] = alive
        if alive:
            return await interaction.response.send_modal(greetMessageModal())
        else:
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
            embed = embedBuilder(
                title="`🌍`・Message d'arrivée",
                description=f"*Le message a l'arrivée a été correctement désactivé*",
                color=embed_color(),
                footer=footer()
            )
            return await interaction.response.send_message(embed=embed)  
        
async def setup(bot):
    await bot.add_cog(greetMeassageConfig(bot))