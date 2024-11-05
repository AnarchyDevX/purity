import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder

class antiraidPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="antiraid-panel", description="Afficher la configuration de l'antiraid")
    async def antiraidPanel(self, interaction: discord.Interaction):
        if not await check_perms(interaction, 2):
            return
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        antiraid = guildJSON["antiraid"]
        embed: embedBuilder = embedBuilder(
            title="`🛡️`・Antiraid",
            color=embed_color(),
            footer=footer(),
            fields={
                "`🛡️`・Antibot": (
                    '`activé`' if antiraid['antibot'] == True else '`désactivé`',
                    True
                ),
                "`🛡️`・Antilien": (
                    '`activé`' if antiraid['antilien'] == True else '`désactivé`',
                    True
                ),
                "`🛡️`・Badwords": (
                    '`activé`' if antiraid['badwords'] == True else '`désactivé`',
                    True
                ),
                "`🛡️`・Antichannels": (
                    f"**Créé:** {'`activé`' if antiraid['channels']['create'] == True else '`désactivé`'}\n"
                    f"**Modifié:** {'`activé`' if antiraid['channels']['edit'] == True else '`désactivé`'}\n"
                    f"**Supprimé:** {'`activé`' if antiraid['channels']['delete'] == True else '`désactivé`'}\n",
                    True
                ),
                "`🛡️`・Antirole": (
                    f"**Créé:** {'`activé`' if antiraid['roles']['create'] == True else '`désactivé`'}\n"
                    f"**Modifié:** {'`activé`' if antiraid['roles']['edit'] == True else '`désactivé`'}\n"
                    f"**Supprimé:** {'`activé`' if antiraid['roles']['delete'] == True else '`désactivé`'}\n",
                    True
                ),
                "`🛡️`・Antiranks": (
                    f"**Up:** {'`activé`' if antiraid['rank']['up'] == True else '`désactivé`'}\n"
                    f"**Down:** {'`activé`' if antiraid['rank']['down'] == True else '`désactivé`'}\n",
                    True
                ),
                "`🛡️`・Antiwebhook": (
                    '`activé`' if antiraid['webhook'] == True else '`désactivé`',
                    True
                )
            }
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(antiraidPanel(bot))
