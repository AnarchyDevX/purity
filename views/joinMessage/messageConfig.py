import discord 
from discord.ext import commands
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder
import asyncio

class MessageConfig(Button):
    def __init__(self, userId, bot):
        self.userId = userId
        self.bot: commands.Bot = bot
        super().__init__(
            style=discord.ButtonStyle.grey,
            label="Message",
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        
        embed = embedBuilder(
            title="`🖊️`・Message d'arrivée",
            description=(
                "```"
                "Mention du membre: {mention}\n"
                "Pseudo du membre: {name}\n"
                "Nombre de membres sur le serveur: {members}\n"
                "Date d'arrivée: {date}\n"
                "```"
            ),
            color=embed_color(),
            footer=footer()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        try:
            message = await self.bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel, timeout=30)
            guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
            guildJSON['greeting']['message'] = message.content
            with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
            await interaction.followup.send("Message d'arrivée configuré avec succès", ephemeral=True)
            await message.delete()

        except asyncio.TimeoutError:
            return await interaction.response.send_message("Vous avez dépasse le delais de réponse", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MessageConfig(bot))
