import nextcord
import random
from nextcord.embeds import Embed
from nextcord import Interaction
from nextcord.ext import commands
import asyncio
import pick_move
import aiosqlite
import battle_page

# Useful source throughout: https://discordpy.readthedocs.io/en/stable/interactions/api.html

# Dicts to store class info:

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all()) # Define client.

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
      "Normal": -45,
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
      "Normal": -50,
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

# Define important variables to be used globally.
class_evaluation_reciever = None # Eval of reciever
class_evaluation_starter = None # Eval of strter
class_value_reciever = None # Class of reciever
class_value_starter = None # Class of starter
battle_value = None # If battle has been initiated 
starter_hp_value = None # hp of starter
reciever_hp_value = None # hp of reciever

async def battle(interaction: Interaction, member: nextcord.Member, start_rand):
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (interaction.user.id,))
      class_value_starter = await cursor.fetchone() # here
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (member.id,))
      class_value_reciever = await cursor.fetchone() # here
      class_evaluation_starter = str(class_value_starter[0]) + str(class_value_reciever[0]) # Concatenate strings of class values to see their evaluation according to the assigned dictionary.
      class_evaluation_reciever = str(class_value_reciever[0]) + str(class_value_starter[0]) # Concatenate strings of class values to see their evaluation according to the assigned dictionary.
      await cursor.execute('UPDATE battles SET battle = ?, starter_hp = ?, reciever_hp = ?, evaluation_starter = ?, evaluation_reciever = ? WHERE starter_id = ? AND reciever_id = ?', (1, health[class_value_starter[0]], health[class_value_reciever[0]], evaluation[class_evaluation_starter], evaluation[class_evaluation_reciever], interaction.user.id, member.id,)) # Update the battle row of both users, insertting values such as their health, evaluation determined by insertting the concatenated string above into the dict, and their ids.
      await cursor.execute('SELECT starter_hp FROM battles WHERE starter_id = ?', (interaction.user.id,))
      starter_hp_value = await cursor.fetchone()
      await cursor.execute('SELECT reciever_hp FROM battles WHERE reciever_id = ?', (member.id,))
      reciever_hp_value = await cursor.fetchone()
    await db.commit()
  switch = None # Define turns
  switch_value = None # Define another variable for turns
  turn = 0 # Turn num
  hp_starter = starter_hp_value[0] 
  hp_reciever = reciever_hp_value[0]
  while hp_starter > 0 and hp_reciever > 0:
    # Below https://stackoverflow.com/questions/21837208/check-if-a-number-is-odd-or-even-in-python
    if turn == 0 or turn % 2 == 0: # if turn is even, define switch_value, insertting switch into the move function in the pick_move file to return switch later and await whosever turn it is to pick a move.
      try:
        switch_value, dmg, move, crit_hit = await pick_move.move(interaction, member, start_rand, class_value_starter, class_value_reciever, starter_hp_value, reciever_hp_value, class_evaluation_starter, class_evaluation_reciever, switch, turn)
      except TypeError:
        return
      else:
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            if switch_value == True:
              hp_reciever += (dmg)
              await cursor.execute(f'UPDATE battles SET reciever_hp = {hp_reciever}') 
            elif switch_value == False:
              hp_starter += (dmg)
              await cursor.execute(f'UPDATE battles SET starter_hp = {hp_starter}') 
              starter_hp_test = await cursor.fetchone()
          await db.commit()
          
        if switch_value == False:
          if dmg == 0:
            hp_percentage = (hp_starter//starter_hp_value[0])*100
            await battle_page.battle_page(interaction, member, f"{member.mention} used the move **{move[0]}**, but missed the attack and dealt **0** damage! \n{interaction.user.mention} still has an HP of ***{hp_starter}***", hp_percentage)
            await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, but missed the attack and dealt **0** damage! \n{interaction.user.mention} still has an HP of ***{hp_starter}***")
          elif crit_hit == 3:
            if hp_starter <= 0:
              await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{interaction.user.mention} now has a depleted HP of ***0***")
            else:
              await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{interaction.user.mention} now has an HP of ***{hp_starter}***")
          else:
            if hp_starter <= 0:
              await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{interaction.user.mention} now has a depleted HP of ***0***")
            else:
              await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{interaction.user.mention} now has an HP of ***{hp_starter}***")
        elif switch_value == True:
          if dmg == 0:
            await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, but missed the attack and dealt **0** damage! \n{member.mention} still has an HP of ***{hp_reciever}***")
          elif crit_hit == 3:
            if hp_reciever <= 0:
              await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{member.mention} now has a depleted HP of ***0***")
            else:
              await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{member.mention} now has an HP of ***{hp_reciever}***")
          else:
              if hp_reciever <= 0:
                await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{member.mention} now has a depleted HP of ***0***")
              else:
                await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{member.mention} now has an HP of ***{hp_reciever}***")
        turn += 1
        try:
          await client.wait_for("message", timeout=5.0, check=lambda message: interaction.user.id == member.id)
        except asyncio.TimeoutError:
          pass
          
    else:  # if turn is odd, define switch, insertting switch_value into the move function in the pick_move file to return switch later and await whosever turn it is to pick a move.
      try:
        switch, dmg, move, crit_hit = await pick_move.move(interaction, member, start_rand, class_value_starter, class_value_reciever, starter_hp_value, reciever_hp_value, class_evaluation_starter, class_evaluation_reciever, switch_value, turn)
      except TypeError:
        return
      else:
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            if switch == True:
              hp_reciever += (dmg)
              await cursor.execute(f'UPDATE battles SET reciever_hp = {hp_reciever}') 
            elif switch == False:
              hp_starter += (dmg)
              await cursor.execute(f'UPDATE battles SET starter_hp = {hp_starter}') 
              starter_hp_test = await cursor.fetchone()
          await db.commit()
          
          if switch == False:
            if dmg == 0:
              await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, but missed the attack and dealt **0** damage! \n{interaction.user.mention} still has an HP of ***{hp_starter}***")
            elif crit_hit == 3:
              if hp_starter <= 0:
                await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{interaction.user.mention} now has a depleted HP of ***0***")
              else:
                await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{interaction.user.mention} now has an HP of ***{hp_starter}***")
            else:
              if hp_starter <= 0:
                await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{interaction.user.mention} now has a depleted HP of ***0***")
              else:
                await interaction.followup.send(f"{member.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{interaction.user.mention} now has an HP of ***{hp_starter}***")
          elif switch == True:
            if dmg == 0:
                await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, but missed the attack and dealt **0** damage! \n{member.mention} still has an HP of ***{hp_reciever}***")
            elif crit_hit == 3:
               if hp_reciever <= 0:
                  await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{member.mention} now has a depleted HP of ***0***")
               else:
                  await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{member.mention} now has an HP of ***{hp_reciever}***")
            else:
              if hp_reciever <= 0:
                await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{member.mention} now has a depleted HP of ***0***")
              else:
                await interaction.followup.send(f"{interaction.user.mention} used the move **{move[0]}**, dealing **{dmg*-1}** damage! \n{member.mention} now has an HP of ***{hp_reciever}***")
        turn += 1
        try:
          await client.wait_for("message", timeout=5.0, check=lambda message: interaction.user.id == member.id)
        except asyncio.TimeoutError:
          pass
        
    if starter_hp_value[0] == None or reciever_hp_value[0] == None: # If the row has been deleted in pick_move, making these value none due to returning nothing, break the loop, ending the battle. 
      break
 # Add 1 to the turn count to cycle through the loop another time if its condition is still true, being that both players' health points are above 0.
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,))
      await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
      await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
      await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
      await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")
    await db.commit()
  if hp_starter <= 0:
    await interaction.followup.send(f"The battle has concluded and {member.mention} has won!")
  elif hp_reciever <= 0:
    await interaction.followup.send(f"The battle has concluded and {interaction.user.mention} has won!")