import discord
import json
import uuid
from discord.ui import Button, View
from functions.functions import * 
from views.ticketView.ticketSelectButton import ticketSelectButton

class sendButtonTicket(Button):
    def __init__(self, bot, userId, optionsList, channel, category):
        self.channel = channel
        self.category = category
        self.bot = bot
        self.userId = userId
        self.optionsList = optionsList
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="Envoyer",
            emoji="✅"
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userId:
            return await unauthorized(interaction)
        
        # Vérifier qu'il y a au moins une option
        if not self.optionsList or len(self.optionsList) == 0:
            return await err_embed(
                interaction,
                title="Impossible d'envoyer le panel",
                description="Vous devez ajouter au moins une option avant de pouvoir envoyer le panel de ticket.",
                ephemeral=True
            )
        
        embed = interaction.message.embeds[0]
        for i, fields in enumerate(embed.fields):
            if fields.name == "`🔧`・Options configurées":
                embed.remove_field(i)

        select_custom_id = f"ticket_select_{uuid.uuid4().hex}"
        view = discord.ui.View(timeout=None)
        view.add_item(ticketSelectButton(self.bot, self.userId, self.category, self.optionsList, custom_id=select_custom_id))
        message = await self.channel.send(embed=embed, view=view)
        
        # Sauvegarder les informations du panel pour la persistance
        guildJSON = load_json_file(f"./configs/{interaction.guild.id}.json")
        if guildJSON is None:
            return await err_embed(
                interaction,
                title="Erreur",
                description="La configuration du serveur n'a pas été trouvée.",
                ephemeral=True
            )
        
        # Initialiser la structure buttons si elle n'existe pas
        if 'tickets' not in guildJSON:
            guildJSON['tickets'] = {}
        if 'buttons' not in guildJSON['tickets']:
            guildJSON['tickets']['buttons'] = {}
        
        # Sauvegarder les informations du panel
        panel_id = str(message.id)
        guildJSON['tickets']['buttons'][panel_id] = {
            'channel_id': self.channel.id,
            'message_id': message.id,
            'category_id': self.category.id,
            'options_list': self.optionsList,
            'custom_id': select_custom_id
        }
        
        with open(f"./configs/{interaction.guild.id}.json", 'w', encoding='utf-8') as f:
            json.dump(guildJSON, f, indent=4)
        
        # Ajouter la vue au bot pour la persistance
        self.bot.add_view(view, message_id=message.id)
        
        await interaction.response.send_message(f"Le panel de ticket a bien été envoyé dans le salon {self.channel.mention}", ephemeral=True)