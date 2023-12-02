#.about command related

# We import the nextcord library, embeds from nextcord.embeds for aesthetic, and interactions for slash comamnd support on discord.

import nextcord
from nextcord.embeds import Embed
import nextcord.interactions

# The function below creates the about page for the mage class in an embed for the about command, giving a description of the class, its stats, attacks, and who its strong/weak against, with a field for each respectively.

async def about(interaction):
    embed_mage = Embed(   
        title = "About the Mage:", 
        color = nextcord.Color.purple())
    embed_mage.add_field(    
        name="About:", 
        value="The mage is a mid ranger but has mediocre hp with mediocre damage.", 
        inline=False)
    embed_mage.add_field(    
        name="Stats:", 
        value="100 HP; Mediocore Damage",
        inline=False)
    embed_mage.add_field(    
        name="Attacks:", 
        value="",
        inline=False)
    embed_mage.add_field(
        name="Zap (Weak)",
        value="Weak -6 HP; Normal -11 HP; Strong -14 HP",
        inline=True)
    embed_mage.add_field(
        name="Fireball (Normal)",
        value="Weak -15 HP; Normal -25 HP; Strong -32 HP",
        inline=False)
    embed_mage.add_field(
        name="Arcane Mania (Special)",
        value="Weak -42 HP; Normal -47 HP; Strong -55 HP",
        inline=False)
    embed_mage.add_field(
        name="Biden Blast! (Avalon's Blessing)",
        value="Weak -70 HP; Normal -75 HP; Strong -80 HP",
        inline=False)
    embed_mage.add_field(
        name="Weaknesses/Strengths",
        value="Mage is strong against archer but weak against knight.",
        inline=False)
    embed_mage.set_thumbnail(url="https://i.imgur.com/0DpJe0b.png")# We also included a little pixel-art in the embed resembling the mage class.
  # We then proceed to defer the need to respond to the interaction and then followup by sending the embed for the mage.
    await interaction.response.defer()
    await interaction.followup.send(embed=embed_mage)