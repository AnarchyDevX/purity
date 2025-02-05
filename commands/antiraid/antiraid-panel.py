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
        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.gestion"), style=discord.ButtonStyle.gray, disabled=True))

        view.add_item(AntiraidEnableButton(lang("antiraid.antibot"), interaction.user.id, "antiraid.antibot") if not antiraid['antibot'] else AntiraidDisableButton(lang("antiraid.antibot"), interaction.user.id, "antiraid.antibot"))
        view.add_item(AntiraidEnableButton(lang("antiraid.antilien"), interaction.user.id, "antiraid.antilien") if not antiraid['antilien'] else AntiraidDisableButton(lang("antiraid.antilien"), interaction.user.id, "antiraid.antilien"))
        view.add_item(AntiraidEnableButton(lang("antiraid.badwords"), interaction.user.id, "antiraid.badwords") if not antiraid['badwords'] else AntiraidDisableButton(lang("antiraid.badwords"), interaction.user.id, "antiraid.badwords"))


        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.channels"), style=discord.ButtonStyle.gray, disabled=True))

        view.add_item(AntiraidEnableButton(lang("antiraid.create"), interaction.user.id, "antiraid.channels.create") if not antiraid['channels']['create'] else AntiraidDisableButton(lang("antiraid.create"), interaction.user.id, "antiraid.channels.create"))
        view.add_item(AntiraidEnableButton(lang("antiraid.edit"), interaction.user.id, "antiraid.channels.edit") if not antiraid['channels']['edit'] else AntiraidDisableButton(lang("antiraid.edit"), interaction.user.id, "antiraid.channels.edit"))
        view.add_item(AntiraidEnableButton(lang("antiraid.delete"), interaction.user.id, "antiraid.channels.delete") if not antiraid['channels']['delete'] else AntiraidDisableButton(lang("antiraid.delete"), interaction.user.id, "antiraid.channels.delete"))

        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.role"), style=discord.ButtonStyle.gray, disabled=True))

        view.add_item(AntiraidEnableButton(lang("antiraid.create"), interaction.user.id, "antiraid.roles.create") if not antiraid['roles']['create'] else AntiraidDisableButton(lang("antiraid.create"), interaction.user.id, "antiraid.roles.create"))
        view.add_item(AntiraidEnableButton(lang("antiraid.edit"), interaction.user.id, "antiraid.roles.edit") if not antiraid['roles']['edit'] else AntiraidDisableButton(lang("antiraid.edit"), interaction.user.id, "antiraid.roles.edit"))
        view.add_item(AntiraidEnableButton(lang("antiraid.delete"), interaction.user.id, "antiraid.roles.delete") if not antiraid['roles']['delete'] else AntiraidDisableButton(lang("antiraid.delete"), interaction.user.id, "antiraid.roles.delete"))

        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.rankswebhooks"), style=discord.ButtonStyle.gray, disabled=True))

        view.add_item(AntiraidEnableButton(lang("antiraid.add"), interaction.user.id, "antiraid.rank.up") if not antiraid['rank']["up"] else AntiraidDisableButton(lang("antiraid.add"), interaction.user.id, "antiraid.rank.up"))
        view.add_item(AntiraidEnableButton(lang("antiraid.remove"), interaction.user.id, "antiraid.rank.down") if not antiraid['rank']["down"] else AntiraidDisableButton(lang("antiraid.remove"), interaction.user.id, "antiraid.rank.down"))
        view.add_item(AntiraidEnableButton(lang("antiraid.webhook"), interaction.user.id, "antiraid.webhook") if not antiraid['webhook'] else AntiraidDisableButton(lang("antiraid.webhook"), interaction.user.id, "antiraid.webhook"))
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(antiraidPanel(bot))