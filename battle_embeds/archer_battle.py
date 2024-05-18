import os
import nextcord
from nextcord.embeds import Embed
import nextcord.interactions 
from nextcord import Interaction
import asyncpg

# Useful source throughout: https://discordpy.readthedocs.io/en/stable/interactions/api.html

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
      "Strong": -45,
    },
    "Sliced and Diced": {
      "Weak": -55,
      "Normal": -60,
      "Strong": -65,
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
      "Strong": -60,
    },
    "Make it Rain": {
      "Weak": -75,
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
    "Strong": -30
  },
  "Arcane Mania": {
    "Weak": -42,
    "Normal": -47,
    "Strong": -55,
  },
  "Biden Blast": {
    "Weak": -70,
    "Normal": -75,
    "Strong": -80,
  }
}

}

# Function to send an embed to the user when they use battle if they picked archer.
async def battle_embd(interaction: Interaction, member: nextcord.Member, switch, turn, starter_hp_value, reciever_hp_value, battle_screen, db_pool):
  id_user = interaction.user.id 
  id_member = member.id
  async with db_pool.acquire() as cursor:

    if switch == False:
      normal_c = await cursor.fetchval('SELECT n_cooldown FROM cooldowns WHERE user_id = $1', interaction.user.id)
      special_c = await cursor.fetchval('SELECT s_cooldown FROM cooldowns WHERE user_id = $1', interaction.user.id)
      avalonbless_c = await cursor.fetchval('SELECT ab_cooldown FROM cooldowns WHERE user_id = $1', interaction.user.id)
    elif switch == True:
      normal_c = await cursor.fetchval('SELECT n_cooldown FROM cooldowns WHERE user_id = $1', member.id)
      special_c = await cursor.fetchval('SELECT s_cooldown FROM cooldowns WHERE user_id = $1', member.id)
      avalonbless_c = await cursor.fetchval('SELECT ab_cooldown FROM cooldowns WHERE user_id = $1', member.id)

  class ChooseFour(nextcord.ui.View):
    def __init__(self):
      super().__init__(timeout=120)
      self.value = None

    @nextcord.ui.button(label="Forfeit", style=nextcord.ButtonStyle.red)
    async def ff(self, button: nextcord.ui.Button, interaction: Interaction):
            if switch == False and interaction.user.id != id_user:
                await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
            elif switch == True and interaction.user.id != id_member:
                await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
            else:
                async with db_pool.acquire() as cursor:
                  if switch is False: 
                    await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id)
                  elif switch is True: 
                     await cursor.execute('DELETE FROM battles WHERE reciever_id = $1', interaction.user.id)
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id}")
                  await cursor.execute(f"DELETE FROM moves WHERE opponent_id = {interaction.user.id}")
                  await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
                  await cursor.execute(f"DELETE FROM cooldowns WHERE opponent_id = {interaction.user.id}")
                  await interaction.response.send_message(f"{interaction.user.mention} has run away from the battle!", ephemeral=False) 
                self.value = "FF"
                self.stop()

    @nextcord.ui.button(label = "Weak Arrow", style=nextcord.ButtonStyle.blurple)
    async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.defer()
        if switch == False and interaction.user.id != id_user:
            await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
        elif switch == True and interaction.user.id != id_member:
            await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
        else:
            move = "Weak Arrow"
            async with db_pool.acquire() as cursor:

              if switch == False:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", id_user, member.id, move, turn)
              elif switch == True:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", member.id, id_user, move, turn)

            self.value = True
            self.stop()

    if normal_c == 0:
      @nextcord.ui.button(label = "Piercing Shot", style=nextcord.ButtonStyle.blurple)
      async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
            await interaction.response.defer()
            if switch == False and interaction.user.id != id_user:
                await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
            elif switch == True and interaction.user.id != id_member:
                await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
            else:
                move = "Piercing Shot"
                async with db_pool.acquire() as cursor:

                  if switch == False:
                    await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", id_user, member.id, move, turn)
                  elif switch == True:
                    await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", member.id, id_user, move, turn)

                self.value = True
                self.stop()

    if special_c == 0:
       @nextcord.ui.button(label = "Triple Shot", style=nextcord.ButtonStyle.blurple)
       async def special(self, button: nextcord.ui.Button, interaction: Interaction):
              await interaction.response.defer()
              if switch == False and interaction.user.id != id_user:
                  await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
              elif switch == True and interaction.user.id != id_member:
                  await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
              else:
                    move = "Triple Shot"
                    async with db_pool.acquire() as cursor:

                      if switch == False:
                        await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", id_user, member.id, move, turn)
                      elif switch == True:
                        await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", member.id, id_user, move, turn)

                    self.value = True
                    self.stop()

    if avalonbless_c == 0:
      @nextcord.ui.button(label = "Make it Rain", style=nextcord.ButtonStyle.blurple)
      async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
          await interaction.response.defer()
          if switch == False and interaction.user.id != id_user:
              await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
          elif switch == True and interaction.user.id != id_member:
              await interaction.followup.send("Buddy you can't choose their move for them!", ephemeral=True)
          else:
              move = "Make it Rain"
              async with db_pool.acquire() as cursor:

                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", id_user, member.id, move, turn)
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", member.id, id_user, move, turn)

              self.value = True
              self.stop()
              
  view = ChooseFour()
  hp = None # Define hp
  evaluation = None # Define evaluation
  async with db_pool.acquire() as cursor:

    if switch == False: # If it's the starter's turn
      user = interaction.user
      hp = await cursor.fetchval(f"SELECT starter_hp FROM battles WHERE starter_id = {interaction.user.id}") # Get hp value of that user
      evaluation = await cursor.fetchval(f"SELECT evaluation_starter FROM battles WHERE starter_id = {interaction.user.id}") # Get the evaluation of that user
    elif switch == True: # If it's the reciever's turn
      user = member
      hp = await cursor.fetchval(f"SELECT reciever_hp FROM battles WHERE starter_id = {interaction.user.id}")  # Get hp value of that user
      evaluation = await cursor.fetchval(f"SELECT evaluation_reciever FROM battles WHERE starter_id = {interaction.user.id}") # Get the evaluation of that user

  embed = Embed( # Title and description, indicating user to pick a move.
    title = f"{user} Moves",
    description = "",
    color = nextcord.Color.green())
  embed.add_field( # Field that shows hp.
    name="HP:", 
    value=str(hp),
    inline=False)
  embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
    name="Weak Arrow (Weak) **No Cooldown**",
    value=str(attacks[2]["Weak Arrow"][evaluation]),
    inline=False)
  embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
    name=f"Piercing Shot (Normal) **Cooldown: {normal_c}**",
    value=str(attacks[2]["Piercing Shot"][evaluation]),
    inline=False)
  embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
    name=f"Triple Shot (Special) **Cooldown: {special_c}**",
    value=str(attacks[2]["Triple Shot"][evaluation]),
    inline=False)
  embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
    name=f"Make it Rain (Avalon's Blessing) **Cooldown: {avalonbless_c}**",
    value=str(attacks[2]["Make it Rain"][evaluation]),
    inline=False)            
  embed.set_thumbnail( # Shows image of archer.
    url="https://i.imgur.com/NcJsHO3.png"
  ) 
  if switch == False: # If it's the starter's turn, send the embed in their dm.
    message = await interaction.followup.send(embed=embed, view=view)
    await view.wait()
    if view.value is None:
      return
    elif view.value == "FF":
      return False
    await message.delete()
    if battle_screen != None:
      await battle_screen.delete()
    async with db_pool.acquire() as cursor:

      move_final = await cursor.fetchval(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {interaction.user.id}")
      if normal_c == 0 and move_final == "Piercing Shot":
        await cursor.execute('UPDATE cooldowns SET n_cooldown = $1 WHERE user_id = $2', 1, interaction.user.id)
      elif normal_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c - 1)} WHERE user_id = {interaction.user.id}')

      if special_c == 0 and move_final == "Triple Shot":
        await cursor.execute('UPDATE cooldowns SET s_cooldown = $1 WHERE user_id = $2', 2, interaction.user.id)
      elif special_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c - 1)} WHERE user_id = {interaction.user.id}')

      if avalonbless_c == 0 and move_final == "Make it Rain":
        await cursor.execute('UPDATE cooldowns SET ab_cooldown = $1 WHERE user_id = $2', 3, interaction.user.id)
      elif avalonbless_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c - 1)} WHERE user_id = {interaction.user.id}')

    return move_final

  elif switch == True: # If it's the reciever's turn, send the embed in their dm.
    message = await interaction.followup.send(embed=embed, view=view)
    await view.wait()
    if view.value is None:
      return
    elif view.value == "FF":
      return False
    await message.delete()
    if battle_screen != None:
      await battle_screen.delete()
    async with db_pool.acquire() as cursor:

      move_final = await cursor.fetchval(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {member.id}")
      if normal_c == 0 and move_final == "Piercing Shot":
        await cursor.execute('UPDATE cooldowns SET n_cooldown = $1 WHERE user_id = $2', 1, member.id)
      elif normal_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c - 1)} WHERE user_id = {member.id}')

      if special_c == 0 and move_final == "Triple Shot":
        await cursor.execute('UPDATE cooldowns SET s_cooldown = $1 WHERE user_id = $2', 2, member.id)
      elif special_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c - 1)} WHERE user_id = {member.id}')

      if avalonbless_c == 0 and move_final == "Make it Rain":
        await cursor.execute('UPDATE cooldowns SET ab_cooldown = $1 WHERE user_id = $2', 3, member.id)
      elif avalonbless_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c - 1)} WHERE user_id = {member.id}')

    return move_final