"""Helper function pour mettre à jour l'embed du giveaway"""
import discord

async def update_giveaway_embed(bot, userId, config, interaction=None):
    """Met à jour l'embed de configuration du giveaway"""
    from commands.giveaway.gstart import gstart
    cog = bot.get_cog("gstart")
    if not cog:
        return
    
    embed = cog._create_config_embed(config)
    from views.giveawayView.basicSelect import basicGiveawaySelect
    from views.giveawayView.sendButton import sendGiveawayButton
    
    view = discord.ui.View(timeout=None)
    view.add_item(basicGiveawaySelect(bot, userId, config))
    view.add_item(sendGiveawayButton(bot, userId, config))
    
    # Trouver le message à modifier
    message_to_edit = None
    
    if interaction and hasattr(interaction, 'message') and interaction.message:
        message_to_edit = interaction.message
    elif config.get("_message_id") and config.get("_channel_id"):
        channel = bot.get_channel(config["_channel_id"])
        if channel:
            try:
                message_to_edit = await channel.fetch_message(config["_message_id"])
            except:
                # Si le message n'existe plus, chercher le dernier message du bot
                async for msg in channel.history(limit=50):
                    if msg.author.id == bot.user.id and msg.embeds:
                        message_to_edit = msg
                        config["_message_id"] = msg.id
                        break
    
    if message_to_edit:
        try:
            await message_to_edit.edit(embed=embed, view=view)
        except Exception as e:
            print(f"[GIVEAWAY] Erreur lors de l'édition du message: {e}")

