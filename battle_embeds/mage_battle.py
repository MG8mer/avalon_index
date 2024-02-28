import nextcord
from nextcord.embeds import Embed
import nextcord.interactions  
import aiosqlite
from nextcord import Interaction

# Useful source throughout: https://discordpy.readthedocs.io/en/stable/interactions/api.html

# Function to send an embed to the user when they use battle if they picked mage.
async def battle_embd(interaction: Interaction, member: nextcord.Member, switch, turn, starter_hp_value, reciever_hp_value, startrand_mage, recieverand_mage):
  if startrand_mage == 7 or recieverand_mage == 7:
        # Dicts to store class info:
    
        # Class health
        health = {
          1: 125,
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
              "Weak": -4,
              "Normal": -8,
              "Strong": -12
            },
            "Sword Slash": {
              "Weak": -8,
              "Normal": -16,
              "Strong": -20
            },
            "Dual Sword Attack": {
              "Weak": -32,
              "Normal": -38,
              "Strong": -50
            },
            "Sliced and Diced": {
              "Weak": -55,
              "Normal": -60,
              "Strong": -65
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
              "Normal": -50,
              "Strong": -60
            },
            "Make it Rain": {
              "Weak": -75,
              "Normal": -90,
              "Strong": -100
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
            "Strong": -30
          },
          "Arcane Mania": {
            "Weak": -42,
            "Normal": -47,
            "Strong": -55
          },
          "Biden Blast": {
            "Weak": -70,
            "Normal": -75,
            "Strong": -80
          }
        },
        4: {
        "THUNDERBOLT": {
          "Weak": -9,
          "Normal": -17,
          "Strong": -21
        },
        "SUPER FIREBALL": {
          "Weak": -23,
          "Normal": -38,
          "Strong": -45
        },
        "THE SORCERER'S WRATH": {
          "Weak": -63,
          "Normal": -71,
          "Strong": -83,
        },
        "TRUE BIDEN BLAST!!!": {
          "Weak": -999,
          "Normal": -999,
          "Strong": -999,
        }
      }
    }
  else:
      # Dicts to store class info:

      # Class health
      health = {
        1: 125,
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
            "Weak": -4,
            "Normal": -8,
            "Strong": -12
          },
          "Sword Slash": {
            "Weak": -8,
            "Normal": -16,
            "Strong": -20
          },
          "Dual Sword Attack": {
            "Weak": -32,
            "Normal": -38,
            "Strong": -50
          },
          "Sliced and Diced": {
            "Weak": -55,
            "Normal": -60,
            "Strong": -65
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
            "Normal": -50,
            "Strong": -60
          },
          "Make it Rain": {
            "Weak": -75,
            "Normal": -90,
            "Strong": -100
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
          "Strong": -30
        },
        "Arcane Mania": {
          "Weak": -42,
          "Normal": -47,
          "Strong": -55
        },
        "Biden Blast": {
          "Weak": -70,
          "Normal": -75,
          "Strong": -80
        }
      }
     }
  id_user = interaction.user.id
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      if switch == False:
        await cursor.execute('SELECT n_cooldown FROM cooldowns WHERE user_id = ?', (interaction.user.id,))
        normal_c = await cursor.fetchone()
        await cursor.execute('SELECT s_cooldown FROM cooldowns WHERE user_id = ?', (interaction.user.id,))
        special_c = await cursor.fetchone()
        await cursor.execute('SELECT ab_cooldown FROM cooldowns WHERE user_id = ?', (interaction.user.id,))
        avalonbless_c = await cursor.fetchone()
      elif switch == True:
        await cursor.execute('SELECT n_cooldown FROM cooldowns WHERE user_id = ?', (member.id,))
        normal_c = await cursor.fetchone()
        await cursor.execute('SELECT s_cooldown FROM cooldowns WHERE user_id = ?', (member.id,))
        special_c = await cursor.fetchone()
        await cursor.execute('SELECT ab_cooldown FROM cooldowns WHERE user_id = ?', (member.id,))
        avalonbless_c = await cursor.fetchone()
    await db.commit()

  if switch == False:
    if startrand_mage == 7:
      class ChooseFour(nextcord.ui.View):
        def __init__(self):
          super().__init__()
          self.value = None
  
        @nextcord.ui.button(label = "THUNDERBOLT", style=nextcord.ButtonStyle.blurple)
        async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
          move = "THUNDERBOLT"
          async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
              if switch == False:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
              elif switch == True:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
            await db.commit()
          self.value = True
          self.stop()
  
        if normal_c[0] == 0:
          @nextcord.ui.button(label = "SUPER FIREBALL", style=nextcord.ButtonStyle.blurple)
          async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "SUPER FIREBALL"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()
      
  
        if special_c[0] == 0:
          @nextcord.ui.button(label = "THE SORCERER'S WRATH", style=nextcord.ButtonStyle.blurple)
          async def special(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "THE SORCERER'S WRATH"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()
  
        if avalonbless_c[0] == 0:
          @nextcord.ui.button(label = "TRUE BIDEN BLAST!!!", style=nextcord.ButtonStyle.blurple)
          async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "TRUE BIDEN BLAST!!!"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()
    else:
      class ChooseFour(nextcord.ui.View):
        def __init__(self):
          super().__init__()
          self.value = None

        @nextcord.ui.button(label = "Zap", style=nextcord.ButtonStyle.blurple)
        async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
          move = "Zap"
          async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
              if switch == False:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
              elif switch == True:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
            await db.commit()
          self.value = True
          self.stop()

        if normal_c[0] == 0:
          @nextcord.ui.button(label = "Fireball", style=nextcord.ButtonStyle.blurple)
          async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "Fireball"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()

        if special_c[0] == 0:
          @nextcord.ui.button(label = "Arcane Mania", style=nextcord.ButtonStyle.blurple)
          async def special(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "Arcane Mania"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()

        if avalonbless_c[0] == 0:
          @nextcord.ui.button(label = "Biden Blast", style=nextcord.ButtonStyle.blurple)
          async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "Biden Blast"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()
  elif switch == True:
    if recieverand_mage == 7:
      class ChooseFour(nextcord.ui.View):
        def __init__(self):
          super().__init__()
          self.value = None

        @nextcord.ui.button(label = "THUNDERBOLT", style=nextcord.ButtonStyle.blurple)
        async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
          move = "THUNDERBOLT"
          async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
              if switch == False:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
              elif switch == True:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
            await db.commit()
          self.value = True
          self.stop()
        
        if normal_c[0] == 0:
          @nextcord.ui.button(label = "SUPER FIREBALL", style=nextcord.ButtonStyle.blurple)
          async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "SUPER FIREBALL"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()


        if special_c[0] == 0:
          @nextcord.ui.button(label = "THE SORCERER'S WRATH", style=nextcord.ButtonStyle.blurple)
          async def special(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "THE SORCERER'S WRATH"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()

        if avalonbless_c[0] == 0:
          @nextcord.ui.button(label = "TRUE BIDEN BLAST!!!", style=nextcord.ButtonStyle.blurple)
          async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "TRUE BIDEN BLAST!!!"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()
    else:
      class ChooseFour(nextcord.ui.View):
        def __init__(self):
          super().__init__()
          self.value = None

        @nextcord.ui.button(label = "Zap", style=nextcord.ButtonStyle.blurple)
        async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
          move = "Zap"
          async with aiosqlite.connect("main.db") as db:
            async with db.cursor() as cursor:
              if switch == False:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
              elif switch == True:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
            await db.commit()
          self.value = True
          self.stop()

        if normal_c[0] == 0:
          @nextcord.ui.button(label = "Fireball", style=nextcord.ButtonStyle.blurple)
          async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "Fireball"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()

        if special_c[0] == 0:
          @nextcord.ui.button(label = "Arcane Mania", style=nextcord.ButtonStyle.blurple)
          async def special(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "Arcane Mania"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()

        if avalonbless_c[0] == 0:
          @nextcord.ui.button(label = "Biden Blast", style=nextcord.ButtonStyle.blurple)
          async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
            move = "Biden Blast"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
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

  if switch == False:
    if startrand_mage == 7:
      embed = Embed( # Title and description, indicating user to pick a move.
        title = "Moves",
        description = "",
        color = nextcord.Color.purple())
      embed.add_field( # Field that shows hp. 
        name="HP:", 
        value=str(hp[0]),
        inline=True)
      embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
        name="THUNDERBOLT (Weak) **No Cooldown**",
        value=str(attacks[4]["THUNDERBOLT"][evaluation[0]]),
        inline=True)
      embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
        name=f"SUPER FIREBALL (Normal) **Cooldown: {normal_c[0]}**",
        value=str(attacks[4]["SUPER FIREBALL"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
        name=f"THE SORCERER'S WRATH (Special) **Cooldown: {special_c[0]}**",
        value=str(attacks[4]["THE SORCERER'S WRATH"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
        name=f"TRUE BIDEN BLAST!!! (Avalon's Blessing) **Cooldown: {avalonbless_c[0]}**",
        value=str(attacks[4]["TRUE BIDEN BLAST!!!"][evaluation[0]]),
        inline=False)        
      embed.set_thumbnail(url="https://i.imgur.com/aIikkUR.png")
    else:
      embed = Embed( # Title and description, indicating user to pick a move.
        title = "Moves",
        description = "",
        color = nextcord.Color.purple())
      embed.add_field( # Field that shows hp. 
        name="HP:", 
        value=str(hp[0]),
        inline=True)
      embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
        name="Zap (Weak) **No Cooldown**",
        value=str(attacks[3]["Zap"][evaluation[0]]),
        inline=True)
      embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
        name=f"Fireball (Normal) **Cooldown: {normal_c[0]}**",
        value=str(attacks[3]["Fireball"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
        name=f"Arcane Mania (Special) **Cooldown: {special_c[0]}**",
        value=str(attacks[3]["Arcane Mania"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
        name=f"Biden Blast (Avalon's Blessing) **Cooldown: {avalonbless_c[0]}**",
        value=str(attacks[3]["Biden Blast"][evaluation[0]]),
        inline=False)
      embed.set_thumbnail(url="https://i.imgur.com/0DpJe0b.png")  # Shows image of mage.
  elif switch == True:
    if recieverand_mage == 7:
      embed = Embed( # Title and description, indicating user to pick a move.
        title = "Moves",
        description = "",
        color = nextcord.Color.purple())
      embed.add_field( # Field that shows hp. 
        name="HP:", 
        value=str(hp[0]),
        inline=True)
      embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
        name="THUNDERBOLT (Weak) **No Cooldown**",
        value=str(attacks[4]["THUNDERBOLT"][evaluation[0]]),
        inline=True)
      embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
        name=f"SUPER FIREBALL (Normal) **Cooldown: {normal_c[0]}**",
        value=str(attacks[4]["SUPER FIREBALL"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
        name=f"THE SORCERER'S WRATH (Special) **Cooldown: {special_c[0]}**",
        value=str(attacks[4]["THE SORCERER'S WRATH"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
        name=f"TRUE BIDEN BLAST!!! (Avalon's Blessing) **Cooldown: {avalonbless_c[0]}**",
        value=str(attacks[4]["TRUE BIDEN BLAST!!!"][evaluation[0]]),
        inline=False)        
      embed.set_thumbnail(url="https://i.imgur.com/aIikkUR.png")
    else:
      embed = Embed( # Title and description, indicating user to pick a move.
        title = "Moves",
        description = "",
        color = nextcord.Color.purple())
      embed.add_field( # Field that shows hp. 
        name="HP:", 
        value=str(hp[0]),
        inline=True)
      embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
        name="Zap (Weak) **No Cooldown**",
        value=str(attacks[3]["Zap"][evaluation[0]]),
        inline=True)
      embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
        name=f"Fireball (Normal) **Cooldown: {normal_c[0]}**",
        value=str(attacks[3]["Fireball"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
        name=f"Arcane Mania (Special) **Cooldown: {special_c[0]}**",
        value=str(attacks[3]["Arcane Mania"][evaluation[0]]),
        inline=False)
      embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
        name=f"Biden Blast (Avalon's Blessing) **Cooldown: {avalonbless_c[0]}**",
        value=str(attacks[3]["Biden Blast"][evaluation[0]]),
        inline=False)
      embed.set_thumbnail(url="https://i.imgur.com/0DpJe0b.png")  # Shows image of mage.

  if switch == False: # If it's the starter's turn, send the embed in their dm.
    await interaction.user.send(embed=embed, view=view)
    await view.wait()
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {interaction.user.id}")
        move_final = await cursor.fetchone()
        if startrand_mage == 7:
          if normal_c[0] == 0 and move_final[0] == "SUPER FIREBALL":
            await cursor.execute('UPDATE cooldowns SET n_cooldown = ? WHERE user_id = ?', (1, interaction.user.id,))
          elif normal_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c[0] - 1)} WHERE user_id = {interaction.user.id}')

          if special_c[0] == 0 and move_final[0] == "THE SORCERER'S WRATH":
            await cursor.execute('UPDATE cooldowns SET s_cooldown = ? WHERE user_id = ?', (2, interaction.user.id,))
          elif special_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c[0] - 1)} WHERE user_id = {interaction.user.id}')
          if avalonbless_c[0] == 0 and move_final[0] == "TRUE BIDEN BLAST!!!":
            await cursor.execute('UPDATE cooldowns SET ab_cooldown = ? WHERE user_id = ?', (3, interaction.user.id,))
          elif avalonbless_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c[0] - 1)} WHERE user_id = {interaction.user.id}')
          await db.commit()
          return move_final
        else:
          if normal_c[0] == 0 and move_final[0] == "Fireball":
            await cursor.execute('UPDATE cooldowns SET n_cooldown = ? WHERE user_id = ?', (1, interaction.user.id,))
          elif normal_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c[0] - 1)} WHERE user_id = {interaction.user.id}')
  
          if special_c[0] == 0 and move_final[0] == "Arcane Mania":
            await cursor.execute('UPDATE cooldowns SET s_cooldown = ? WHERE user_id = ?', (2, interaction.user.id,))
          elif special_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c[0] - 1)} WHERE user_id = {interaction.user.id}')
          
          if avalonbless_c[0] == 0 and move_final[0] == "Biden Blast":
            await cursor.execute('UPDATE cooldowns SET ab_cooldown = ? WHERE user_id = ?', (3, interaction.user.id,))
          elif avalonbless_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c[0] - 1)} WHERE user_id = {interaction.user.id}')
          await db.commit()
          return move_final
  elif switch == True: # If it's the reciever's turn, send the embed in their dm.
    await member.send(embed=embed, view=view)
    await view.wait()
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {member.id}")
        move_final = await cursor.fetchone()
        if recieverand_mage == 7:
          if normal_c[0] == 0 and move_final[0] == "SUPER FIREBALL":
            await cursor.execute('UPDATE cooldowns SET n_cooldown = ? WHERE user_id = ?', (1, member.id,))
          elif normal_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c[0] - 1)} WHERE user_id = {member.id}')

          if special_c[0] == 0 and move_final[0] == "THE SORCERER'S WRATH":
            await cursor.execute('UPDATE cooldowns SET s_cooldown = ? WHERE user_id = ?', (2, member.id,))
          elif special_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c[0] - 1)} WHERE user_id = {member.id}')

          if avalonbless_c[0] == 0 and move_final[0] == "TRUE BIDEN BLAST!!!":
            await cursor.execute('UPDATE cooldowns SET ab_cooldown = ? WHERE user_id = ?', (3, member.id,))
          elif avalonbless_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c[0] - 1)} WHERE user_id = {member.id}')
          await db.commit()
          return move_final
        else:
          if normal_c[0] == 0 and move_final[0] == "Fireball":
            await cursor.execute('UPDATE cooldowns SET n_cooldown = ? WHERE user_id = ?', (1, member.id,))
          elif normal_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c[0] - 1)} WHERE user_id = {member.id}')
  
          if special_c[0] == 0 and move_final[0] == "Arcane Mania":
            await cursor.execute('UPDATE cooldowns SET s_cooldown = ? WHERE user_id = ?', (2, member.id,))
          elif special_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c[0] - 1)} WHERE user_id = {member.id}')
  
          if avalonbless_c[0] == 0 and move_final[0] == "Biden Blast":
            await cursor.execute('UPDATE cooldowns SET ab_cooldown = ? WHERE user_id = ?', (3, member.id,))
          elif avalonbless_c[0] != 0:
            await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c[0] - 1)} WHERE user_id = {member.id}')
          await db.commit()
          return move_final
  if view.value is None:
    return
