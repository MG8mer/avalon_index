import os
import nextcord
from nextcord.embeds import Embed
import nextcord.interactions 
import asyncpg
from nextcord import Interaction

# Useful source throughout: https://discordpy.readthedocs.io/en/stable/interactions/api.html

# Dicts to store class info: 

# Class health
health = {
  1: 150,
  2: 100,
  3: 125
}

# Dict order:
  # Class
    # Attacks: Damage:

attacks = {
    1: {
      "Sword Jab": -10,
      "Sword Slash": -20,
      "Dual Sword Attack": -35,
      "Sliced and Diced": -65
    },
    2: {
      "Weak Arrow": -20,
      "Piercing Shot": -30,
      "Triple Shot": -45,
      "Make it Rain": -75
    },
    3: {
      "Zap": -15,
      "Fireball": -25,
      "Arcane Mania": -40,
      "Biden Blast": -70,
    }
}

# Function to send an embed to the user when they use battle if they picked knight.
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

    if turn <= 3:
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
              await interaction.response.send_message(f"{interaction.user.mention} has run away from the battle! No XP gained by either party...", ephemeral=False) 
            self.value = "FF"
            self.stop()

    @nextcord.ui.button(label = "Sword Jab", style=nextcord.ButtonStyle.blurple)
    async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
      if switch == False and interaction.user.id != id_user:
          await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
      elif switch == True and interaction.user.id != id_member:
          await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
      else:
          move = "Sword Jab"
          async with db_pool.acquire() as cursor:

            if switch == False:
              await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", id_user, member.id, move, turn)
            elif switch == True:
              await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", member.id, id_user, move, turn)

          self.value = True
          self.stop()

    if normal_c == 0:
      @nextcord.ui.button(label = "Sword Slash", style=nextcord.ButtonStyle.blurple)
      async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
        if switch == False and interaction.user.id != id_user:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        elif switch == True and interaction.user.id != id_member:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        else:
            move = "Sword Slash"
            async with db_pool.acquire() as cursor:

              if switch == False:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", id_user, member.id, move, turn)
              elif switch == True:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", member.id, id_user, move, turn)

            self.value = True
            self.stop()

    if special_c == 0:
      @nextcord.ui.button(label = "Dual Sword Attack", style=nextcord.ButtonStyle.blurple)
      async def special(self, button: nextcord.ui.Button, interaction: Interaction):
        if switch == False and interaction.user.id != id_user:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        elif switch == True and interaction.user.id != id_member:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        else:
            move = "Dual Sword Attack"
            async with db_pool.acquire() as cursor:

              if switch == False:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", id_user, member.id, move, turn)
              elif switch == True:
                await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES ($1, $2, $3, $4)", member.id, id_user, move, turn)

            self.value = True
            self.stop()

    if avalonbless_c == 0:
      @nextcord.ui.button(label = "Sliced and Diced", style=nextcord.ButtonStyle.blurple)
      async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
        if switch == False and interaction.user.id != id_user:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        elif switch == True and interaction.user.id != id_member:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        else:
            move = "Sliced and Diced"
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
    elif switch == True: # If it's the reciever's turn
      user = member
      hp = await cursor.fetchval(f"SELECT reciever_hp FROM battles WHERE starter_id = {interaction.user.id}") # Get hp value of that user

  embed = Embed( # Title and description, indicating user to pick a move.
    title = f"{user} Moves",
     description = "",
    color = nextcord.Color.dark_gray())
  embed.add_field( # Field that shows hp.   
    name="HP:", 
    value=str(hp),
    inline=False)
  embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
    name="Sword Jab (Weak) **No Cooldown; Hit Chance: 99.9%**",
    value=str(attacks[1]["Sword Jab"]),
    inline=False)
  embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
    name=f"Sword Slash (Normal) **Cooldown: {normal_c}; Hit Chance: 80%**",
    value=str(attacks[1]["Sword Slash"]),
    inline=False)
  embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
    name=f"Dual Sword Attack (Special) **Cooldown: {special_c}; ; Hit Chance: 60%**",
    value=str(attacks[1]["Dual Sword Attack"]),
    inline=False)
  embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
    name=f"Sliced and Diced (Avalon's Blessing) **Cooldown: {avalonbless_c}; Hit Chance: 35%**",
    value=str(attacks[1]["Sliced and Diced"]),
    inline=False)            
  embed.set_thumbnail(url="https://i.imgur.com/soNMbTL.png")  # Shows image of knight.
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
      if normal_c == 0 and move_final == "Sword Slash":
        await cursor.execute('UPDATE cooldowns SET n_cooldown = $1 WHERE user_id = $2', 1, interaction.user.id)
      elif normal_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c - 1)} WHERE user_id = {interaction.user.id}')

      if special_c == 0 and move_final == "Dual Sword Attack":
        await cursor.execute('UPDATE cooldowns SET s_cooldown = $1 WHERE user_id = $2', 2, interaction.user.id)
      elif special_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c - 1)} WHERE user_id = {interaction.user.id}')

      if avalonbless_c == 0 and move_final == "Sliced and Diced":
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
      if normal_c == 0 and move_final == "Sword Slash":
        await cursor.execute('UPDATE cooldowns SET n_cooldown = $1 WHERE user_id = $2', 1, member.id)
      elif normal_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c - 1)} WHERE user_id = {member.id}')

      if special_c == 0 and move_final == "Dual Sword Attack":
        await cursor.execute('UPDATE cooldowns SET s_cooldown = $1 WHERE user_id = $2', 2, member.id)
      elif special_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c - 1)} WHERE user_id = {member.id}')

      if avalonbless_c == 0 and move_final == "Sliced and Diced":
        await cursor.execute('UPDATE cooldowns SET ab_cooldown = $1 WHERE user_id = $2', 3, member.id)
      elif avalonbless_c != 0:
        await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c - 1)} WHERE user_id = {member.id}')

    return move_final  