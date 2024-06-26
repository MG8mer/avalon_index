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

async def move(interaction: Interaction, member: nextcord.Member, start_rand, startrand_mage, recieverand_mage, class_value_starter, class_value_reciever, starter_hp_value, reciever_hp_value, class_evaluation_starter, class_evaluation_reciever, switch, turn, battle_screen, db_pool, starter_crit_num, reciever_crit_num, starter_av_blessing_hits, reciever_av_blessing_hits):
  if startrand_mage == 7 or recieverand_mage == 7:
      # Dicts to store class info:

      # Class health
      health = {
        1: 150,
        2: 100,
        3: 125
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
            "Weak": -10,
            "Normal": -15,
            "Strong": -20
          },
          "Sword Slash": {
            "Weak": -15,
            "Normal": -25,
            "Strong": -35
          },
          "Dual Sword Attack": {
            "Weak": -30,
            "Normal": -45,
            "Strong": -60
          },
          "Sliced and Diced": {
            "Weak": -50,
            "Normal": -75,
            "Strong": -100
          }
        },
        2: {
          "Weak Arrow": {
            "Weak": -15,
            "Normal": -20,
            "Strong": -25
          },
          "Piercing Shot": {
            "Weak": -25,
            "Normal": -35,
            "Strong": -45
          },
          "Triple Shot": {
            "Weak": -50,
            "Normal": -70,
            "Strong": -90
          },
          "Make it Rain": {
            "Weak": -85,
            "Normal": -125,
            "Strong": -150
          }
        },
        3: {
        "Zap": {
          "Weak": -12,
          "Normal": -18,
          "Strong": -22
        },
        "Fireball": {
          "Weak": -22,
          "Normal": -32,
          "Strong": -42
        },
        "Arcane Mania": {
          "Weak": -45,
          "Normal": -65,
          "Strong": -80
        },
        "Biden Blast": {
          "Weak": -75,
          "Normal": -100,
          "Strong": -125
        }
      },
      4: {
      "THUNDERBOLT": {
        "Weak": -15,
        "Normal": -20,
        "Strong": -25
      },
      "SUPER FIREBALL": {
        "Weak": -25,
        "Normal": -35,
        "Strong": -45
      },
      "THE SORCERER'S WRATH": {
        "Weak": -50,
        "Normal": -70,
        "Strong": -90
      },
      "TRUE BIDEN BLAST!!!": {
        "Weak": -999,
        "Normal": -999,
        "Strong": -999
      }
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
          "Weak": -10,
          "Normal": -15,
          "Strong": -20
        },
        "Sword Slash": {
          "Weak": -15,
          "Normal": -25,
          "Strong": -35
        },
        "Dual Sword Attack": {
          "Weak": -30,
          "Normal": -45,
          "Strong": -60
        },
        "Sliced and Diced": {
          "Weak": -50,
          "Normal": -75,
          "Strong": -100
        }
      },
      2: {
        "Weak Arrow": {
          "Weak": -15,
          "Normal": -20,
          "Strong": -25
        },
        "Piercing Shot": {
          "Weak": -25,
          "Normal": -35,
          "Strong": -45
        },
        "Triple Shot": {
          "Weak": -50,
          "Normal": -70,
          "Strong": -90,
        },
        "Make it Rain": {
          "Weak": -85,
          "Normal": -125,
          "Strong": -150,
        }
      },
      3: {
      "Zap": {
        "Weak": -12,
        "Normal": -18,
        "Strong": -22
      },
      "Fireball": {
        "Weak": -22,
        "Normal": -32,
        "Strong": -42
      },
      "Arcane Mania": {
        "Weak": -45,
        "Normal": -65,
        "Strong": -80,
      },
      "Biden Blast": {
        "Weak": -75,
        "Normal": -100,
        "Strong": -125,
      }
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
          dmg = attacks[class_value_starter][move][evaluation[class_evaluation_starter]]
          if move == 'Sword Jab':
            miss = randint(1, 800)
            if miss == 69:
              dmg = 0
          elif move == 'Sword Slash':
             miss = randint(1, 4)
             if miss == 2:
               dmg = 0
          elif move == 'Dual Sword Attack':
            miss = randint(1, 10)
            if miss == 1 or miss == 3 or miss == 5 or miss == 7 or miss == 9 or miss == 10:
              dmg = 0
          elif move == 'Sliced and Diced':
            miss = randint(1, 10)
            if miss == 1 or miss == 2 or miss == 3 or miss == 5 or miss == 6 or miss == 8 or miss == 9 or miss == 10:
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
          dmg = attacks[class_value_starter][move][evaluation[class_evaluation_starter]]
          if move == 'Weak Arrow':
             miss = randint(1, 1000)
             if miss == 69:
                dmg = 0
          elif move == 'Piercing Shot':
             miss = randint(1, 5)
             if miss == 2:
               dmg = 0
          elif move == 'Triple Shot':
            miss = randint(1, 2)
            if miss == 1:
              dmg = 0
          elif move == 'Make it Rain':
            miss = randint(1, 4)
            if miss == 1 or miss == 3 or miss == 4:
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
              dmg = attacks[4][move][evaluation[class_evaluation_starter]]
              if startrand_mage == 7:
                if move == "THUNDERBOLT":
                  miss = randint(1, 2)
                  if miss == 1:
                    dmg = 0
                elif move == "SUPER FIREBALL":
                  miss = randint(1, 10)
                  if miss == 2 or miss == 4 or miss == 6 or miss == 8 or miss == 9 or miss == 10:
                    dmg = 0
                elif move == "THE SORCERER'S WRATH":
                  miss = randint(1, 4)
                  if miss == 2 or miss == 3 or miss == 4:
                    dmg = 0
                elif move == "TRUE BIDEN BLAST!!!":
                  miss = randint(1, 100)
                  if miss != 69:
                    dmg = 0
                  else:
                    starter_av_blessing_hits += 1
            else:
              dmg = (attacks[class_value_starter][move][evaluation[class_evaluation_starter]])
              if move == 'Zap':
                miss = randint(1, 1000)
                if miss == 69:
                  dmg = 0
              elif move == 'Fireball':
                miss = randint(1, 5)
                if miss == 2:
                  dmg = 0 
              elif move == 'Arcane Mania':
                miss = randint(1, 2)              
                if miss == 1:
                  dmg = 0
              elif move == 'Biden Blast':
                miss = randint(1, 4)
                if miss == 1 or miss == 3 or miss == 4:
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
                dmg = attacks[class_value_reciever][move][evaluation[class_evaluation_reciever]]
                if move == 'Sword Jab':
                  miss = randint(1, 800)
                  if miss == 69:
                    dmg = 0
                elif move == 'Sword Slash':
                   miss = randint(1, 4)
                   if miss == 2:
                     dmg = 0
                elif move == 'Dual Sword Attack':
                  miss = randint(1, 10)
                  if miss == 1 or miss == 3 or miss == 5 or miss == 7 or miss == 9 or miss == 10:
                    dmg = 0
                elif move == 'Sliced and Diced':
                  miss = randint(1, 10)
                  if miss == 1 or miss == 2 or miss == 3 or miss == 5 or miss == 6 or miss == 8 or miss == 9 or miss == 10:
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
          dmg = attacks[class_value_reciever][move][evaluation[class_evaluation_reciever]]
          if move == 'Weak Arrow':
             miss = randint(1, 1000)
             if miss == 69:
                dmg = 0
          elif move == 'Piercing Shot':
             miss = randint(1, 5)
             if miss == 2:
               dmg = 0
          elif move == 'Triple Shot':
            miss = randint(1, 2)
            if miss == 1:
              dmg = 0
          elif move == 'Make it Rain':
            miss = randint(1, 4)
            if miss == 1 or miss == 3 or miss == 4:
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
                dmg = attacks[4][move][evaluation[class_evaluation_reciever]]
                if move == "THUNDERBOLT":
                  miss = randint(1, 2)
                  if miss == 1:
                    dmg = 0
                elif move == "SUPER FIREBALL":
                  miss = randint(1, 10)
                  if miss == 2 or miss == 4 or miss == 6 or miss == 8 or miss == 9 or miss == 10:
                    dmg = 0
                elif move == "THE SORCERER'S WRATH":
                  miss = randint(1, 4)
                  if miss == 2 or miss == 3 or miss == 4:
                    dmg = 0
                elif move == "TRUE BIDEN BLAST!!!":
                  miss = randint(1, 100)
                  if miss != 69:
                    dmg = 0
                  else:
                    reciever_av_blessing_hits += 1
              else:
                dmg = attacks[class_value_reciever][move][evaluation[class_evaluation_reciever]]
                if move == 'Zap':
                  miss = randint(1, 1000)
                  if miss == 69:
                    dmg = 0
                elif move == 'Fireball':
                  miss = randint(1, 5)
                  if miss == 2:
                    dmg = 0 
                elif move == 'Arcane Mania':
                  miss = randint(1, 2)              
                  if miss == 1:
                    dmg = 0
                elif move == 'Biden Blast':
                  miss = randint(1, 4)
                  if miss == 1 or miss == 3 or miss == 4:
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
