"""Resources:
Multiline comments:
https://www.geeksforgeeks.org/multiline-comments-in-python
Initialzing Discord Bot From Replit's article:
https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
https://www.youtube.com/playlist?list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP

Database Resources:
https://datacarpentry.org/python-ecology-lesson/instructor/09-working-with-sql.html, https://www.w3schools.com/sql/sql_select.aspm, https://www.w3schools.com/sql/sql_where.asp, and https://www.w3schools.com/sql/sql_insert.asp
https://www.w3schools.com/sql/sql_delete.asp
https://www.w3schools.com/sql/sql_update.asp
https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
"""

# https://infosecwriteups.com/running-discord-bots-24-7-for-free-with-replit-and-uptime-robot-43caebb0cb60 <----- IMPORTANT


# Database connect along with cursor method and database commit method all throughout main.py from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik

import os
import requests
from pprint import pprint
from nextcord import Interaction # from https://www.youtube.com/watch?v=zvVziW2qS-0&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=17&t=558s&ab_channel=JamesS
import nextcord # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
import asyncio # from https://docs.python.org/3/library/asyncio.html
import aiosqlite # from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
from nextcord.application_command import ClientCog, SlashOption # from https://www.youtube.com/watch?v=gtSbqUJLpvM&t=238s&ab_channel=Civo
from nextcord.embeds import Embed # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext import commands # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext.commands import context    #from https://docs.replit.com/tutorialsb/python/build-basic-discord-bot- python and # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
# import wavelink
import about_archer
import about_knight
import about_mage
import help_page
import pick_move
import help_pageTWO
import start_page
import battle_command
from randGIF import randgif
import random
from random import randint

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all())   #from https://youtu.be/ksAtGCFxrP8#si=A89Nokdcqfsy_tGZ
client.remove_command('help') # Removing the built in help command 

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
  
@client.slash_command(name = "gif", description = "Generate a GIF! Idek why we have this feature its just there.") 
async def gif(interaction: Interaction, query: str = SlashOption(description="Search for the GIF that you want to generate!")): #prefix command to grab gif based on arg
  media_filter = "gif, tinygif"
  random = True
  SECRET_KEY = os.environ["TENOR_API_KEY"]
  ckey = "my_client_key"
  lim = 1
  
  try:
    r = requests.get(
      f"https://tenor.googleapis.com/v2/search?q={query}&key={SECRET_KEY}&client_key={ckey}&limit={lim}&media_filter={media_filter}&random={random}") #requests api for an obj containing our results
    r.raise_for_status()
  except requests.exceptions.RequestException as e:
    await ctx.send("Error fetching GIF. Please try again later.")
    return

  if r.status_code == 200:
    data = r.json()
    url = data['results'][0]['media_formats']['gif']['url'] #opens the json obj and grabs the gif url
    embed = Embed(title="The GIF Machine", 
                  description=f"Here's your GIF! {interaction.user.mention}", 
                  color=0x00ff00)
    embed.set_image(url=f"{url}")
    embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/qY14QUB9KPYAAAAi/tenor-stickers.gif")
    await interaction.response.send_message(embed=embed) #sends the gif and deletes the user msg to not clutter the chat
  else:
    embed = Embed(title="No Results Found")
    await interaction.response.send_message(embed=embed)
    
@client.event
async def on_ready(): # from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
  print("Bot is up") #prints when bot is online from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
  # Table creation from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, guild_id INTEGER, class INTEGER, start INTEGER)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS battles(battle INTEGER, starter_id INTEGER, starter_hp INTEGER, starter_ff STRING, reciever_id INTEGER, reciever_hp INTEGER, reciever_ff STRING, channel_id INTEGER, evaluation_starter STRING, evaluation_reciever STRING)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS moves(user_id INTEGER, opponent_id INTEGER, move_used STRING, turn_num INTEGER)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS cooldowns(user_id INTEGER, opponent_id INTEGER, weak STRING, w_cooldown INTEGER, normal STRING, n_cooldown INTEGER, special STRING, s_cooldown INTEGER, avalon_blessing STRING, ab_cooldown INTEGER)')
    await db.commit()
  url = randgif("cat")
  print(f"{len(client.guilds)}")
  for i in range(len(client.guilds)):
     print(f"{client.guilds[i].name}")
     print(f"{client.guilds[i].member_count}")

