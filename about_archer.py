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
      value="Weak -15 HP; Normal -20 HP; Strong -25 HP",
      inline=True)
    embed_archer.add_field(
      name="Piercing Shot (Normal)",
      value="Weak -25 HP; Normal -35 HP; Strong -45 HP",
      inline=False)
    embed_archer.add_field(
      name="Triple Shot (Special)",
      value="Weak -50 HP; Normal -70 HP; Strong -90 HP",
      inline=False)
    embed_archer.add_field(
      name="Make it Rain! (Avalon's Blessing)",
      value="Weak -85 HP; Normal -125 HP; Strong -150 HP",
      inline=False)
    embed_archer.add_field(
      name="Weaknesses/Strengths",
      value="Archer is **STRONG** against the Knight but **WEAK** against the Mage (**NORMAL** against itself).",
      inline=False)
    embed_archer.set_thumbnail(
      url="https://i.imgur.com/NcJsHO3.png"
    ) 
    return embed_archer