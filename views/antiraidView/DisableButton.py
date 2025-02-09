import discord
from discord.ui import Button
from functions.functions import *

class AntiraidDisableButton(Button):
    def __init__(self, label, userId, jsonName):
        self.jsonName = jsonName
        self.userId = userId
        super().__init__(
            style=discord.ButtonStyle.grey,
            label=label,
            emoji="🟢"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.userId != interaction.user.id:
            return await unauthorized(interaction)
        
        from views.antiraidView.EnableButton import AntiraidEnableButton

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        
        keys = self.jsonName.split(".") 

        current = guildJSON
        for key in keys[:-1]:
            if key not in current:
                current[key] = {} 
            current = current[key]  

        last_key = keys[-1]
        current[last_key] = False

        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        antiraid = guildJSON["antiraid"]
        embed: embedBuilder = embedBuilder(
            title="`🛡️`・Antiraid",
            color=embed_color(),
            footer=footer(),
            fields={
                "`🛡️`・Antibot": (
                    f'`{lang("antiraid.activer")}`' if antiraid['antibot'] == True else f'`{lang("antiraid.desactiver")}`',
                    True
                ),
                f"`🛡️`・{lang('antiraid.antilien')}": (
                    f'`{lang("antiraid.activer")}`' if antiraid['antilien'] == True else f'`{lang("antiraid.desactiver")}`',
                    True
                ),
                "`🛡️`・Badwords": (
                    f'`{lang("antiraid.activer")}`' if antiraid['badwords'] == True else f'`{lang("antiraid.desactiver")}`',
                    True
                ),
                "`🛡️`・Antichannels": (
                    f"**Créé:** {f'`{lang('antiraid.activer')}`' if antiraid['channels']['create'] == True else f'`{lang('antiraid.desactiver')}`'}\n"
                    f"**Modifié:** {f'`{lang("antiraid.activer")}`' if antiraid['channels']['edit'] == True else f'`{lang('antiraid.desactiver')}`'}\n"
                    f"**Supprimé:** {f'`{lang("antiraid.activer")}`' if antiraid['channels']['delete'] == True else f'`{lang('antiraid.desactiver')}`'}\n",
                    True
                ),
                "`🛡️`・Antirole": (
                    f"**Créé:** {f'`{lang('antiraid.activer')}`' if antiraid['roles']['create'] == True else f'`{lang('antiraid.desactiver')}`'}\n"
                    f"**Modifié:** {f'`{lang('antiraid.activer')}`' if antiraid['roles']['edit'] == True else f'`{lang('antiraid.desactiver')}`'}\n"
                    f"**Supprimé:** {f'`{lang('antiraid.activer')}`' if antiraid['roles']['delete'] == True else f'`{lang('antiraid.desactiver')}`'}\n",
                    True
                ),
                "`🛡️`・Antiranks": (
                    f"**Up:** {f'`{lang("antiraid.activer")}`' if antiraid['rank']['up'] == True else f'`{lang("antiraid.desactiver")}`'}\n"
                    f"**Down:** {f'`{lang("antiraid.activer")}`' if antiraid['rank']['down'] == True else f'`{lang("antiraid.desactiver")}`'}\n",
                    True
                ),
                "`🛡️`・Antiwebhook": (
                    f'`{lang("antiraid.activer")}`' if antiraid['webhook'] == True else f'`{lang("antiraid.desactiver")}`',
                    True
                )
            }
        )
        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.gestion"), style=discord.ButtonStyle.gray, disabled=True))

        for key in ['antibot', 'antilien', 'badwords']:
            view.add_item(
                AntiraidEnableButton(lang(f"antiraid.{key}"), self.userId, f"antiraid.{key}")
                if not antiraid[key] else
                AntiraidDisableButton(lang(f"antiraid.{key}"), self.userId, f"antiraid.{key}")
            )

        return await interaction.response.edit_message(embed=embed, view=view)
