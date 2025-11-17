import json
import discord
from discord.ext import commands
from functions.functions import *
from core.embedBuilder import embedBuilder
from views.tempVoc.lock import lockTempVoice
from views.tempVoc.unlock import unlockTempVoice
from views.tempVoc.hide import hideTempVoice
from views.tempVoc.unhide import unhideTempVoice
from views.tempVoc.name import nameTempVoice
from views.tempVoc.delete import deleteTempVoice

class createVoice(commands.Cog):
    def __init__(self, bot: commands.Cog) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel != None:
            guildJSON = load_json_file(f'./configs/{member.guild.id}.json')
            for element in guildJSON['configuration']['tempvoices']['configs']:
                if after.channel.id == int(element):
                    category = discord.utils.get(member.guild.categories, id=guildJSON['configuration']['tempvoices']['configs'][element]['category'])
                    if category:
                        try:
                            toMoveChannel = await category.create_voice_channel(name=f"{member.name}")
                        except discord.Forbidden:
                            # Bot n'a pas les permissions
                            return
                        except discord.HTTPException as e:
                            await logs(f"Erreur lors de la création du salon vocal: {e}", 2)
                            return
                        try:
                            embed = embedBuilder(
                                title="`⚙️`・Salon vocal temporaire",
                                description=f"*Te voici dans ton salon vocal temporaire, tu peux le gerer via cet embed.*",
                                color=embed_color(),
                                footer=footer()
                            )
                            view = discord.ui.View(timeout=None)
                            view.add_item(nameTempVoice(member.id, toMoveChannel))
                            view.add_item(lockTempVoice(member.id, toMoveChannel))
                            view.add_item(unlockTempVoice(member.id, toMoveChannel))
                            view.add_item(hideTempVoice(member.id, toMoveChannel))
                            view.add_item(unhideTempVoice(member.id, toMoveChannel))
                            view.add_item(deleteTempVoice(member.id, toMoveChannel))

                            await toMoveChannel.send(embed=embed, view=view, content=member.mention)
                            await member.move_to(toMoveChannel)
                            activeList = guildJSON['configuration']['tempvoices']['active']
                            activeList.append(toMoveChannel.id)
                            with open(f'./configs/{member.guild.id}.json', 'w', encoding='utf-8') as f:
                                json.dump(guildJSON, f, indent=4)
                        except discord.Forbidden:
                            # Permissions insuffisantes
                            pass
                        except discord.HTTPException as e:
                            await logs(f"Erreur lors de la gestion du salon vocal: {e}", 2)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(createVoice(bot))