@client.slash_command(name = "help", description = "Are you confused?") #slash command to print out help pages
async def help(interaction: Interaction, number: int = SlashOption(name="page", choices={"#1": 1, "#2": 2})):
    botName = client.user.name
    bot_avatar_url = client.user.avatar.url
    if number == 1: 
        await help_page.help(interaction, botName, bot_avatar_url)
    elif number == 2: 
        await help_pageTWO.help(interaction, botName, bot_avatar_url)

# The start command essentially starts the game for the user that uses the command and allows them to use commands such as stats, battle, pick, and so on. It does this by creating a new section in the users table and setting the start value column to one. Additionally, the other functions rely on this value by checking if the start value is one, or in other words if the user used the start command, if the user did not use the command, the user won't be able to use the other functions. Additionally, if the user already used start, the command will not work by checking the start value. The command also sends an embed explaining the game and hot to get started.
# Start command implementation code from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik

@client.slash_command(name = "start", description = "Starts the game!")
async def start(interaction: Interaction): 
  botName = client.user.name
  bot_avatar_url = client.user.avatar.url
  
  start_value, check_battle_one, check_battle_two, user_count = await start_page.check_assign(interaction)
  
  if check_battle_one == (1,) or check_battle_two == (1,) or check_battle_one == (0,) or check_battle_two == (0,):
      await interaction.response.send_message("Cannot start the game when you're in a battle or are requesting/being requested for one! Wait until the battle ends or flee the battle when possible! Or just make a move my guy (if it's your turn in the battle)...")
  elif start_value == (1,):
      await interaction.response.send_message("You have already used /start! If you would like to reset your stats, please use the /reset command.")
  else:
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute('INSERT INTO users (user_id, guild_id, start) VALUES (?, ?, ?)', (interaction.user.id, interaction.guild_id, 1))
      await db.commit()

      
    await start_page.start(interaction, botName, bot_avatar_url)

