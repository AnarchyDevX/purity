import asyncio
import discord
import json
from discord.ext import commands
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder

class ticketRoleAddButton(Button):
    def __init__(self, userId, bot):
        self.bot: commands.Bot = bot
        self.userId = userId
        super().__init__(
            label="Ajouter",
            style=discord.ButtonStyle.green,
            emoji="➕"
        )

    async def callback(self, interaction: discord.Interaction):
        from views.ticketView.roleAdd import ticketRoleAddButton
        from views.ticketView.roleRemove import ticketRoleRemoveButton

        if interaction.user.id != self.userId:
            return await unauthorized(interaction)

        await interaction.response.send_message(
            "Veuillez mentionner le rôle de support que vous voulez ajouter.", 
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            message = await self.bot.wait_for("message", check=check, timeout=30.0)  
            role = message.role_mentions[0] if message.role_mentions else None

            if role:
                guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
                if guildJSON is None:
                    await err_embed(
                        interaction,
                        title="Configuration manquante",
                        description="La configuration du serveur n'existe pas.",
                        followup=True,
                        ephemeral=True
                    )
                    await asyncio.sleep(1)
                    return await message.delete()
                
                # Initialiser la structure si nécessaire
                if 'tickets' not in guildJSON:
                    guildJSON['tickets'] = {
                        "logs": None,
                        "transcripts": True,
                        "roles": [],
                        "claim": True,
                        "buttons": {},
                        "categories": {
                            "nouveaux": None,
                            "pris_en_charge": None,
                            "en_pause": None,
                            "fermes": None
                        }
                    }
                
                if 'roles' not in guildJSON['tickets']:
                    guildJSON['tickets']['roles'] = []
                
                roleList = guildJSON['tickets']['roles']
                if role.id in roleList:
                    await err_embed(
                        interaction,
                        title="Rôle déjà configuré",
                        description=f"Le rôle que vous avez fourni est déjà configuré comme rôle de support.",
                        followup=True,
                        ephemeral=True
                    )
                    await asyncio.sleep(1)
                    return await message.delete()
                else:
                    roleList.append(role.id)
                    with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
                        json.dump(guildJSON, f, indent=4)
                    rolesList = [f"<@&{roleId}> `{roleId}`" for roleId in guildJSON['tickets']['roles']]
                    embed = embedBuilder(
                        title="`🎫`・Liste des rôles de support",
                        description='\n'.join(rolesList) if rolesList else "*Aucun rôle configuré*",
                        footer=footer(),
                        color=embed_color()
                    )
                    view = discord.ui.View(timeout=None)
                    view.add_item(ticketRoleAddButton(self.userId, self.bot))
                    view.add_item(ticketRoleRemoveButton(self.userId, self.bot))
                    await interaction.followup.edit_message(embed=embed, view=view, message_id=interaction.message.id)
                    await asyncio.sleep(1)
                    return await message.delete()
            else:
                await interaction.followup.send("Je n'ai pas reconnu de rôle dans votre réponse.", ephemeral=True)
                await asyncio.sleep(1)
                return await message.delete()
            
        except asyncio.TimeoutError:
            await interaction.followup.send("Temps écoulé. Veuillez réessayer.", ephemeral=True)

