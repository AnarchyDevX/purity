import io
import json
import random
import discord
import re
from typing import Dict, Any
from datetime import datetime
from urllib.parse import urlparse
from core.embedBuilder import embedBuilder
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def load_json() -> Dict[str, Any]:
    with open("config.json", 'r', encoding='utf-8') as f:
        config: Dict[str, Any] = json.load(f)
    return config

def embed_color() -> int:
    config: Dict[str, Any] = load_json()
    color = config['color'].replace('#', '')  # Enlever le # si présent
    return int(color, 16)

def footer() -> str:
    now: str = datetime.now().strftime('%H:%M:%S')
    return f"[{now}] - Purity | Anarchy | 685552160594723015"

def load_json_file(filePath: str) -> Dict[str, Any] | None:
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            file: Dict[str, Any] = json.load(f)
        return file
    except FileNotFoundError:
        # Fichier de config n'existe pas, retourner None
        return None

async def unauthorized(interaction: discord.Interaction) -> None:
    embed: embedBuilder = embedBuilder(
        title="`❌`・Commande non autorisée",
        description="*Vous n'avez pas la permission d'utiliser cette commande.*",
        color=embed_color(),
        footer=footer()
    )
    return await interaction.response.send_message(embed=embed, ephemeral=True)

async def check_perms(interaction: discord.Interaction, number: int) -> bool:
    config: Dict[str, Any] = load_json()
    guildConfig = load_json_file(f"./configs/{interaction.guild.id}.json")
    if guildConfig is None:
        await unauthorized(interaction)
        return False  # Config n'existe pas
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
    with open("./logs/logs.log", "+a", encoding='utf-8') as f:
        if logsTypes == 1:
            f.write(f"[LOGS] - [{now}] - [COMMAND] - [{interaction.user.name}] - [{interaction.user.id}] - {content} ")
        if logsTypes == 2 and interaction == None:
            f.write(f"[LOGS] - [{now}] -  [EVENT]  - [] - [] - {content} ")
        if logsTypes == 3:
            f.write(f"[LOGS] - [{now}] -  [VIEWS]  - [{interaction.user.name}] - [{interaction.user.id}] - {content} ")
        if logsTypes == 4:
            f.write(f"[LOGS] - [{now}] -  [ERROR]  - [{interaction.user.name}] - [{interaction.user.id}] - {content} ")
        f.write("\n")

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
    guildJSON = load_json_file(f"./configs/{guild.id}.json")
    if guildJSON is None:
        return None  # Config n'existe pas
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
        
def format_date(choice: str, toFormat: datetime | None) -> (str | None):
    if toFormat is None:
        return None
    if choice == "hour":
        return toFormat.strftime("%H:%M:%S")
    elif choice == "year":
        return toFormat.strftime("%d/%m/%Y")
    elif choice == "all":
        a: str = toFormat.strftime("%H:%M:%S")
        b: str = toFormat.strftime("%d/%m/%Y")
        return f"{b} à {a}"
    

async def err_embed(interaction: discord.Interaction, title: str, description: str, followup: bool = None, ephemeral: bool = None) -> None:
    embed: embedBuilder = embedBuilder(
        title=f"`❌`・{title}",
        description=f"*{description}*",
        color=embed_color(),
        footer=footer()
    )
    ephemeral = True if ephemeral == None else ephemeral
    if followup == None:
        return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
    elif followup == True:
        return await interaction.followup.send(embed=embed, ephemeral=ephemeral)
    elif followup == False:
        return await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
    


async def check_id_perms(member: discord.Member | discord.User, guild: discord.Guild, number: int) -> bool:
    config: Dict[str, Any] = load_json()
    guildConfig = load_json_file(f"./configs/{guild.id}.json")
    if guildConfig is None: return False  # Config n'existe pas
    memberId: int = member.id
    isOwner: bool = memberId in guildConfig['ownerlist']
    isWhitelist: bool = memberId in guildConfig['whitelist']
    if number == 1:
        if memberId not in config['buyer'] and not isOwner and not isWhitelist:
            return False
        else:
            return True
    elif number == 2:
        if memberId not in config['buyer'] and not isOwner:
            return False
        else:
            return True
    elif number == 3:
        if memberId not in config['buyer']:
            return False
        else:
            return True
        

def lang(element: str) -> str:
    config = load_json()
    with open(f"./lang/{config['lang']}", 'r', encoding="utf-8") as f:
        langfile = json.load(f)
    return langfile[element]


def gen_captcha(code):
    img = Image.new('RGB', (600, 200), color=(255, 255, 255))  
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 50)  
    except IOError:
        font = ImageFont.load_default()  
    x_start = 20
    for char in code:
        angle = random.randint(-30, 30)
        char_font_size = random.randint(40, 70)
        font = ImageFont.truetype("arial.ttf", char_font_size)
        char_img = Image.new('RGBA', (80, 80), color=(255, 255, 255, 0)) 
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((10, 10), char, font=font, fill=(0, 0, 0))
        char_img = char_img.rotate(angle, expand=1)
        img.paste(char_img, (x_start, random.randint(30, 70)), char_img)  
        x_start += char_font_size + random.randint(5, 15)
    for _ in range(5):
        start_point = (random.randint(0, 600), random.randint(0, 200))
        end_point = (random.randint(0, 600), random.randint(0, 200))
        d.line([start_point, end_point], fill=(0, 0, 0), width=2)
    img = img.filter(ImageFilter.GaussianBlur(1))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def is_valid_url(url: str) -> bool:
    """
    Valide une URL en vérifiant le domaine et l'extension de fichier
    Protection contre SSRF et téléchargement de fichiers malveillants
    """
    ALLOWED_DOMAINS = [
        'discord.com', 
        'discordapp.com', 
        'cdn.discordapp.com',
        'media.discordapp.net',
        'i.imgur.com',
        'i.redd.it',
        'images-ext-1.discordapp.net'
    ]
    
    try:
        parsed = urlparse(url)
        
        # Vérifier le schéma
        if parsed.scheme != 'https':
            return False
        
        # Vérifier le domaine
        if parsed.netloc not in ALLOWED_DOMAINS:
            return False
        
        # Vérifier l'extension du fichier
        if not re.match(r'.*\.(jpg|jpeg|png|gif|webp)$', parsed.path, re.IGNORECASE):
            return False
        
        return True
    except (ValueError, AttributeError, TypeError):
        # URL invalide, format incorrect, etc.
        return False