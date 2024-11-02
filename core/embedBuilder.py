import discord
from typing import Dict, Tuple

class embedBuilder(discord.Embed):
    def __init__(
            self, *,
            fields: Dict[str, Tuple[str, bool]] = None,
            title: str = None, 
            description: str = None, 
            color: int = None, 
            footer: str = None, 
            footerIcon: str = None, 
            author: str = None, 
            authorIcon: str = None,
            imageUrl: str = None,
            thumbnailUrl: str = None
        ) -> None:
        super().__init__(title=title, description=description, color=color)
        if footer:
            self.set_footer(text=footer, icon_url=footerIcon)
        if author:
            self.set_author(name=author, icon_url=authorIcon)
        if imageUrl:
            self.set_image(url=imageUrl)
        if thumbnailUrl:
            self.set_thumbnail(url=thumbnailUrl)
        if fields:
            for name, (value, inline) in fields.items():
                self.add_field(name=name, value=value, inline=inline)
