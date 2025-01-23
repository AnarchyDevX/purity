import asyncio
import discord
from discord.ext import commands
from discord.ui import Button
from functions.functions import *

class autoroleAddButton(Button):
    def __init__(self, userId, bot):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            label="Ajouter",
            style=discord.ButtonStyle.green,
            emoji="➕"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.autoRole.autoRoleAdd import autoroleAddButton
        from views.autoRole.autoRoleRemove import autoroleRemoveButton

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        await interaction.response.send_message(
            "Veuillez mentionner le rôle que vous voulez configurer.", 
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            message = await self.bot.wait_for("message", check=check, timeout=30.0)  
            role = message.role_mentions[0] if message.role_mentions else None

            if role:
                guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
                roleList = guildJSON['configuration']['autorole']
                if role.id in roleList:
                    await err_embed(
                        interaction,
                        title="Role déjà configuré",
                        description=f"Le role que vous avez fourni est déjà un role ajouté a l'arrivée.",
                        followup=True,
                        ephemeral=True
                    )
                    await asyncio.sleep(1)
                    return await message.delete()
                else:
                    roleList.append(role.id)
                    json.dump(guildJSON, open(f"./configs/{interaction.guild.id}.json", 'w'), indent=4)
                    rolesList: list[str] = [f"<@&{roleId}>`{roleId}`" for roleId in guildJSON['configuration']['autorole']]
                    embed: embedBuilder = embedBuilder(
                        title="`✨`・Liste des roles ajoutés a l'arrivée",
                        description='\n'.join(rolesList),
                        footer=footer(),
                        color=embed_color()
                    )
                    view = discord.ui.View(timeout=None)
                    view.add_item(autoroleAddButton(self.userId, self.bot))
                    view.add_item(autoroleRemoveButton(self.userId, self.bot))
                    await interaction.followup.edit_message(embed=embed, view=view, message_id=interaction.message.id)
                    await asyncio.sleep(1)
                    return await message.delete()
            else:
                await interaction.followup.send("Je n'ai pas reconnu de role dans votre réponse.", ephemeral=True)
                await asyncio.sleep(1)
                return await message.delete()
            
        except asyncio.TimeoutError:
            await interaction.message.delete()


