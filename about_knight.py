# We import the nextcord library, embeds from nextcord.embeds for aesthetic, and interactions for slash comamnd support on discord.

import nextcord
from nextcord.embeds import Embed
from nextcord import Interaction
import nextcord.interactions  

# The function below creates the about page for the knight class in an embed for the about command, giving a description of the class, its stats, attacks, and who its strong/weak against, with a field for each respectively.

async def about(interaction: Interaction, bot_name, bot_avatar_url):
  botName=bot_name
  bot_avatar_url = bot_avatar_url
  embed_knight = Embed(   
    title = "__Starter Manual (pg. 3)__", 
    color = nextcord.Color.dark_gray())
  embed_knight.set_author(name=botName,
    icon_url=bot_avatar_url)
  embed_knight.add_field(    
    name="__About the Knight__", 
    value="", 
    inline=False)
  embed_knight.add_field(    
    name="Brief Description:", 
    value="The Knight is the tankiest class in the game, but deals low damage.", 
    inline=False)
  embed_knight.add_field(    
    name="HP:", 
    value="150",
    inline=False)
  embed_knight.add_field(    
    name="Attacks:", 
    value="",
    inline=False)
  embed_knight.add_field(
    name="Sword Jab (Weak)",
    value="Weak -10 HP; Normal -15 HP; Strong -20 HP",
    inline=True)
  embed_knight.add_field(
    name="Sword Slash (Normal)",
    value="Weak -15 HP; Normal -25 HP; Strong -35 HP",
    inline=False)
  embed_knight.add_field(
    name="Dual Sword Attack (Special)",
    value="Weak -30 HP; Normal -45 HP; Strong -60 HP",
    inline=False)
  embed_knight.add_field(
    name="Sliced and Diced (Avalon's Blessing)",
    value="Weak -50 HP; Normal -75 HP; Strong -100 HP",
    inline=False)
  embed_knight.add_field(
    name="Weaknesses/Strengths",
    value="The Knight is **STRONG** against the Mage but **WEAK** against the Archer (**NORMAL** against itself).",
    inline=False)
  embed_knight.set_thumbnail(url="https://i.imgur.com/soNMbTL.png")
  return embed_knight