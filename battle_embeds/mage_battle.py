import nextcord
from nextcord.embeds import Embed
import nextcord.interactions  
import aiosqlite
from nextcord import Interaction

# Useful source throughout: https://discordpy.readthedocs.io/en/stable/interactions/api.html

# Dicts to store class info:

# Class health
health = {
  1: 150,
  2: 75,
  3: 100
}


# Battle evaluation:
  # Ex: 12; if a knight fights an archer it's weak for the knight.
  # Ex 2: 32: if a mage fights an archer, it's strong for the mage.
evaluation = {
  "11": "Normal",
  "22": "Normal",
  "33": "Normal",
  "12": "Weak",
  "13": "Strong",
  "21": "Strong",
  "23": "Weak",
  "31": "Weak",
  "32": "Strong",
}

# Dict order:
# Class
  # Attacks:
    # Damage dependent on evaluation.

attacks = {
  1: {
    "Sword Jab": {
      "Weak": -5,
      "Normal": -10,
      "Strong": -15
    },
    "Sword Slash": {
      "Weak": -10,
      "Normal": -20,
      "Strong": -30
    },
    "Dual Sword Attack": {
      "Weak": -40,
      "Nomral": -45,
      "Strong": -50,
    },
    "Sliced and Diced": {
      "Weak": -60,
      "Normal": -65,
      "Strong": -70,
    }
  },
  2: {
    "Weak Arrow": {
      "Weak": -7,
      "Normal": -12,
      "Strong": -15
    },
    "Piercing Shot": {
      "Weak": -20,
      "Normal": -25,
      "Strong": -35
    },
    "Triple Shot": {
      "Weak": -45,
      "Nomral": -50,
      "Strong": -60,
    },
    "Make it Rain": {
      "Weak": -80,
      "Normal": -90,
      "Strong": -100,
    }
  },
  3: {
  "Zap": {
    "Weak": -6,
    "Normal": -11,
    "Strong": -14
  },
  "Fireball": {
    "Weak": -15,
    "Normal": -25,
    "Strong": -32
  },
  "Arcane Mania": {
    "Weak": -42,
    "Nomral": -47,
    "Strong": -55,
  },
  "Biden Blast": {
    "Weak": -70,
    "Normal": -75,
    "Strong": -80,
  }
}

}

# Function to send an embed to the user when they use battle if they picked mage.
async def battle_embd(interaction: Interaction, member: nextcord.Member, switch):
  hp = None # Define hp
  evaluation = None # Define evaluation
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      if switch == False: # If it's the starter's turn
        await cursor.execute(f"SELECT starter_hp FROM battles WHERE starter_id = {interaction.user.id}")
        hp = await cursor.fetchone() # Get hp value of that user 
        await cursor.execute(f"SELECT evaluation_starter FROM battles WHERE starter_id = {interaction.user.id}")
        evaluation = await cursor.fetchone() # Get the evaluation of that user
      elif switch == True: # If it's the reciever's turn
        await cursor.execute(f"SELECT reciever_hp FROM battles WHERE starter_id = {interaction.user.id}")
        hp = await cursor.fetchone() # Get hp value of that user 
        await cursor.execute(f"SELECT evaluation_reciever FROM battles WHERE starter_id = {interaction.user.id}")
        evaluation = await cursor.fetchone() # Get the evaluation of that user
    await db.commit()
  embed = Embed( # Title and description, indicating user to pick a move.
    title = "Moves",
    description = "Pick from the avaliable moves!",
    color = nextcord.Color.purple())
  embed.add_field( # Field that shows hp. 
    name="HP:", 
    value=str(hp[0]),
    inline=True)
  embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
    name="Zap (Weak)",
    value=str(attacks[3]["Zap"][evaluation[0]]),
    inline=True)
  embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
    name="Fireball (Normal)",
    value=str(attacks[3]["Fireball"][evaluation[0]]),
    inline=False)
  embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
    name="Arcane Mania (Special)",
    value=str(attacks[3]["Arcane Mania"][evaluation[0]]),
    inline=False)
  embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
    name="Biden Blast (Avalon's Blessing)",
    value=str(attacks[3]["Biden Blast"][evaluation[0]]),
    inline=False)
  embed.set_thumbnail(url="https://i.imgur.com/0DpJe0b.png")  # Shows image of mage.
  if switch == False: # If it's the starter's turn, send the embed in their dm.
    await interaction.user.send(embed=embed)
  elif switch == True: # If it's the reciever's turn, send the embed in their dm.
    await member.send(embed=embed)