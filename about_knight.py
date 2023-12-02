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
    name="About:", 
    value="The knight is the tankiest class in the game, being close range.", 
    inline=False)
  embed_knight.add_field(    
    name="Stats:", 
    value="150 HP; Low Damage",
    inline=False)
  embed_knight.add_field(    
    name="Attacks:", 
    value="",
    inline=False)
  embed_knight.add_field(
    name="Sword Jab (Weak)",
    value="Weak -5 HP; Normal -10 HP; Strong -15 HP",
    inline=True)
  embed_knight.add_field(
    name="Sword Slash (Normal)",
    value="Weak -10 HP; Normal -20 HP; Strong -30 HP",
    inline=False)
  embed_knight.add_field(
    name="Dual Sword Attack (Special)",
    value="Weak -40 HP; Normal -45 HP; Strong -50 HP",
    inline=False)
  embed_knight.add_field(
    name="Sliced and Diced (Avalon's Blessing)",
    value="Weak -60 HP; Normal -65 HP; Strong -70 HP",
    inline=False)
  embed_knight.add_field(
    name="Weaknesses/Strengths",
    value="Knight is strong against mage but weak against archer.",
    inline=False)
  embed_knight.set_thumbnail(url="https://i.imgur.com/soNMbTL.png")# We also included a little pixel-art in the embed resembling the knight class.
  # We then proceed to defer the need to respond to the interaction and then followup by sending the embed for the knight.
  await interaction.response.defer()
  await interaction.followup.send(embed=embed_knight)