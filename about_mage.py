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
        title = "__Starter Manual (pg. 4)__", 
        color = nextcord.Color.purple())
    embed_mage.set_author(name=botName,
        icon_url=bot_avatar_url)
    embed_mage.add_field(    
        name="About the Mage", 
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
        value="Weak -12 HP; Normal -18 HP; Strong -22 HP",
        inline=True)
    embed_mage.add_field(
        name="Fireball (Normal)",
        value="Weak -22 HP; Normal -32 HP; Strong -42 HP",
        inline=False)
    embed_mage.add_field(
        name="Arcane Mania (Special)",
        value="Weak -45 HP; Normal -65 HP; Strong -80 HP",
        inline=False)
    embed_mage.add_field(
        name="Biden Blast! (Avalon's Blessing)",
        value="Weak -75 HP; Normal -100 HP; Strong -125 HP",
        inline=False)
    embed_mage.add_field(
        name="Weaknesses/Strengths",
        value="Mage is **STRONG** against the Archer but **WEAK** against the Knight (**NORMAL** against itself).",
        inline=False)
    embed_mage.set_thumbnail(url="https://i.imgur.com/0DpJe0b.png")
    return embed_mage