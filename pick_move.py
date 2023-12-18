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

#start_value of 1 is the starter
#start_value of 2 is the reciever

# Move function that returns what turn it is, taking the arguments interaction for who used battle, member for whor ecieved battle, start_rand for who starts in the battle, the class of the starter, and the class of the reciever.

async def move(interaction: Interaction, member: nextcord.Member, start_rand, class_value_starter, class_value_reciever, switch):
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
      # Sample Explanation (applicable for rest)
        try: # Try awaiting for a message from the user's turn.
          msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
        except asyncio.TimeoutError:
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
              check_deleted = await cursor.fetchone() # Check if /ff was used. 
            await db.commit()
          if check_deleted == None: # If it was, simply return and send nothing.
            return
          else: 
            await interaction.followup.send("Request timed out...Ending battle.")
            async with aiosqlite.connect("main.db") as db:                  
              async with db.cursor() as cursor:
                await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (interaction.user.id,)) # If it times out after 60 seconds and /ff was not used, send a message saying the request timed out, delete the row for the starter and reciever in the battles table, ending the battle. 
              await db.commit()    
# The message to be awaited from the user will be implemented in the final version of this bot.
    elif class_value_starter[0] == 2: # If the class of the starter is the archer.
      await archer_battle.battle_embd(interaction, member, switch)
      check_deleted = None
      try: 
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        async with aiosqlite.connect("main.db") as db:                  
          async with db.cursor() as cursor:
            await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
            check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
        if check_deleted == None:
          return
        else: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (interaction.user.id,)) 
            await db.commit()    
    else: # If the class of the starter is the mage.
      await mage_battle.battle_embd(interaction, member, switch)
      check_deleted = None
      try: 
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        async with aiosqlite.connect("main.db") as db:                  
          async with db.cursor() as cursor:
            await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
            check_deleted = await cursor.fetchone() # Check if /ff was used. 
          await db.commit()
        if check_deleted == None:
          return
        else: 
          await interaction.followup.send("Request timed out...Ending battle.")
          async with aiosqlite.connect("main.db") as db:                  
            async with db.cursor() as cursor:
              await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (interaction.user.id,)) 
            await db.commit()        
    switch = True
  elif switch == True: # Else if it's the reciever's turn.
    if class_value_reciever[0] == 1: # If the class of the reciever is the knight.
      await knight_battle.battle_embd(interaction, member, switch)
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
    elif class_value_reciever[0] == 2: # If the class of the reciever is the archer.
      await archer_battle.battle_embd(interaction, member, switch)
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
    else: # If the class of the reciever is the mage.
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
    switch = False
  return switch 
    
      