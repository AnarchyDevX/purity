# Developed by Celentroft
# Github: https://github.com/Celentroft
# Telegram: https://t.me/scarlxrd_1337

import discord
import asyncio
import signal
import sys
from core._colors import Colors
from discord.ext import commands
from functions.functions import load_json

C = Colors()

class MyBot(commands.Bot):
    def __init__(self) -> None:
        self.C = Colors()
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            help_command=None
        )

    async def setup_hook(self):
        await self.load_extension("events.utils.ready")
    
    async def close(self):
        print(f"\n{C.RED}[SHUTDOWN] {C.WHITE}Shutting down gracefully...")
        await super().close()

def signal_handler(sig, frame):
    print(f"\n{C.YELLOW}[SIGNAL] {C.WHITE}Received interrupt signal, shutting down...")
    try:
        client.loop.create_task(client.close())
    except:
        pass
    sys.exit(0)
        
config = load_json()
client = MyBot()

# Gérer les signaux d'interruption
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    client.run(config['token'])
except KeyboardInterrupt:
    print(f"\n{C.YELLOW}[KEYBOARD] {C.WHITE}Interrupted by user")
except Exception as e:
    print(f"{C.RED}[ERROR] {C.WHITE}{e}")