import discord
import asyncio
from functions.functions import *
from core.embedBuilder import embedBuilder
from discord.ui import Button

class enableButtonLogs(Button):
    def __init__(self, userId, text, json, bot):
        self.userId = userId
        self.json = json
        self.bot = bot
        super().__init__(
            style=discord.ButtonStyle.green,
            label=text,
            emoji="🟢"
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        from views.logs.disableButton import disableButtonLogs

        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            await interaction.response.send_message("Merci de mentionner le salon que vous voulez configurer.", ephemeral=True)
            message: discord.Message = await self.bot.wait_for("message", check=check, timeout=30.0)
            channel = message.channel_mentions[0] if message.channel_mentions else None

            guildJSON['logs'][self.json]['alive'] = True
            guildJSON['logs'][self.json]['channel'] = channel.id

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
            view = discord.ui.View(timeout=None)
            view.add_item(discord.ui.Button(emoji="⚙️", label="Panel", style=discord.ButtonStyle.gray, disabled=True))
            view.add_item(discord.ui.Button(emoji="📂", label="Logs", style=discord.ButtonStyle.gray, disabled=True))
            view.add_item(enableButtonLogs(self.userId, "Moderation", "modlogs", self.bot) if modsLogs['alive'] == False else disableButtonLogs(self.userId, "Modslogs", "modlogs", self.bot))
            view.add_item(enableButtonLogs(self.userId, "Message", "msglogs", self.bot) if msgLogs['alive'] == False else disableButtonLogs(self.userId, "Modslogs", "msglogs", self.bot))
            view.add_item(enableButtonLogs(self.userId, "Raids", "raidlogs", self.bot) if raidlogs['alive'] == False else disableButtonLogs(self.userId, "Modslogs", "raidlogs", self.bot))
            view.add_item(discord.ui.Button(emoji="⚙️", label="Panel", style=discord.ButtonStyle.gray, disabled=True))
            view.add_item(discord.ui.Button(emoji="📂", label="Logs", style=discord.ButtonStyle.gray, disabled=True))
            view.add_item(enableButtonLogs(self.userId, "Vocal", "voicelogs", self.bot) if voicelogs['alive'] == False else disableButtonLogs(self.userId, "Modslogs", "voicelogs", self.bot))
            view.add_item(enableButtonLogs(self.userId, "Ranks", "ranklogs", self.bot) if ranklogs['alive'] == False else disableButtonLogs(self.userId, "Modslogs", "ranklogs", self.bot))
            view.add_item(enableButtonLogs(self.userId, "Join & Leave", "joinleavelogs", self.bot) if joinleaveLogs['alive'] == False else disableButtonLogs(self.userId, "Modslogs", "joinleavelogs", self.bot))
            await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=view)
            await message.delete()
            
        except asyncio.TimeoutError:
            return await interaction.followup.send("Le delai de réponse est dépasse. Merci de recommencer.", ephemeral=True)