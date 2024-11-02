import json
import discord
from typing import Dict, Any
from datetime import datetime
from core.embedBuilder import embedBuilder

def load_json() -> Dict[str, Any]:
    config: Dict[str, Any] = json.load(open("config.json", 'r'))
    return config

def embed_color() -> int:
    config: Dict[str, Any] = load_json()
    return int(config['color'], 16)

def footer() -> str:
    now: str = datetime.now().strftime('%H:%M:%S')
    return f"[{now}] - slash-mutlti-options Bot"

def load_json_file(filePath: str) -> Dict[str, Any]:
    file: Dict[str, Any] = json.load(open(filePath, 'r'))
    return file

async def unauthorized(interaction: discord.Interaction) -> None:
    embed: embedBuilder = embedBuilder(
        title="`❌`・Commade non autorisée",
        description="*Vous n'avez pas la permission d'utiliser cette commande.*",
        color=embed_color(),
        footer=footer()
    )
    return await interaction.response.send_message(embed=embed, ephemeral=True)

async def check_perms(interaction: discord.Interaction, number: int) -> bool:
    config: Dict[str, Any] = load_json()
    guildConfig: Dict[str, Any] = json.load(open(f"./configs/{interaction.guild.id}.json", 'r'))
    interactionUser: int = interaction.user.id
    isOwner: bool = interactionUser in guildConfig['ownerlist']
    isWhitelist: bool = interactionUser in guildConfig['whitelist']
    if number == 1:
        if interactionUser not in config['buyer'] and not isOwner and not isWhitelist:
            await unauthorized(interaction)
            return False
        else:
            return True
    elif number == 2:
        if interactionUser not in config['buyer'] and not isOwner:
            await unauthorized(interaction)
            return False
        else:
            return True
    elif number == 3:
        if interactionUser not in config['buyer']:
            await unauthorized(interaction)
            return False
        else:
            return True

async def logs(content: str, logsTypes: int, interaction: discord.Interaction = None) -> None:
    now: str = datetime.now().strftime('%H:%M:%S')
    with open("./logs/logs.log", "+a") as f:
        if logsTypes == 1:
            f.write(f"[LOGS] - [{now}] - [COMMAND] - [{interaction.user.name}] - [{interaction.user.id}] - {content} ")
        if logsTypes == 2 and interaction == None:
            f.write(f"[LOGS] - [{now}] -  [EVENT]  - [] - [] - {content} ")
        if logsTypes == 3:
            f.write(f"[LOGS] - [{now}] -  [VIEWS]  - [{interaction.user.name}] - [{interaction.user.id}] - {content} ")
        if logsTypes == 4:
            f.write(f"[LOGS] - [{now}] -  [ERROR]  - [{interaction.user.name}] - [{interaction.user.id}] - {content} ")
        f.write("\n")
        f.close()

def time_now(choice: bool = None) -> str:
    if choice == None:
        now: str = datetime.now().strftime("%H:%M:%S")
        return now
    else:
        if choice == True:
            nowHour = datetime.now().strftime("%H:%M:%S")
            nowYear = datetime.now().strftime("%d:%m:%Y")
            return f"{nowYear} à {nowHour}"

async def check_if_logs(guild: discord.Guild, logsType: str) -> (discord.abc.GuildChannel | None):
    guildJSON: Dict[str, Any] = json.load(open(f"./configs/{guild.id}.json", 'r'))
    logsConfig: Any = guildJSON['logs'][logsType]
    if logsConfig['alive'] == True:
        if logsConfig['channel'] != None:
            logsChannel: discord.abc.GuildChannel | None = discord.utils.get(guild.channels, id=logsConfig['channel'])
            if logsChannel != None:
                return logsChannel
            else:
                return None
        else:
            return None
    else:
        return None
        
def format_date(choice: str, toFormat: datetime) -> (str | None):
    if choice == "hour":
        return toFormat.strftime("%H:%M:%S")
    elif choice == "year":
        return toFormat.strftime("%d/%m/%Y")
    elif choice == "all":
        a: str = toFormat.strftime("%H:%M:%S")
        b: str = toFormat.strftime("%d/%m/%Y")
        return f"{b} à {a}"
    

async def err_embed(interaction: discord.Interaction, title: str, description: str, followup: bool = None) -> None:
    embed: embedBuilder = embedBuilder(
        title=f"`❌`・{title}",
        description=f"*{description}*",
        color=embed_color(),
        footer=footer()
    )
    if followup == None:
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif followup == True:
        return await interaction.followup.send(embed=embed, ephemeral=True)
    elif followup == False:
        return await interaction.response.send_message(embed=embed, ephemeral=True)