import discord
from discord.ui import Select, View
from functions.functions import *
from core.embedBuilder import embedBuilder

class AntiraidSelect(Select):
    def __init__(self, userId, modulesList: list[dict[str, str, str]]):
        self.userId = userId
        options = [
            discord.SelectOption(label=element["name"], value=element['value'], emoji=f"✅" if element["module"] == True else "❌") for element in modulesList
        ]
        super().__init__(
            options=options, min_values=1, max_values=1, placeholder="Selectionner une option."
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        keys = self.values[0].split(".") 

        current = guildJSON
        for key in keys[:-1]:
            if key not in current:
                current[key] = {} 
            current = current[key]  
        last_key = keys[-1]
        current[last_key] = not current[last_key]
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
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

        modulesList = [
            {"module": antiraid['antibot'], 'name': "Antibot", "value": "antiraid.antibot"},
            {"module": antiraid['antilien'], 'name': "Antilien", "value": "antiraid.antilien"},
            {"module": antiraid['badwords'], 'name': "Badwords", "value": "antiraid.badwords"},
            {"module": antiraid['channels']['create'], 'name': "Salon Crée", "value": "antiraid.channels.create"},
            {"module": antiraid['channels']['edit'], 'name': "Salon Modifié", "value": "antiraid.channels.edit"},
            {"module": antiraid['channels']['delete'], 'name': "Salon Supprimé", "value": "antiraid.channels.delete"},
            {"module": antiraid['roles']['create'], 'name': "Roles Crée", "value": "antiraid.roles.create"},
            {"module": antiraid['roles']['edit'], 'name': "Roles Modifié", "value": "antiraid.roles.edit"},
            {"module": antiraid['roles']['delete'], 'name': "Roles Supprimé", "value": "antiraid.roles.delete"},
            {"module": antiraid['rank']['up'], 'name': "Rank Up", "value": "antiraid.rank.up"},
            {"module": antiraid['rank']['down'], 'name': "Rank Down", "value": "antiraid.rank.down"},
            {"module": antiraid['webhook'], 'name': "Webhook", "value": "antiraid.webhook"},
        ]
        

        view = View(timeout=None)
        view.add_item(AntiraidSelect(
            self.userId,
            modulesList
        ))
        await interaction.response.edit_message(embed=embed, view=view)
