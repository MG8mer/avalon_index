# We import the nextcord library, embeds from nextcord.embeds for aesthetic, and interactions for slash comamnd support on discord.

import nextcord
from nextcord.embeds import Embed
import nextcord.interactions  

# The function below creates the about page for the knight class in an embed for the about command, giving a description of the class, its stats, attacks, and who its strong/weak against, with a field for each respectively.

async def about(interaction):
  embed_knight = Embed(   
    title = "About the Knight:", 
    color = nextcord.Color.dark_gray())
  embed_knight.add_field(    
    name="Brief Description:", 
    value="The Knight is the tankiest class in the game, being a close ranger and dealing low damage.", 
    inline=False)
  embed_knight.add_field(    
    name="HP:", 
    value="125",
    inline=False)
  embed_knight.add_field(    
    name="Attacks:", 
    value="",
    inline=False)
  embed_knight.add_field(
    name="Sword Jab (Weak)",
    value="Weak -4 HP; Normal -8 HP; Strong -12 HP",
    inline=True)
  embed_knight.add_field(
    name="Sword Slash (Normal)",
    value="Weak -8 HP; Normal -16 HP; Strong -20 HP",
    inline=False)
  embed_knight.add_field(
    name="Dual Sword Attack (Special)",
    value="Weak -32 HP; Normal -38 HP; Strong -45 HP",
    inline=False)
  embed_knight.add_field(
    name="Sliced and Diced (Avalon's Blessing)",
    value="Weak -55 HP; Normal -60 HP; Strong -65 HP",
    inline=False)
  embed_knight.add_field(
    name="Weaknesses/Strengths",
    value="The Knight is **STRONG** against the Mage but **WEAK** against the Archer (**NORMAL** against itself).",
    inline=False)
  embed_knight.set_thumbnail(url="https://i.imgur.com/soNMbTL.png")# We also included a little pixel-art in the embed resembling the knight class.
  # We then proceed to defer the need to respond to the interaction and then followup by sending the embed for the knight.
  await interaction.response.defer()
  await interaction.followup.send(embed=embed_knight)