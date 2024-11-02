import discord
from discord.ui import Button, View
from core.embedBuilder import embedBuilder

class precedentButton(Button):
    def __init__(self, page, pages):
        super().__init__(
            style=discord.ButtonStyle.blurple,
            emoji="⏭️"
        )
        self.page = page 
        self.pages = pages
    

    async def callback(self, interaction: discord.Interaction):
        from .suivantButton import suivantButton
        if self.page > 0:
            self.page -= 1
            embed: embedBuilder = embedBuilder(
                title=interaction.message.embeds[0].title,
                description="\n".join(self.pages[self.page]),
                footer=f"Page: {self.page + 1}/{len(self.pages)}",
                color=interaction.message.embeds[0].color
            )
            view = View(timeout=None)
            view.add_item(precedentButton(self.page, self.pages))
            view.add_item(suivantButton(self.page, self.pages))
            await interaction.response.edit_message(embed=embed, view=view)