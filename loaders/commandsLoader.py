import os
from core._colors import Colors
from discord.ext import commands

class commandsLoader:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.bot = bot
        self.C: Colors = Colors()

    async def load_commands(self) -> None:
        for folder in os.listdir('./commands/'):
            folderPath: str = os.path.join('./commands', folder)
            if os.path.isdir(folderPath):  
                for file in os.listdir(folderPath):
                    filePath: str = os.path.join(folderPath, file)
                    if file.endswith('.py'): 
                        try:
                            await self.bot.load_extension(f"commands.{folder}.{file[:-3]}")
                            print(f"{self.C.YELLOW}[COMMAND] {self.C.WHITE}Command loaded: {file}")
                        except Exception as e:
                            print(f"{self.C.RED}[ERROR] Failed to load command {file}: {e}")
                    
                    elif os.path.isdir(filePath): 
                        for subfile in os.listdir(filePath):
                            if subfile.endswith('.py'):
                                try:
                                    await self.bot.load_extension(f"commands.{folder}.{file}.{subfile[:-3]}")
                                    
                                    print(f"{self.C.YELLOW}[COMMAND] {self.C.WHITE}Command loaded: {subfile}")
                                except Exception as e:
                                    print(f"{self.C.RED}[ERROR] Failed to load command {file}: {e}")