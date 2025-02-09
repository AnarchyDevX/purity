import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from discord.ui import Button

class disableButtonLogs(Button):
    def __init__(self, userId, text, json, bot):
        self.userId = userId
        self.json = json
        self.bot = bot
        super().__init__(
            style=discord.ButtonStyle.red,
            label=text,
            emoji="🔴"
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.logs.enableButton import enableButtonLogs
        
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")

        guildJSON['logs'][self.json]['alive'] = False
        json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
        modsLogs = guildJSON['logs']['modlogs']
        msgLogs = guildJSON['logs']['msglogs']
        raidlogs = guildJSON['logs']['raidlogs']
        voicelogs = guildJSON['logs']['voicelogs']
        ranklogs = guildJSON['logs']['ranklogs']
        joinleaveLogs = guildJSON['logs']['joinleavelogs']

        embed: embedBuilder = embedBuilder(
            title="`📂`・Configuration actuelle des logs",
            color=embed_color(),
            footer=footer(),
            fields={
                "`📂`・Modération": (
                    f"<#{modsLogs['channel']}>" if modsLogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Messages": (
                    f"<#{msgLogs['channel']}>" if msgLogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Raids": (
                    f"<#{raidlogs['channel']}>" if raidlogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Vocale": (
                    f"<#{voicelogs['channel']}>" if voicelogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Ranks": (
                    f"<#{ranklogs['channel']}>" if ranklogs['alive'] == True else "`désactivées`",
                    True
                ),
                "`📂`・Joins et Leave": (
                    f"<#{joinleaveLogs['channel']}>" if joinleaveLogs['alive'] == True else "`désactivées`",
                    True
                ),
            }
        )

        def createbutton(params, params2, element, userId, bot):
            return enableButtonLogs(userId, params, params2, bot) if not element else disableButtonLogs(userId, params, params2, bot)

        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(emoji="⚙️", label="Panel", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(emoji="📂", label="Logs", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(createbutton(lang("logs.moderation"), "modlogs", modsLogs['alive'], self.userId, self.bot))
        view.add_item(createbutton(lang("logs.message"), "msglogs", msgLogs['alive'], self.userId, self.bot))
        view.add_item(createbutton(lang("logs.raids"), "raidlogs", raidlogs['alive'], self.userId, self.bot))
        view.add_item(discord.ui.Button(emoji="⚙️", label="Panel", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(discord.ui.Button(emoji="📂", label="Logs", style=discord.ButtonStyle.gray, disabled=True))
        view.add_item(createbutton(lang("logs.voice"), "voicelogs", voicelogs['alive'], self.userId, self.bot))
        view.add_item(createbutton(lang("logs.ranks"), "ranklogs", ranklogs['alive'], self.userId, self.bot))
        view.add_item(createbutton(lang("logs.joinleave"), "joinleavelogs", joinleaveLogs['alive'], self.userId, self.bot))
        await interaction.response.edit_message(embed=embed, view=view)