class ConfirmDeny(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

# The function below creates the "yes" button for the reset function, which is red is color, and what it does is it deletes the row in the table of the user that used /reset, resetting their stats and allowing them to use /reset again. Additinally, after the button is pressed, it cannot be pressed again, as the buttons stop working.
  @nextcord.ui.button(label = 'Yes', style=nextcord.ButtonStyle.green)
  async def y(self, button: nextcord.ui.Button, interaction: Interaction):
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute('DELETE FROM users WHERE user_id = ?', (interaction.user.id,))
        await cursor.execute('DELETE FROM levels WHERE user_id = ?', (interaction.user.id,))
        await interaction.response.send_message('Stats successfully deleted. You may use /start to get started again!', ephemeral=True) # Ephermeral makes the message only visible to the user that used the command.
      await db.commit()
    self.value = True
    self.stop()
    
# The function below creates the "no" button for the reset function, which is red in color. It merely cancels the command by responding to the interaction by sending a message that says the request was cancelled.
  @nextcord.ui.button(label = 'No', style=nextcord.ButtonStyle.red)
  async def n(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.send_message('Request cancelled.', ephemeral=True)
    self.value = False
    self.stop()

# The reset function below implements the ConfirmDeny class created above and ensures to wait for the user to press a button and eventually times out. Additionally, the function checks that start value is one in the users table so that stats can actually be deleted.
@client.slash_command(name = "reset", description = "Reset your stats and start from scratch!")
async def re(interaction: Interaction):
  view = ConfirmDeny()
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
      battle_check_one = await cursor.fetchone()
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
      battle_check_two = await cursor.fetchone()
      if battle_check_one == (1,) or battle_check_two == (1,) or battle_check_one == (0,) or battle_check_two == (0,):
         await interaction.response.send_message("You cannot use /reset during battle! Wait until the battle ends or flee the battle when possible!")
      else:
        await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
        start_value = await cursor.fetchone()
        if start_value == (1,):
           await interaction.response.send_message("Hold up! Once you reset your stats, you cannot go back, are you sure you want to proceed?", view=view, ephemeral=True)
           await view.wait()
        else:
           await interaction.response.send_message("Cannot erase stats that don't exist!", ephemeral=True)
      await db.commit()
  if view.value is None:
    return

# The pick command allows the user to pick the class they will use until they reset their stats, which takes the arguments Knight with a value of one, Archer with a value of 2, and Mage with a value of 3. It ensures first that the start value is 1, or in other words that the user has used start, if so the program continues, and it also checks if the pick command has already been used by checking if the value of the class column is either 1, 2, or 3 for each class respectively. Afterwards, whatever the value of the argument is, function will insert that value into the users table for that user. Additionally, it will send a message notifying the user that they selected their class with the class they chose, dependent on the value of the argument.
@client.slash_command(name = "pick", description = "Pick a class of your choice: Knight, Archer, or Mage!")
async def pck(interaction: Interaction, number: int = SlashOption(name="class", choices={"Knight": 1, "Archer": 2, "Mage": 3})):    
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
      start_value = await cursor.fetchone()
      
      await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
      check_battle_one = await cursor.fetchone()
      
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
      check_battle_two = await cursor.fetchone()
      
      if start_value != (1,):
        await interaction.response.send_message("Cannot pick class when /start has not been used!")
      elif check_battle_one == (1,) or check_battle_two == (1,) or check_battle_one == (0,) or check_battle_two == (0,):
        await interaction.response.send_message("Cannot pick a class during a battle! Wait until the battle ends or flee the battle when possible!")
      else:
        await cursor.execute('SELECT class FROM users WHERE user_id = ?', (interaction.user.id,))
        class_value = await cursor.fetchone()
        if class_value == (1,) or class_value == (2,) or class_value == (3,):
           await interaction.response.send_message("You have already picked a class! To pick a new class, you must reset your stats.")
        else:
          await cursor.execute('UPDATE users SET class = ? WHERE user_id = ?', (number, interaction.user.id))
          if number == 1:
            await interaction.response.send_message("You picked the Knight class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 
          elif number == 2:
            await interaction.response.send_message("You picked the Archer class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 
          elif number == 3:
            await interaction.response.send_message("You picked the Mage class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 
    await db.commit()     


@client.slash_command(name = "battle", description = "Battle an opponent of your choice!")   
# gotten from: https://stackoverflow.com/questions/68646719/discord-py-set-user-id-as-an-
async def battle(interaction: Interaction, member: nextcord.Member):    #.battle command, request battles to other users
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      # Various 'select' queries to check various conditions.
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
      start_value = await cursor.fetchone() # If start has been initialized.
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (interaction.user.id,))
      class_value_initial = await cursor.fetchone() # If the starter has used /pick.
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (member.id,))
      class_value_final = await cursor.fetchone()  # If the reciever has used /pick.
      await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
      check_battle_one = await cursor.fetchone() # If the starter is currently is already in a battle as a starter.
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
      check_battle_two = await cursor.fetchone() # If the starter is currently is already in a battle as a reciever.
      await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (member.id,))
      check_battle_three = await cursor.fetchone() # If the reciever is currently is already in a battle as a starter.
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,))
      check_battle_four = await cursor.fetchone() # If the starter is currently is already in a battle as a reciever.
      await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
      battle_requested = await cursor.fetchone() # To check if the starter has already requested for a battle.
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
      requesting_battle = await cursor.fetchone() # To check if the starter has been requested for a battle.
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (member.id,)) # To check if the reciever has alraeady been requested for a battle.
      requested_battle = await cursor.fetchone()
    await db.commit()
  if start_value != (1,): # Has the user used start?
    await interaction.response.send_message("Please use /start and try again.")
  elif class_value_initial != (1,) and class_value_initial != (2,) and class_value_initial != (3,): # Has the starter picked a class?
    await interaction.response.send_message("Please use /pick and try again.")
  elif battle_requested == (0,) or requesting_battle == (0,): # Has the starter requested or been requested for a battle?
    await interaction.response.send_message("You have already requested or been requested for a battle! Please await for your request to timeout or be accepted/rejected or accept/reject your request to try again.")
  elif check_battle_one == (1,) or check_battle_two == (1,): # Is the user in a battle?
    await interaction.response.send_message("Cannot initiate another battle during a battle! Wait until the battle ends or flee the battle!")
  elif check_battle_three == (1,) or check_battle_four == (1,) or requested_battle == (0,): # Is the reciever in a battle or has been requested for one already?
    await interaction.response.send_message("Cannot battle someone who is already in a battle or has requested for a battle! Try again later.")
  elif member.id == interaction.user.id: # Is the starter attempting to battle himself?
    await interaction.response.send_message("You cannot battle yourself!")
  elif class_value_final != (1,) and class_value_final != (2,) and class_value_final != (3,): # Has the reciever picked a class?
    await interaction.response.send_message("Cannot battle user who has not picked a class!")
  else: # If the conditions have been met and none of the players are in a battle or have requested for one are requesting one, then battle can start being initialized.
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute('INSERT INTO battles (battle, starter_id, starter_ff, reciever_id, reciever_ff, channel_id) VALUES (?, ?, ?, ?, ?, ?)', (0, interaction.user.id, 'N/A', member.id, 'N/A', interaction.channel_id)) # Insert these temporary values, in which 0 as the battle value means both the starter (interaction.user.id), and the reciever (member.id) are in a battle request state. Also, interaction.channel_id ensures that a command such as /ff can only be used in the channel where the battle between these users was started.
      await db.commit()
    await interaction.response.defer()
    await interaction.followup.send(f"Before you fight {member.mention}, they must consent to your worthy request! \n{member.mention}, would you like to fight, {interaction.user.mention}? Respond `yes` or something similar to confirm, respond anything else to cancel.") # Send a message to inform both users of the battle and ask the reciever for their consent to the battle.  
    if battle_requested != (0,): # If the starter has not started a battle request or has been requested for a battle then do what is below.
      # Below from https://www.youtube.com/watch?v=zamNFx3L7oA&t=2s&ab_channel=Dannycademy
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == member.id) # Await for a message from the reciever.
      except asyncio.TimeoutError: # If 60 seconds have passed and the reciever hasn't responded, inform that the reciever took too long to respond and cancel the battle.
        await interaction.followup.send("User took too long to respond. Use /battle to try again.")
      # Above from https://www.youtube.com/watch?v=zamNFx3L7oA&t=2s&ab_channel=Dannycademy
        async with aiosqlite.connect("main.db") as db: # Delete that battle row instance between both users as a result of the cancellation of the battle.
          async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,))
          await db.commit()
          return 
          
      if msg.content == "yes" or msg.content == "Yes" or msg.content == "Yes" or msg.content == "ye" or msg.content == "Yeah" or msg.content == "yeah" or msg.content == "Ye" or msg.content == "sure" or msg.content == "Sure" or msg.content == "ok" or msg.content == "Ok" or msg.content == "Y" or msg.content == "y" or msg.content == "k" or msg.content == "K" or msg.content == "Okay" or msg.content == "okay": # However, if the reciever strictly says "yes", do what is below.
        start_rand = random.choice([1,2]) #currently, we are deciding the person who gets first move by random
        await interaction.followup.send("Starting battle...") # Inform the users that the battle is starting.
        await battle_command.battle(interaction, member, start_rand) # Call the battle function in the battle_command file and proceed.
      else: # If the reciever responds with anything else, cancel the battle.
        async with aiosqlite.connect("main.db") as db:
          async with db.cursor() as cursor:
            await interaction.followup.send("Battle request cancelled.")
            await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,)) # Delete that battle instance row in the table as a result of the cancellation of the battle.
          await db.commit()
    else:
      return

