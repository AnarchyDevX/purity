import discord
from discord.ext import commands
from discord import app_commands
from functions.functions import *
import json
import os

class warnAdd(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name="warn", description="Ajouter un warn à un utilisateur")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        check = await check_perms(interaction, 1)
        if check == False:
            return

        await interaction.response.defer()

        config_path = f"./configs/{interaction.guild.id}.json"
        guildJSON = load_json_file(config_path)
        warnConfig = guildJSON['warndb']
        userDb = warnConfig.setdefault('users', {})

        userWarnings = userDb.setdefault(str(member.id), {})
        warnCount = len(userWarnings) + 1

        userWarnings[str(warnCount)] = {
            "reason": reason,
            "date": time_now(True),
            "moderator": interaction.user.id
        }

        if warnCount > warnConfig["maxwarn"]:
            sanction = warnConfig['sanction']
            title = ""

            try:
                if sanction == "ban":
                    await member.ban()
                    title = "banni"
                elif sanction == "kick":
                    await member.kick()
                    title = "expulser"
            except discord.Forbidden:
                return await err_embed(
                    interaction,
                    title="Impossible d'appliquer la sanction",
                    description=f"Je n'ai pas les permissions pour appliquer les sanctions à {member.mention}",
                    followup=True
                )

            del userDb[str(member.id)]
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
            embed = embedBuilder(
                title=f"`🪼`・Membre {title}",
                description=f"*Le membre {member.mention} a été {title} du serveur car il a dépassé `{warnConfig['maxwarn']} warn`.*",
                color=embed_color(),
                footer=footer()
            )
            return await interaction.followup.send(embed=embed)
        else:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(guildJSON, f, indent=4)
            embed = embedBuilder(
                title="`📢`・Warn ajouté",
                description=f"*Le membre {member.mention} a été averti. Il est à `{warnCount}/{warnConfig['maxwarn']} warn`.*",
                color=embed_color(),
                footer=footer()
            )
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(warnAdd(bot))
