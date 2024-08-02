import os
import nextcord
from nextcord.embeds import Embed
from nextcord import Interaction
import asyncio
import asyncpg
from battle_embeds import archer_battle
from battle_embeds import mage_battle
from battle_embeds import knight_battle
from nextcord.ext import commands
import random
from random import randint
import math


client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all()) # Define client.

#start_value of 1 is the starter
#start_value of 2 is the reciever

# Move function that returns what turn it is, taking the arguments interaction for who used battle, member for who recieved battle, start_rand for who starts in the battle, the class of the starter, and the class of the reciever.

async def move(interaction: Interaction, member: nextcord.Member, start_rand, startrand_mage, recieverand_mage, class_value_starter, class_value_reciever, starter_hp_value, reciever_hp_value, switch, turn, battle_screen, db_pool, starter_crit_num, reciever_crit_num, starter_av_blessing_hits, reciever_av_blessing_hits):
  if startrand_mage == 7 or recieverand_mage == 7:
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
        },
        4: {
          "THUNDERBOLT": -25,
          "SUPER FIREBALL": -40,
          "THE SORCERER'S WRATH": -70,
          "TRUE BIDEN BLAST!!!": -999
        }
      }
  else:
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

  crit_hit = randint(1, 5)
  if switch == None:
      if start_rand == 1:
        switch = False  
      elif start_rand == 2:
        switch = True

  # There is alot of repitition, so the code below will be explained with the first example as a sample. 
  if switch == False: # If it's the starter's turn.
    if class_value_starter == 1: # If the class of the starter is the knight.
        move = await knight_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value, battle_screen, db_pool) # Send respective embed depending on class and whosever turn it is.  
        if move == False:
            return
        elif move is None:
            await interaction.followup.send("Request timed out...Ending battle.")
            async with db_pool.acquire() as cursor:

              await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id) # If it times out after 120 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
              await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
              await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
              await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
              await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")

            return
        else:
          dmg = attacks[class_value_starter][move]
          if move == 'Sword Jab':
            miss = randint(1, 1000)
            if miss == 69:
              dmg = 0
          elif move == 'Sword Slash':
             miss = randint(1, 100)
             if miss <= 20:
               dmg = 0
          elif move == 'Dual Sword Attack':
            miss = randint(1, 100)
            if miss <= 40:
              dmg = 0
          elif move == 'Sliced and Diced':
            miss = randint(1, 100)
            if miss <= 65:
              dmg = 0
            else:
              starter_av_blessing_hits += 1

    elif class_value_starter == 2: # If the class of the starter is the archer.
        move = await archer_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value, battle_screen, db_pool)
        if move == False:
            return
        elif move is None:
              await interaction.followup.send("Request timed out...Ending battle.")
              async with db_pool.acquire() as cursor:

                await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id) # If it times out after 120 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
                await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
                await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
                await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")

              return
        else:
          dmg = attacks[class_value_starter][move]
          if move == 'Weak Arrow':
             miss = randint(1, 1000)
             if miss == 69:
                dmg = 0
          elif move == 'Piercing Shot':
             miss = randint(1, 100)
             if miss <= 20:
               dmg = 0
          elif move == 'Triple Shot':
            miss = randint(1, 100)
            if miss <= 40:
              dmg = 0
          elif move == 'Make it Rain':
            miss = randint(1, 100)
            if miss <= 65:
              dmg = 0
            else:
              starter_av_blessing_hits += 1

    elif class_value_starter == 3: # If the class of the starter is the mage.
        move = await mage_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value, startrand_mage, recieverand_mage, battle_screen, db_pool)
        if move == False:
          return
        elif move is None:
            await interaction.followup.send("Request timed out...Ending battle.")
            async with db_pool.acquire() as cursor:

              await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id) # If it times out after 120 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
              await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
              await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
              await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
              await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")

            return
        else: 
            if startrand_mage == 7:
              dmg = attacks[4][move]
              if startrand_mage == 7:
                if move == "THUNDERBOLT":
                  miss = randint(1, 100)
                  if miss <= 30:
                    dmg = 0
                elif move == "SUPER FIREBALL":
                  miss = randint(1, 100)
                  if miss <= 40:
                    dmg = 0
                elif move == "THE SORCERER'S WRATH":
                  miss = randint(1, 100)
                  if miss <= 65:
                    dmg = 0
                elif move == "TRUE BIDEN BLAST!!!":
                  miss = randint(1, 100)
                  if miss != 69:
                    dmg = 0
                  else:
                    starter_av_blessing_hits += 1
            else:
              dmg = (attacks[class_value_starter][move])
              if move == 'Zap':
                miss = randint(1, 1000)
                if miss == 69:
                  dmg = 0
              elif move == 'Fireball':
                miss = randint(1, 100)
                if miss <= 20:
                  dmg = 0 
              elif move == 'Arcane Mania':
                miss = randint(1, 100)              
                if miss <= 40:
                  dmg = 0
              elif move == 'Biden Blast':
                miss = randint(1, 100)
                if miss <= 65:
                  dmg = 0
                else:
                  starter_av_blessing_hits += 1
    switch = True

  elif switch == True: # Else if it's the reciever's turn.
    if class_value_reciever == 1: # If the class of the reciever is the knight.
        move = await knight_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value, battle_screen, db_pool)
        if move == False:
          return
        elif move is None:
              await interaction.followup.send("Request timed out...Ending battle.")
              async with db_pool.acquire() as cursor:

                await cursor.execute('DELETE FROM battles WHERE reciever_id = $1', member.id) 
                await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
                await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
                await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")

              return
        else:
                dmg = attacks[class_value_reciever][move]
                if move == 'Sword Jab':
                  miss = randint(1, 1000)
                  if miss == 69:
                    dmg = 0
                elif move == 'Sword Slash':
                   miss = randint(1, 100)
                   if miss <= 20:
                     dmg = 0
                elif move == 'Dual Sword Attack':
                  miss = randint(1, 100)
                  if miss <= 40:
                    dmg = 0
                elif move == 'Sliced and Diced':
                  miss = randint(1, 100)
                  if miss <= 65:
                    dmg = 0
                  else:
                    reciever_av_blessing_hits += 1
    elif class_value_reciever == 2: # If the class of the reciever is the archer.
        move = await archer_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value, battle_screen, db_pool)
        if move == False:
          return
        elif move is None:
                await interaction.followup.send("Request timed out...Ending battle.")
                async with db_pool.acquire() as cursor:

                  await cursor.execute('DELETE FROM battles WHERE reciever_id = $1', member.id) 
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
                  await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
                  await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")

                return
        else:
          dmg = attacks[class_value_reciever][move]
          if move == 'Weak Arrow':
             miss = randint(1, 1000)
             if miss == 69:
                dmg = 0
          elif move == 'Piercing Shot':
             miss = randint(1, 100)
             if miss <= 20:
               dmg = 0
          elif move == 'Triple Shot':
            miss = randint(1, 100)
            if miss <= 40:
              dmg = 0
          elif move == 'Make it Rain':
            miss = randint(1, 100)
            if miss <= 65:
              dmg = 0
            else:
              reciever_av_blessing_hits += 1

    elif class_value_reciever == 3: 
      # If the class of the reciever is the mage.
          move = await mage_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value, startrand_mage, recieverand_mage, battle_screen, db_pool)
          if move == False:
            return
          elif move is None:
                  await interaction.followup.send("Request timed out...Ending battle.")
                  async with db_pool.acquire() as cursor:

                    await cursor.execute('DELETE FROM battles WHERE reciever_id = $1', member.id) 
                    await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                    await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
                    await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
                    await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")

                  return
          else:
              if recieverand_mage == 7:
                dmg = attacks[4][move]
                if move == "THUNDERBOLT":
                  miss = randint(1, 100)
                  if miss <= 30:
                    dmg = 0
                elif move == "SUPER FIREBALL":
                  miss = randint(1, 100)
                  if miss <= 40:
                    dmg = 0
                elif move == "THE SORCERER'S WRATH":
                  miss = randint(1, 100)
                  if miss <= 65:
                    dmg = 0
                elif move == "TRUE BIDEN BLAST!!!":
                  miss = randint(1, 100)
                  if miss != 69:
                    dmg = 0
                  else:
                    reciever_av_blessing_hits += 1
              else:
                dmg = attacks[class_value_reciever][move]
                if move == 'Zap':
                  miss = randint(1, 1000)
                  if miss == 69:
                    dmg = 0
                elif move == 'Fireball':
                  miss = randint(1, 100)
                  if miss <= 20:
                    dmg = 0 
                elif move == 'Arcane Mania':
                  miss = randint(1, 100)              
                  if miss <= 40:
                    dmg = 0
                elif move == 'Biden Blast':
                  miss = randint(1, 100)
                  if miss <= 65:
                    dmg = 0
                  else:
                    reciever_av_blessing_hits += 1
    switch = False

  if crit_hit == 3:
    dmg *= 1.2
    if switch == False:
      reciever_crit_num += 1
    elif switch == True:
      starter_crit_num += 1

  dmg = math.floor(dmg)

  return switch, dmg, move, crit_hit, starter_crit_num, reciever_crit_num, starter_av_blessing_hits, reciever_av_blessing_hits