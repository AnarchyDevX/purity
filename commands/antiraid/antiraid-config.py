import discord
from discord import app_commands
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.antiraidView.EnableButton import AntiraidEnableButton
from views.antiraidView.DisableButton import AntiraidDisableButton

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

        def createbutton(params, params2, element, userId):
            return AntiraidEnableButton(params, userId, params2) if not element else AntiraidDisableButton(params, userId, params2)

        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.gestion"), style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(createbutton(lang("antiraid.antibot"), "antiraid.antibot", antiraid['antibot'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.antilien"), "antiraid.antilien", antiraid['antilien'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.badwords"), "antiraid.badwords", antiraid['badwords'], interaction.user.id))
        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.channels"), style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(createbutton(lang("antiraid.create"), "antiraid.channels.create", antiraid['channels']['create'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.edit"), "antiraid.channels.edit", antiraid['channels']['edit'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.delete"), "antiraid.channels.delete", antiraid['channels']['delete'], interaction.user.id))
        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.role"), style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(createbutton(lang("antiraid.create"), "antiraid.roles.create", antiraid['roles']['create'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.edit"), "antiraid.roles.edit", antiraid['roles']['edit'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.delete"), "antiraid.roles.delete", antiraid['roles']['delete'], interaction.user.id))
        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.rankswebhooks"), style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(createbutton(lang("antiraid.add"), "antiraid.rank.up", antiraid['rank']['up'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.remove"), "antiraid.rank.down", antiraid['rank']['down'], interaction.user.id))
        view.add_item(createbutton(lang("antiraid.webhook"), "antiraid.webhook", antiraid['webhook'], interaction.user.id))
                
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(antiraidPanel(bot))