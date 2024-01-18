import nextcord
from nextcord.embeds import Embed
from nextcord import Interaction
import asyncio
import aiosqlite
from battle_embeds import archer_battle
from battle_embeds import mage_battle
from battle_embeds import knight_battle
from nextcord.ext import commands
import random
from random import randint


client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all()) # Define client.
      
# Dicts to store classx info:

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


#start_value of 1 is the starter
#start_value of 2 is the reciever

# Move function that returns what turn it is, taking the arguments interaction for who used battle, member for who recieved battle, start_rand for who starts in the battle, the class of the starter, and the class of the reciever.

async def move(interaction: Interaction, member: nextcord.Member, start_rand, class_value_starter, class_value_reciever, starter_hp_value, reciever_hp_value, class_evaluation_starter, class_evaluation_reciever, switch, turn):
  crit_hit = randint(1, 5)
  if switch == None:
    if start_rand == 1:
      switch = False
    elif start_rand == 2:
       switch = True

  # There is alot of repitition, so the code below will be explained with the first example as a sample. 
  if switch == False: # If it's the starter's turn.
    if class_value_starter[0] == 1: # If the class of the starter is the knight.
        await cursor.execute(f"INSERT INTO cooldowns (user_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES (?, ?, ?, ?)", (interaction.user.id, "Sword Jab", 0, "Sword Slash", 0, "Dual Sword Attack", 2, "Sliced and Diced", 3))
        move = await knight_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value) # Send respective embed depending on class and whosever turn it is.     
        check_deleted = None
      # Sample Explanation (applicable for rest)
        async with aiosqlite.connect("main.db") as db:        
            async with db.cursor() as cursor:
                await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
                check_deleted = await cursor.fetchone() # Check if /ff was used. 
            await db.commit()
        if check_deleted == None: # If it was, simply return and send nothing.
            return
        elif move is None: 
            await interaction.followup.send("Request timed out...Ending battle.")
            async with aiosqlite.connect("main.db") as db:     
                async with db.cursor() as cursor:
                    await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,)) # If it times out after 60 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
                    await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                    await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
                await db.commit() 
                return
        else:
          dmg = attacks[class_value_starter[0]][move[0]][evaluation[class_evaluation_starter]]
          if move[0] == 'Sword Jab':
            miss = randint(1, 1000)
            if miss == 69:
              dmg = 0
          elif move[0] == 'Sword Slash':
             miss = randint(1, 5)
             if miss == 2:
               dmg = 0
          elif move[0] == 'Dual Sword Attack':
            miss = randint(1, 2)
            if miss == 1:
              dmg = 0
          elif move[0] == 'Sliced and Diced':
            miss = randint(1, 4)
            if miss == 1 or miss == 3 or miss == 4:
              dmg = 0
    
    elif class_value_starter[0] == 2: # If the class of the starter is the archer.
      await cursor.execute(f"INSERT INTO cooldowns (user_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES (?, ?, ?, ?)", (interaction.user.id, "Weak Arrow", 0, "Piercing Shot", 0, "Triple Shot", 2, "Make it Rain", 3))
      move = await archer_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value)
      check_deleted = None
      async with aiosqlite.connect("main.db") as db:           
          async with db.cursor() as cursor:
              await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
              check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
      if check_deleted == None:
          return
      elif move is None: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:     
              async with db.cursor() as cursor:
                  await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,)) # If it times out after 60 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
              await db.commit() 
              return
      else:
        dmg = attacks[class_value_starter[0]][move[0]][evaluation[class_evaluation_starter]]
        if move[0] == 'Weak Arrow':
           miss = randint(1, 1000)
           if miss == 69:
              dmg = 0
        elif move[0] == 'Piercing Shot':
           miss = randint(1, 5)
           if miss == 2:
             dmg = 0
        elif move[0] == 'Triple Shot':
          miss = randint(1, 2)
          if miss == 1:
            dmg = 0
        elif move[0] == 'Make it Rain':
          miss = randint(1, 4)
          if miss == 1 or miss == 3 or miss == 4:
            dmg = 0

          
    elif class_value_starter[0] == 3: # If the class of the starter is the mage.
      await cursor.execute(f"INSERT INTO cooldowns (user_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES (?, ?, ?, ?)", (interaction.user.id, "Zap", 0, "Fireball", 0, "Arcane Mania", 2, "Biden Blast", 3))
      move = await mage_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value)
      check_deleted = None
      async with aiosqlite.connect("main.db") as db:         
          async with db.cursor() as cursor:
              await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
              check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
      if check_deleted == None:
          return
      elif move is None: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:     
              async with db.cursor() as cursor:
                  await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,)) # If it times out after 60 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
              await db.commit() 
              return
      else:
          dmg = attacks[class_value_starter[0]][move[0]][evaluation[class_evaluation_starter]]
          if move[0] == 'Zap':
             miss = randint(1, 1000)
             if miss == 69:
                dmg = 0
          elif move[0] == 'Fireball':
             miss = randint(1, 5)
             if miss == 2:
               dmg = 0
          elif move[0] == 'Arcane Mania':
            miss = randint(1, 2)
            if miss == 1:
              dmg = 0
          elif move[0] == 'Biden Blast':
            miss = randint(1, 4)
            if miss == 1 or miss == 3 or miss == 4:
              dmg = 0
    switch = True
    
  elif switch == True: # Else if it's the reciever's turn.
    if class_value_reciever[0] == 1: # If the class of the reciever is the knight.
      await cursor.execute(f"INSERT INTO cooldowns (user_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES (?, ?, ?, ?)", (member.id, "Sword Jab", 0, "Sword Slash", 0, "Dual Sword Attack", 2, "Sliced and Diced", 3))
      move = await knight_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value)
      check_deleted = None
      async with aiosqlite.connect("main.db") as db:           
          async with db.cursor() as cursor:
              await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,))
              check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
      if check_deleted == None:
          return
      elif move is None: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:      
              async with db.cursor() as cursor:
                  await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,)) 
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
              await db.commit()  
              return
      else:
          dmg = attacks[class_value_reciever[0]][move[0]][evaluation[class_evaluation_reciever]]
          if move[0] == 'Sword Jab':
             miss = randint(1, 1000)
             if miss == 69:
                dmg = 0
          elif move[0] == 'Sword Slash':
             miss = randint(1, 5)
             if miss == 2:
               dmg = 0
          elif move[0] == 'Dual Sword Attack':
            miss = randint(1, 2)
            if miss == 1:
              dmg = 0
          elif move[0] == 'Sliced and Diced':
            miss = randint(1, 4)
            if miss == 1 or miss == 3 or miss == 4:
              dmg = 0
        
    elif class_value_reciever[0] == 2: # If the class of the reciever is the archer.
      await cursor.execute(f"INSERT INTO cooldowns (user_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES (?, ?, ?, ?)", (member.id, "Weak Arrow", 0, "Piercing Shot", 0, "Triple Shot", 2, "Make it Rain", 3))
      move = await archer_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value)
      check_deleted = None
      async with aiosqlite.connect("main.db") as db:           
          async with db.cursor() as cursor:
              await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,))
              check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
      if check_deleted == None:
          return
      elif move is None: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:      
              async with db.cursor() as cursor:
                  await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,)) 
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                  await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
              await db.commit()  
              return
      else:
        dmg = attacks[class_value_reciever[0]][move[0]][evaluation[class_evaluation_reciever]]
        if move[0] == 'Weak Arrow':
           miss = randint(1, 1000)
           if miss == 69:
              dmg = 0
        elif move[0] == 'Piercing Shot':
           miss = randint(1, 5)
           if miss == 2:
             dmg = 0
        elif move[0] == 'Triple Shot':
          miss = randint(1, 2)
          if miss == 1:
            dmg = 0
        elif move[0] == 'Make it Rain':
          miss = randint(1, 4)
          if miss == 1 or miss == 3 or miss == 4:
            dmg = 0
            
    elif class_value_reciever[0] == 3: 
      # If the class of the reciever is the mage.
        await cursor.execute(f"INSERT INTO cooldowns (user_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES (?, ?, ?, ?)", (member.id, "Zap", 0, "Fireball", 0, "Arcane Mania", 2, "Biden Blast", 3))
        move = await mage_battle.battle_embd(interaction, member, switch, turn, starter_hp_value, reciever_hp_value)
        check_deleted = None
        async with aiosqlite.connect("main.db") as db:         
            async with db.cursor() as cursor:
                await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,))
                check_deleted = await cursor.fetchone() # Check if /ff was used. 
            await db.commit()
        if check_deleted == None:
            return
        elif move is None: 
            await interaction.followup.send("Request timed out...Ending battle.")
            async with aiosqlite.connect("main.db") as db:     
                async with db.cursor() as cursor:
                    await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,)) 
                    await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")
                    await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
                await db.commit()  
                return
        else:
            dmg = attacks[class_value_reciever[0]][move[0]][evaluation[class_evaluation_reciever]]
            if move[0] == 'Zap':
               miss = randint(1, 1000)
               if miss == 69:
                  dmg = 0
            elif move[0] == 'Fireball':
               miss = randint(1, 5)
               if miss == 2:
                 dmg = 0
            elif move[0] == 'Arcane Mania':
              miss = randint(1, 2)
              if miss == 1:
                dmg = 0
            elif move[0] == 'Biden Blast':
              miss = randint(1, 4)
              if miss == 1 or miss == 3 or miss == 4:
                dmg = 0
    switch = False
    
  if crit_hit == 3:
    dmg *= 1.2

  return switch, dmg, move, crit_hit 
    
      