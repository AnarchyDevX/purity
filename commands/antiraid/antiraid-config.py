import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.antiraidView.AntiraidSelect import AntiraidSelect

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
                    f"`{lang('antiraid.activer')}`" if antiraid['antibot'] else f"`{lang('antiraid.desactiver')}`",
                    True
                ),
                f"`🛡️`・{lang('antiraid.antilien')}": (
                    f"`{lang('antiraid.activer')}`" if antiraid['antilien'] else f"`{lang('antiraid.desactiver')}`",
                    True
                ),
                "`🛡️`・Badwords": (
                    f"`{lang('antiraid.activer')}`" if antiraid['badwords'] else f"`{lang('antiraid.desactiver')}`",
                    True
                ),
                "`🛡️`・Antichannels": (
                    f"**Créé:** `{lang('antiraid.activer') if antiraid['channels']['create'] else lang('antiraid.desactiver')}`\n"
                    f"**Modifié:** `{lang('antiraid.activer') if antiraid['channels']['edit'] else lang('antiraid.desactiver')}`\n"
                    f"**Supprimé:** `{lang('antiraid.activer') if antiraid['channels']['delete'] else lang('antiraid.desactiver')}`",
                    True
                ),
                "`🛡️`・Antirole": (
                    f"**Créé:** `{lang('antiraid.activer') if antiraid['roles']['create'] else lang('antiraid.desactiver')}`\n"
                    f"**Modifié:** `{lang('antiraid.activer') if antiraid['roles']['edit'] else lang('antiraid.desactiver')}`\n"
                    f"**Supprimé:** `{lang('antiraid.activer') if antiraid['roles']['delete'] else lang('antiraid.desactiver')}`",
                    True
                ),
                "`🛡️`・Antiranks": (
                    f"**Up:** `{lang('antiraid.activer') if antiraid['rank']['up'] else lang('antiraid.desactiver')}`\n"
                    f"**Down:** `{lang('antiraid.activer') if antiraid['rank']['down'] else lang('antiraid.desactiver')}`",
                    True
                ),
                "`🛡️`・Antiwebhook": (
                    f"`{lang('antiraid.activer')}`" if antiraid['webhook'] else f"`{lang('antiraid.desactiver')}`",
                    True
                )
            }
        )

        view = discord.ui.View(timeout=None)
        modulesList = [
            {"module": antiraid['antibot'], 'name': "Antibot", "value": "antiraid.antibot"},
            {"module": antiraid['antilien'], 'name': "Antilien", "value": "antiraid.antilien"},
            {"module": antiraid['badwords'], 'name': "Badwords", "value": "antiraid.badwords"},
            {"module": antiraid['channels']['create'], 'name': "Salon Crée", "value": "antiraid.channels.create"},
            {"module": antiraid['channels']['edit'], 'name': "Salon Modifié", "value": "antiraid.channels.edit"},
            {"module": antiraid['channels']['delete'], 'name': "Salon Supprimé", "value": "antiraid.channels.delete"},
            {"module": antiraid['roles']['create'], 'name': "Rôles Crée", "value": "antiraid.roles.create"},
            {"module": antiraid['roles']['edit'], 'name': "Rôles Modifié", "value": "antiraid.roles.edit"},
            {"module": antiraid['roles']['delete'], 'name': "Rôles Supprimé", "value": "antiraid.roles.delete"},
            {"module": antiraid['rank']['up'], 'name': "Rank Up", "value": "antiraid.rank.up"},
            {"module": antiraid['rank']['down'], 'name': "Rank Down", "value": "antiraid.rank.down"},
            {"module": antiraid['webhook'], 'name': "Webhook", "value": "antiraid.webhook"},
        ]
        
        view.add_item(AntiraidSelect(interaction.user.id, modulesList))
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(antiraidPanel(bot))