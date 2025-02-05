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
                f"`🛡️`・{lang("antiraid.antilien")}": (
                    f'`{lang("antiraid.activer")}`' if antiraid['antilien'] == True else f'`{lang("antiraid.desactiver")}`',
                    True
                ),
                "`🛡️`・Badwords": (
                    f'`{lang("antiraid.activer")}`' if antiraid['badwords'] == True else f'`{lang("antiraid.desactiver")}`',
                    True
                ),
                "`🛡️`・Antichannels": (
                    f"**Créé:** {f'`{lang("antiraid.activer")}`' if antiraid['channels']['create'] == True else f'`{lang("antiraid.desactiver")}`'}\n"
                    f"**Modifié:** {f'`{lang("antiraid.activer")}`' if antiraid['channels']['edit'] == True else f'`{lang("antiraid.desactiver")}`'}\n"
                    f"**Supprimé:** {f'`{lang("antiraid.activer")}`' if antiraid['channels']['delete'] == True else f'`{lang("antiraid.desactiver")}`'}\n",
                    True
                ),
                "`🛡️`・Antirole": (
                    f"**Créé:** {f'`{lang("antiraid.activer")}`' if antiraid['roles']['create'] == True else f'`{lang("antiraid.desactiver")}`'}\n"
                    f"**Modifié:** {f'`{lang("antiraid.activer")}`' if antiraid['roles']['edit'] == True else f'`{lang("antiraid.desactiver")}`'}\n"
                    f"**Supprimé:** {f'`{lang("antiraid.activer")}`' if antiraid['roles']['delete'] == True else f'`{lang("antiraid.desactiver")}`'}\n",
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

        view.add_item(AntiraidEnableButton(lang("antiraid.antibot"), self.userId, "antiraid.antibot") if not antiraid['antibot'] else AntiraidDisableButton(lang("antiraid.antibot"), self.userId, "antiraid.antibot"))
        view.add_item(AntiraidEnableButton(lang("antiraid.antilien"), self.userId, "antiraid.antilien") if not antiraid['antilien'] else AntiraidDisableButton(lang("antiraid.antilien"), self.userId, "antiraid.antilien"))
        view.add_item(AntiraidEnableButton(lang("antiraid.badwords"), self.userId, "antiraid.badwords") if not antiraid['badwords'] else AntiraidDisableButton(lang("antiraid.badwords"), self.userId, "antiraid.badwords"))
        

        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.channels"), style=discord.ButtonStyle.gray, disabled=True))
        
        view.add_item(AntiraidEnableButton(lang("antiraid.create"), self.userId, "antiraid.channels.create") if not antiraid['channels']['create'] else AntiraidDisableButton(lang("antiraid.create"), self.userId, "antiraid.channels.create"))
        view.add_item(AntiraidEnableButton(lang("antiraid.edit"), self.userId, "antiraid.channels.edit") if not antiraid['channels']['edit'] else AntiraidDisableButton(lang("antiraid.edit"), self.userId, "antiraid.channels.edit"))
        view.add_item(AntiraidEnableButton(lang("antiraid.delete"), self.userId, "antiraid.channels.delete") if not antiraid['channels']['delete'] else AntiraidDisableButton(lang("antiraid.delete"), self.userId, "antiraid.channels.delete"))
        
        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.role"), style=discord.ButtonStyle.gray, disabled=True))
        
        view.add_item(AntiraidEnableButton(lang("antiraid.create"), self.userId, "antiraid.roles.create") if not antiraid['roles']['create'] else AntiraidDisableButton(lang("antiraid.create"), self.userId, "antiraid.roles.create"))
        view.add_item(AntiraidEnableButton(lang("antiraid.edit"), self.userId, "antiraid.roles.edit") if not antiraid['roles']['edit'] else AntiraidDisableButton(lang("antiraid.edit"), self.userId, "antiraid.roles.edit"))
        view.add_item(AntiraidEnableButton(lang("antiraid.delete"), self.userId, "antiraid.roles.delete") if not antiraid['roles']['delete'] else AntiraidDisableButton(lang("antiraid.delete"), self.userId, "antiraid.roles.delete"))

        view.add_item(discord.ui.Button(label=lang("antiraid.name"), emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label=lang("antiraid.rankswebhooks"), style=discord.ButtonStyle.gray, disabled=True))

        view.add_item(AntiraidEnableButton(lang("antiraid.add"), self.userId, "antiraid.rank.up") if not antiraid['rank']["up"] else AntiraidDisableButton(lang("antiraid.add"), self.userId, "antiraid.rank.up"))
        view.add_item(AntiraidEnableButton(lang("antiraid.remove"), self.userId, "antiraid.rank.down") if not antiraid['rank']["down"] else AntiraidDisableButton(lang("antiraid.remove"), self.userId, "antiraid.rank.down"))
        view.add_item(AntiraidEnableButton(lang("antiraid.webhook"), self.userId, "antiraid.webhook") if not antiraid['webhook'] else AntiraidDisableButton(lang("antiraid.webhook"), self.userId, "antiraid.webhook"))
        
        return await interaction.response.edit_message(embed=embed, view=view)