# The /ff function below for if either the starter or the reciever want to run away.

# Create a class for two buttons (yes and no) like /reset.
class RunStay(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

  # For yes, delete the battle instance as a result of one of the belligerents running away.
  @nextcord.ui.button(label = 'Yes', style=nextcord.ButtonStyle.green) #yes button for ff
  async def y(self, button: nextcord.ui.Button, interaction: Interaction):
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
        battle_check_one = await cursor.fetchone() # Check if the starter is the one who used /ff
        await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
        battle_check_two = await cursor.fetchone() # Check if the reciever is the one who used /ff
        if battle_check_one == (1,) or battle_check_one == (0,): # If the starter used /ff, use their id to delete the battle instance row.
          await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,))
        elif battle_check_two == (1,) or battle_check_two == (0,):  # If the reciever used /ff, use their id to delete the battle instance row.
           await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (interaction.user.id,))
        await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id}")
        await cursor.execute(f"DELETE FROM moves WHERE opponent_id = {interaction.user.id}")
        await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
        await cursor.execute(f"DELETE FROM cooldowns WHERE opponent_id = {interaction.user.id}")
        await interaction.response.send_message(f"{interaction.user.mention} has run away from the battle!", ephemeral=False) # Inform both users that the person who used /ff ranaway from the bottle because ephemeral is false, so everyone sees the message, unlike when ephemeral is true and only the person who performed the interaction sees the message.
      await db.commit()
    self.value = True # Allow for the button to do something.
    self.stop() # After the button is pressed, stop the interaction.

  # TODO
  @nextcord.ui.button(label = 'No', style=nextcord.ButtonStyle.red) #no button for ff
  async def n(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.send_message('The battle continues!', ephemeral=True) # Inform the user that the battle continues.
    self.value = False # This button being pressed will be as though nothing happened.
    self.stop() # After the button is pressed, stop the interaction.

  # TODO
@client.slash_command(name = "ff", description = "Run away from a battle!")
async def ff(interaction: Interaction):    #/ff command which is to stop the battle and flee
  view = RunStay()
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
      battle_check_one = await cursor.fetchone() # Check that the user is in a battle where they are the starter.
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
      battle_check_two = await cursor.fetchone() # Or check that the user is in a battle where they are the reciever.
      await cursor.execute('SELECT channel_id FROM battles WHERE channel_id = ?', (interaction.channel_id,))
      battle_check_three = await cursor.fetchone() # Check that /ff is used in the same channel where /battle was used.
      await cursor.execute('SELECT starter_ff FROM battles WHERE starter_id = ?',(interaction.user.id,))
      ff_check_one = await cursor.fetchone()
      await cursor.execute('SELECT reciever_ff FROM battles WHERE reciever_id = ?', (interaction.user.id,))
      ff_check_two = await cursor.fetchone()
      if battle_check_one == (1,) or battle_check_two == (1,): # If the user is in a battle where he is a starter or reciever and /ff is used in the same channel where /battle was used for that user (i.e the value for its checking isn't none), ask for confirmation with the two buttons with the class in the variable view, in which they can only see this interaction with ephermeral = True, then respond accordingly.
        if ff_check_one == ('Yes',) or ff_check_two == ('Yes',):
          if battle_check_three != None:
            if interaction.channel_id == battle_check_three[0]:
              await interaction.response.send_message("Are you sure you want to flee this battle?", view=view, ephemeral=True)
              await view.wait() # Await for the user to press one of the buttons made by the class RunStay.
          else: # If /ff is used not in the place where /battle was used such as the bot's dms, send that you must use ff in the channel where you used /battle.
             await interaction.response.send_message("Plese flee the battle in the channel where you started the battle.", ephemeral=True)
        else:
          await interaction.response.send_message("Please flee the battle when it is your turn.", ephemeral=True)
      elif battle_check_one == (0,) or battle_check_two == (0,):
         await interaction.response.send_message("Cannot flee the battle when you're not yet in a proper battle state!", ephemeral=True)
      else: # If /ff is used when no battle exists for that user, simply respond only ot that user that you can't runaway from a nonexistent battle, or in other words the voices in your head.
         await interaction.response.send_message("No, you can't runaway from the voices in your head...", ephemeral=True)
    await db.commit()
  if view.value is None: # If the user dosen't press any button after a while, invalidate the interaction.
    return

# The stats command diplays the stats of a user that is mentioned, for now displaying the user's class only. The function checks that the start value is one for the user so stats can be actually displayed for the user. Then the value of the class column for that user is checked to display their class, which is then proceeded to deferring the need to respond to the interaction and then following up by sending the embed for the user's stats, which is for now only their class. If the user has not used the pick function ypet, the class displayed will simply be N/A.
@client.slash_command(name = "stats", description = "Display the stats for any person on the server!")
async def st(interaction: Interaction, member: nextcord.Member):    #.stats command, displays the stats of user's chosen class in an embed
  # member: nextcord.Member arg gotten from https://stackoverflow.com/questions/68646719/discord-py-set-user-id-as-an-argument
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (member.id,))
      start_value = await cursor.fetchone()
      if start_value != (1,):
        await interaction.response.send_message(f"Cannot view stats for {member} that don't exist!")
      else:
        await cursor.execute('SELECT class FROM users WHERE user_id = ?', (member.id,))
        class_value = await cursor.fetchone()
        await cursor.execute('SELECT level FROM levels WHERE user_id = ?', (member.id,))
        level = await cursor.fetchone()
        level_value = None
        if level != None:
           level_value = int(level[0] // 1)
        classing = None
        if class_value != None:
             classing = class_value[0]
             if classing == 1:
               classing = "Knight"
             elif classing == 2:
               classing = "Archer"
             elif classing == 3:
               classing = "Mage"
        embed_st = Embed(   
          title = f"Stats for {member}:", 
          color = nextcord.Color.blue())
        embed_st.add_field(
          name = "Class:",
          value = classing,
        )    
        embed_st.add_field(    
          name="Level:", 
          value=str(level_value),
          inline = False,)
        await interaction.response.defer()
        await interaction.followup.send(embed=embed_st)
    await db.commit()


@client.slash_command(name = "about", description = "Learn more about each class!") #slash command to print out info on the three classes, based on user arg, it will call a function from another py file and send an embed on the corresponding class
async def about(interaction: Interaction, number: int = SlashOption(name = "class", choices = {"Knight": 1, "Archer": 2, "Mage": 3})):
    if number == 1: 
        await (about_knight.about(interaction))
    elif number == 2: 
        await (about_archer.about(interaction))
    elif number == 3: 
        await (about_mage.about(interaction))
      
@client.command()
async def download_db(ctx):
      try:
        await ctx.message.delete()
      except nextcord.errors.Forbidden:
        response = await ctx.send("You do not have permission to use this command.")
        await asyncio.sleep(3)
        await response.delete()
        return
      id = int(os.environ['ID'])
      file = os.environ['FILE']
      guild = int(os.environ['ID_GUILD'])
      if ctx.author.id == id and ctx.guild.id == guild: 
          file_path = file
          if os.path.exists(file_path):
              file = nextcord.File(file_path, filename=file)
              response = await ctx.send("Here's the database file:", file=file)
              await asyncio.sleep(3)
              await response.delete()
          else:
              response = await ctx.send("Database file not found.")
              await asyncio.sleep(3)
              await response.delete()
      else:
          response = await ctx.send("You do not have permission to use this command.")
          await asyncio.sleep(3)
          await response.delete()
    
# Below from https://stackoverflow.com/questions/73488299/how-can-i-import-a-cog-into-my-main-py-file
cog_files = ["levels"]

for file in cog_files:
    client.load_extension(f"cogs.{file}")

# Below from https://docs.replit.com/tutorials/python/build-basic discord-bot-python

my_secret = os.environ['DISCORD_BOT_SECRET'] 
client.run(my_secret)  