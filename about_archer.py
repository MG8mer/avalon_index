# We import the nextcord library, embeds from nextcord.embeds for aesthetic, and interactions for slash comamnd support on discord.

import nextcord
from nextcord.embeds import Embed
import nextcord.interactions

# The function below creates the about page for the archer class in an embed for the about command, giving a description of the class, its stats, attacks, and who its strong or weak against, with a field for each respectively.

async def about(interaction):
    embed_archer = Embed(   
      title = "About the Archer:", 
      color = nextcord.Color.green())
    embed_archer.add_field(    
      name="Brief Description:", 
      value="The Archer is a long ranger, but has a low HP and deals high damage.", 
      inline=False)
    embed_archer.add_field(    
      name="HP:", 
      value="75",
      inline=False)
    embed_archer.add_field(    
      name="Attacks:", 
      value="",
      inline=False)
    embed_archer.add_field(
      name="Weak Arrow (Weak)",
      value="Weak -7 HP; Normal -12 HP; Strong -15 HP",
      inline=True)
    embed_archer.add_field(
      name="Piercing Shot (Normal)",
      value="Weak -20 HP; Normal -25 HP; Strong -35 HP",
      inline=False)
    embed_archer.add_field(
      name="Triple Shot (Special)",
      value="Weak -45 HP; Normal -50 HP; Strong -60 HP",
      inline=False)
    embed_archer.add_field(
      name="Make it Rain! (Avalon's Blessing)",
      value="Weak -75 HP; Normal -90 HP; Strong -100 HP",
      inline=False)
    embed_archer.add_field(
      name="Weaknesses/Strengths",
      value="Archer is **STRONG** against the Knight but **WEAK** against the Mage (**NORMAL** against itself).",
      inline=False)
    embed_archer.set_thumbnail(
      url="https://i.imgur.com/NcJsHO3.png"
    ) 
    await interaction.response.defer()
    await interaction.followup.send(embed=embed_archer)

# We also included a little pixel-art in the embed resembling the archer class.
# We then proceed to defer the need to respond to the interaction and then followup by sending the embed for the archer.