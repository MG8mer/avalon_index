import nextcord
from nextcord.embeds import Embed
from nextcord import Interaction
import asyncio
import aiosqlite
from battle_embeds import archer_battle
from battle_embeds import mage_battle
from battle_embeds import knight_battle
from nextcord.ext import commands



client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all()) # Define client.
      
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

#start_value of 1 is the starter
#start_value of 2 is the reciever

# Move function that returns what turn it is, taking the arguments interaction for who used battle, member for who recieved battle, start_rand for who starts in the battle, the class of the starter, and the class of the reciever.

async def move(interaction: Interaction, member: nextcord.Member, start_rand, class_value_starter, class_value_reciever, class_evaluation_starter, class_evaluation_reciever, switch):
  if switch == None:
    if start_rand == 1:
      switch = False
    elif start_rand == 2:
      switch = True

  # There is alot of repitition, so the code below will be explained with the first example as a sample. 
  if switch == False: # If it's the starter's turn.
    if class_value_starter[0] == 1: # If the class of the starter is the knight.
        await knight_battle.battle_embd(interaction, member, switch) # Send respective embed depending on class and whosever turn it is.     
        check_deleted = None
        dmg = None
      # Sample Explanation (applicable for rest)
        while dmg == None:
          await interaction.followup.send(f"Pick from the avaliable moves {interaction.user.mention}!")
          try: # Try awaiting for a message from the user's turn.
            msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
          except asyncio.TimeoutError:
            async with aiosqlite.connect("main.db") as db:                 
              async with db.cursor() as cursor:
                await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
                check_deleted = await cursor.fetchone() # Check if /ff was used. 
              await db.commit()
            if check_deleted == None: # If it was, simply return and send nothing.
              return
            else: 
              await interaction.followup.send("Request timed out...Ending battle.")
              async with aiosqlite.connect("main.db") as db:               
                async with db.cursor() as cursor:
                  await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,)) # If it times out after 60 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
                await db.commit() 
                return
          
          if msg.content == "yes": # msg.content == "Sword Jab" or msg.content == "Sword Slash" or msg.content == "Dual Sword Attack" or msg.content == "Sliced and Diced"
            print("test2")
            move = msg.content
            dmg = attacks[class_value_starter[0]][move][class_evaluation_starter]
            print(dmg)
          else:
             await interaction.user.send("That is not an executable move. Try again.")
# The message to be awaited from the user will be implemented in the final version of this bot.
    
    elif class_value_starter[0] == 2: # If the class of the starter is the archer.
      await archer_battle.battle_embd(interaction, member, switch)
      check_deleted = None
      try: 
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        async with aiosqlite.connect("main.db") as db:                  
          async with db.cursor() as cursor:
            await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
            check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
        if check_deleted == None:
          return
        else: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,)) 
            await db.commit()  
          return
        if msg.content == "Weak Arrow" or msg.content == "Piercing Shot" or msg.content == "Triple Shot" or msg.content == "Make it Rain":
          move = msg.content
          dmg = attacks[class_value_starter[0]][move][class_evaluation_starter]
    elif class_value_starter[0] == 3: # If the class of the starter is the mage.
      await mage_battle.battle_embd(interaction, member, switch)
      check_deleted = None
      try: 
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
        print(msg.content)
      except asyncio.TimeoutError:
        async with aiosqlite.connect("main.db") as db:                  
          async with db.cursor() as cursor:
            await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
            check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
        if check_deleted == None:
          return
        else: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,)) 
            await db.commit()
          return
      if msg.content == "Zap" or msg.content == "Fireball" or msg.content == "Arcane Mania" or msg.content == "Biden Blast":
        move = msg.content
        dmg = attacks[class_value_starter[0]][move][class_evaluation_starter]
    switch = True
  elif switch == True: # Else if it's the reciever's turn.
    if class_value_reciever[0] == 1: # If the class of the reciever is the knight.
      await knight_battle.battle_embd(interaction, member, switch)
      check_deleted = None
      try: 
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == member.id)
        print(msg.content)
      except asyncio.TimeoutError:
        async with aiosqlite.connect("main.db") as db:                  
          async with db.cursor() as cursor:
            await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,))
            check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
        if check_deleted == None:
          return
        else: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,)) 
            await db.commit()  
          return
        
      if msg.content == "Sword Jab" or msg.content == "Sword Slash" or msg.content == "Dual Sword Attack" or msg.content == "Sliced and Diced":
        move = msg.content
        dmg = attacks[class_value_reciever[0]][move][class_evaluation_reciever]
    elif class_value_reciever[0] == 2: # If the class of the reciever is the archer.
      await archer_battle.battle_embd(interaction, member, switch)
      check_deleted = None
      dmg = None
      while dmg == None:
        await interaction.followup.send(f"Pick from the avaliable moves {member.mention}!")
        try: 
          msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == member.id)  
        except asyncio.TimeoutError:
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,))
              check_deleted = await cursor.fetchone() # Check if /ff was used. 
            await db.commit()
          if check_deleted == None:
            return
          else: 
            await interaction.followup.send("Request timed out...Ending battle.")
            async with aiosqlite.connect("main.db") as db:                  
              async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,)) 
              await db.commit()  
              return
            
        if msg.content == "yes": # msg.content == "Weak Arrow" or msg.content == "Piercing Shot" or msg.content == "Triple Shot" or msg.content == "Make it Rain"
          print("test2")
          move = msg.content
          dmg = attacks[class_value_reciever[0]][move][class_evaluation_reciever]
          print(dmg)
        else:
          await interaction.user.send("That is not an executable move. Try again.")
    elif class_value_reciever[0] == 3: 
      # If the class of the reciever is the mage.
        await mage_battle.battle_embd(interaction, member, switch)
        check_deleted = None
        try: 
          msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == member.id)
        except asyncio.TimeoutError:
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,))
              check_deleted = await cursor.fetchone() # Check if /ff was used. 
            await db.commit()
          if check_deleted == None:
            return
          else: 
            await interaction.followup.send("Request timed out...Ending battle.")
            async with aiosqlite.connect("main.db") as db:                  
              async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,)) 
              await db.commit() 
            return
        if msg.content == "Zap" or msg.content == "Fireball" or msg.content == "Arcane Mania" or msg.content == "Biden Blast":
          move = msg.content
          dmg = attacks[class_value_reciever[0]][move][class_evaluation_reciever]
        else:
          await member.send("That is not an executable move. Try again.")
    switch = False
  return switch, dmg 
    
      