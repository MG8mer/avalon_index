# We import the nextcord library, embeds from nextcord.embeds for aesthetic, and interactions for slash comamnd support on discord.

import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
from nextcord import Interaction

# The function below creates the about page for the archer class in an embed for the about command, giving a description of the class, its stats, attacks, and who its strong or weak against, with a field for each respectively.

async def about(interaction: Interaction, bot_name, bot_avatar_url):
    botName=bot_name
    bot_avatar_url = bot_avatar_url
    embed_archer = Embed(   
      title = "__Starter Manual (pg. 4)__", 
      color = nextcord.Color.green())
    embed_archer.set_author(name=botName,
      icon_url=bot_avatar_url)
    embed_archer.add_field(    
      name="__About the Archer__", 
      value="", 
      inline=False)
    embed_archer.add_field(    
      name="Brief Description:", 
      value="The Archer has low HP and deals high damage.", 
      inline=False)
    embed_archer.add_field(    
      name="HP:", 
      value="100",
      inline=False)
    embed_archer.add_field(    
      name="Attacks:", 
      value="",
      inline=False)
    embed_archer.add_field(
      name="Weak Arrow (Weak)",
      value="-20 HP",
      inline=True)
    embed_archer.add_field(
      name="Piercing Shot (Normal)",
      value="-30 HP",
      inline=False)
    embed_archer.add_field(
      name="Triple Shot (Special)",
      value="-45 HP",
      inline=False)
    embed_archer.add_field(
      name="Make it Rain! (Avalon's Blessing)",
      value="-75 HP",
      inline=False)
    embed_archer.set_thumbnail(
      url="https://i.imgur.com/NcJsHO3.png"
    ) 
    return embed_archer