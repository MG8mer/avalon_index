#.about command related

# We import the nextcord library, embeds from nextcord.embeds for aesthetic, and interactions for slash comamnd support on discord.

import nextcord
from nextcord.embeds import Embed
from nextcord import Interaction
import nextcord.interactions

# The function below creates the about page for the mage class in an embed for the about command, giving a description of the class, its stats, attacks, and who its strong/weak against, with a field for each respectively.

async def about(interaction: Interaction, bot_name, bot_avatar_url):
    botName=bot_name
    bot_avatar_url = bot_avatar_url
    embed_mage = Embed(   
        title = "__Starter Manual (pg. 5)__", 
        color = nextcord.Color.purple())
    embed_mage.set_author(name=botName,
        icon_url=bot_avatar_url)
    embed_mage.add_field(    
        name="__About the Mage__", 
        value="", 
        inline=False)
    embed_mage.add_field(    
        name="About:", 
        value="The Mage deals baseline damage and has decent HP.", 
        inline=False)
    embed_mage.add_field(    
        name="HP:", 
        value="125",
        inline=False)
    embed_mage.add_field(    
        name="Attacks:", 
        value="",
        inline=False)
    embed_mage.add_field(
        name="Zap (Weak)",
        value="-15 HP",
        inline=True)
    embed_mage.add_field(
        name="Fireball (Normal)",
        value="-25 HP",
        inline=False)
    embed_mage.add_field(
        name="Arcane Mania (Special)",
        value="-40 HP",
        inline=False)
    embed_mage.add_field(
        name="Biden Blast! (Avalon's Blessing)",
        value="-70 HP",
        inline=False)
    embed_mage.set_thumbnail(url="https://i.imgur.com/0DpJe0b.png")
    return embed_mage