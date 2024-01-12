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



# Function to send an embed to the user when they use battle if they picked knight.
async def battle_embd(interaction: Interaction, member: nextcord.Member, switch, turn):
  class ChooseFour(nextcord.ui.View):
    def __init__(self):
      super().__init__()
      self.value = None

    @nextcord.ui.button(label = 'Sword Jab', style=nextcord.ButtonStyle.blurple)
    async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
      move = 'Sword Jab'
      async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
          if switch == False:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (interaction.user.id, member.id, move, turn,))
          elif switch == True:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, interaction.user.id, move, turn,))
        await db.commit()
      self.value = True
      self.stop()

    @nextcord.ui.button(label = 'Sword Slash', style=nextcord.ButtonStyle.blurple)
    async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
      move = 'Sword Slash'
      async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
          if switch == False:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (interaction.user.id, member.id, move, turn,))
          elif switch == True:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, interaction.user.id, move, turn,))
        await db.commit()
      self.value = True
      self.stop()

    @nextcord.ui.button(label = 'Dual Sword Attack', style=nextcord.ButtonStyle.blurple)
    async def special(self, button: nextcord.ui.Button, interaction: Interaction):
      move = 'Dual Sword Attack'
      async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
          if switch == False:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (interaction.user.id, member.id, move, turn,))
          elif switch == True:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, interaction.user.id, move, turn,))
        await db.commit()
      self.value = True
      self.stop()

    @nextcord.ui.button(label = 'Sliced and Diced', style=nextcord.ButtonStyle.blurple)
    async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
      move = 'Sliced and Diced'
      async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
          if switch == False:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (interaction.user.id, member.id, move, turn,))
          elif switch == True:
            await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, interaction.user.id, move, turn,))
        await db.commit()
      self.value = True
      self.stop()
  view = ChooseFour()
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
     description = "",
    color = nextcord.Color.dark_gray())
  embed.add_field( # Field that shows hp.   
    name="HP:", 
    value=str(hp[0]),
    inline=True)
  embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
    name="Sword Jab(Weak)",
    value=str(attacks[1]["Sword Jab"][evaluation[0]]),
    inline=True)
  embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
    name="Sword Slash (Normal)",
    value=str(attacks[1]["Sword Slash"][evaluation[0]]),
    inline=False)
  embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
    name="Dual Sword Attack (Special)",
    value=str(attacks[1]["Dual Sword Attack"][evaluation[0]]),
    inline=False)
  embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
    name="Sliced and Diced (Avalon's Blessing)",
    value=str(attacks[1]["Sliced and Diced"][evaluation[0]]),
    inline=False)            
  embed.set_thumbnail(url="https://i.imgur.com/soNMbTL.png")  # Shows image of knight.
  if switch == False: # If it's the starter's turn, send the embed in their dm.
    await interaction.user.send(embed=embed, view=view)
    await view.wait()
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {interaction.user.id}")
        move = await cursor.fetchone()
      await db.commit()
    return move
  elif switch == True: # If it's the reciever's turn, send the embed in their dm.
    await member.send(embed=embed, view=view)
    await view.wait()
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {member.id}")
        move = await cursor.fetchone()
      await db.commit()
    return move
  if view.value is None:
    return