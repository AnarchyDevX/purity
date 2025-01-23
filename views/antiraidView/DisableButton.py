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
        view.add_item(discord.ui.Button(label="Antiraid", emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label="Gestion", style=discord.ButtonStyle.gray, disabled=True))

        view.add_item(AntiraidEnableButton("Antibot", self.userId, "antiraid.antibot") if not antiraid['antibot'] else AntiraidDisableButton("Antibot", self.userId, "antiraid.antibot"))
        view.add_item(AntiraidEnableButton("Antilien", self.userId, "antiraid.antilien") if not antiraid['antilien'] else AntiraidDisableButton("Antilien", self.userId, "antiraid.antilien"))
        view.add_item(AntiraidEnableButton("Badwords", self.userId, "antiraid.badwords") if not antiraid['badwords'] else AntiraidDisableButton("Badwords", self.userId, "antiraid.badwords"))
        

        view.add_item(discord.ui.Button(label="Antiraid", emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label="Channels", style=discord.ButtonStyle.gray, disabled=True))
        
        view.add_item(AntiraidEnableButton("Crée", self.userId, "antiraid.channels.create") if not antiraid['channels']['create'] else AntiraidDisableButton("Crée", self.userId, "antiraid.channels.create"))
        view.add_item(AntiraidEnableButton("Modifié", self.userId, "antiraid.channels.edit") if not antiraid['channels']['edit'] else AntiraidDisableButton("Modifié", self.userId, "antiraid.channels.edit"))
        view.add_item(AntiraidEnableButton("Supprimé", self.userId, "antiraid.channels.delete") if not antiraid['channels']['delete'] else AntiraidDisableButton("Supprimé", self.userId, "antiraid.channels.delete"))
        
        view.add_item(discord.ui.Button(label="Antiraid", emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label="Roles", style=discord.ButtonStyle.gray, disabled=True))
        
        view.add_item(AntiraidEnableButton("Crée", self.userId, "antiraid.roles.create") if not antiraid['roles']['create'] else AntiraidDisableButton("Crée", self.userId, "antiraid.roles.create"))
        view.add_item(AntiraidEnableButton("Modifié", self.userId, "antiraid.roles.edit") if not antiraid['roles']['edit'] else AntiraidDisableButton("Modifié", self.userId, "antiraid.roles.edit"))
        view.add_item(AntiraidEnableButton("Supprimé", self.userId, "antiraid.roles.delete") if not antiraid['roles']['delete'] else AntiraidDisableButton("Supprimé", self.userId, "antiraid.roles.delete"))

        view.add_item(discord.ui.Button(label="Antiraid", emoji="🛡️", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(label="Ranks/Webhook", style=discord.ButtonStyle.gray, disabled=True))

        view.add_item(AntiraidEnableButton("Ajout", self.userId, "antiraid.rank.up") if not antiraid['rank']["up"] else AntiraidDisableButton("Ajout", self.userId, "antiraid.rank.up"))
        view.add_item(AntiraidEnableButton("Retrait", self.userId, "antiraid.rank.down") if not antiraid['rank']["down"] else AntiraidDisableButton("Retrait", self.userId, "antiraid.rank.down"))
        view.add_item(AntiraidEnableButton("Webhook", self.userId, "antiraid.webhook") if not antiraid['webhook'] else AntiraidDisableButton("Webhook", self.userId, "antiraid.webhook"))
        return await interaction.response.edit_message(embed=embed, view=view)