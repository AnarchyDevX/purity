import os
from core._colors import Colors
from discord.ext import commands

class eventsLoader:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.C: Colors = Colors()

    async def load_events(self) -> int:
        count = 0
        for folder in os.listdir('./events/'):
            folderPath: str = os.path.join('./events', folder)
            if os.path.isdir(folderPath):  
                for file in os.listdir(folderPath):
                    filePath: str = os.path.join(folderPath, file)
                    if file.endswith('.py'): 
                        try:
                            await self.bot.load_extension(f"events.{folder}.{file[:-3]}")
                            count += 1
                            print(f"{self.C.YELLOW}[EVENT] {self.C.WHITE}Event loaded: {file}")
                        except Exception as e:
                            print(f"{self.C.RED}[ERROR] Failed to load event {file}: {e}")
                    
                    elif os.path.isdir(filePath): 
                        for subfile in os.listdir(filePath):
                            if subfile.endswith('.py'):
                                try:
                                    await self.bot.load_extension(f"events.{folder}.{file}.{subfile[:-3]}")
                                    count += 1
                                    print(f"{self.C.YELLOW}[EVENT] {self.C.WHITE}Event loaded: {subfile}")
                                except Exception as e:
                                    print(f"{self.C.RED}[ERROR] Failed to load event {file}: {e}")
        return count