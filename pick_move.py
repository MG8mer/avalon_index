import nextcord
from nextcord.embeds import Embed
from nextcord import Interaction
import asyncio
import aiosqlite
from battle_embeds import archer_battle
from battle_embeds import mage_battle
from battle_embeds import knight_battle
from nextcord.ext import commands


client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all())

#start_value of 1 is the starter
#start_value of 2 is the reciever

async def move(interaction: Interaction, member: nextcord.Member, start_rand, class_value_starter, class_value_reciever, switch):
  # po this is some good pseudocode ty
  # if start_rand == 1
  # switch = False
  # if not switch:
  #   check starter class:
  #     send specific embed from respective py files:
  #       get response and return the move
  #       flip value of switch to opposite
  # else:
  #   check reciever class:
  #     send specific embed from respective py files:
  #       get response and return the move
  #       flip value of switch to opposite

  
  if switch == None:
    if start_rand == 1:
      switch = False
    elif start_rand == 2:
      switch = True

  if switch == False:
    if class_value_starter[0] == 1:
      await knight_battle.battle_embd(interaction, member, switch)
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        await interaction.followup.send("Request timed out...Ending battle.")
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,))
          await db.commit()
      return      
    elif class_value_starter[0] == 2:
      await archer_battle.battle_embd(interaction, member, switch)
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        await interaction.followup.send("Request timed out...Ending battle.")
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,))
          await db.commit()
        return      
    else:
      await mage_battle.battle_embd(interaction, member, switch)
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        await interaction.followup.send("Request timed out...Ending battle.")
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,))
          await db.commit()
        return      
    switch = True
  elif switch == True:
    if class_value_reciever[0] == 1:
      await knight_battle.battle_embd(interaction, member, switch)
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        await interaction.followup.send("Request timed out...Ending battle.")
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,))
          await db.commit()
        return      
    elif class_value_reciever[0] == 2:
      await archer_battle.battle_embd(interaction, member, switch)
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        await interaction.followup.send("Request timed out...Ending battle.")
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,))
          await db.commit()
        return      
    else:
      await mage_battle.battle_embd(interaction, member, switch)
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == interaction.user.id)
      except asyncio.TimeoutError:
        await interaction.followup.send_message("Request timed out...Ending battle.")
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (member.id,))
          await db.commit()
        return      
    switch = False
  return switch
    
      