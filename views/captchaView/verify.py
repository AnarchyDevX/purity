import random
import string
import discord
import asyncio
from discord.ui import Button
from functions.functions import *
from core.embedBuilder import embedBuilder

class startVerify(Button):
    def __init__(self, bot, role) -> None:
        self.role: discord.Role = role
        self.bot = bot
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Verify",
            emoji="🛡️"
        )

    async def callback(self, interaction) -> None:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        image_buf = gen_captcha(code)
        file = discord.File(image_buf, filename='captcha.png')
        embed = embedBuilder(
            description="*Veuillez utiliser le code ci-dessous pour vous verifier en cliquant sur le bouton **se verifier***",
            color=embed_color()
        )
        embed.set_image(url="attachment://captcha.png")
        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            response = await self.bot.wait_for('message', check=check, timeout=60)
            if response.content == code:
                try:
                    await interaction.user.add_roles(self.role)
                    await interaction.followup.send(f"Le rôle {self.role.mention} vous a bien été ajouté.", ephemeral=True)
                except discord.Forbidden:
                    await interaction.followup.send("Je n'ai pas pu vous attribuer le rôle. Contactez un membre du staff", ephemeral=True)
                except discord.HTTPException:
                    await interaction.followup.send("Une erreur est survenue lors de l'attribution du rôle.", ephemeral=True)
            else:
                await interaction.followup.send('Code Incorrect', ephemeral=True)
                try:
                    await interaction.user.kick(reason="Failed Captcha")
                except Exception:
                    pass
            await response.delete()
        except asyncio.TimeoutError:
            await interaction.followup.send('Temps écoulé', ephemeral=True)
            await interaction.user.kick(reason="Timeout Captcha")
