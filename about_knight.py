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
    value="-10 HP",
    inline=True)
  embed_knight.add_field(
    name="Sword Slash (Normal)",
    value="-20 HP",
    inline=False)
  embed_knight.add_field(
    name="Dual Sword Attack (Special)",
    value="-35 HP",
    inline=False)
  embed_knight.add_field(
    name="Sliced and Diced (Avalon's Blessing)",
    value="-65 HP",
    inline=False)
  embed_knight.set_thumbnail(url="https://i.imgur.com/soNMbTL.png")
  return embed_knight