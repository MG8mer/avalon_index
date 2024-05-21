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
import asyncpg
from nextcord.application_command import ClientCog, SlashOption # from https://www.youtube.com/watch?v=gtSbqUJLpvM&t=238s&ab_channel=Civo
from nextcord.embeds import Embed # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext import commands # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext.commands import context    #from https://docs.replit.com/tutorialsb/python/build-basic-discord-bot- python and # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext import tasks, commands
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
import logging
import signal

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all())   #from https://youtu.be/ksAtGCFxrP8#si=A89Nokdcqfsy_tGZ
client.remove_command('help') # Removing the built in help command 

db_pool = None
keep_db_alive_task = None

run = "Main"

async def create_db_pool():
  # Function to establish database connection using asyncpg
  if run == "Main":
    global db_pool
    DATABASE_URL = os.environ['DATABASE_URL']
    try:
      db_pool = await asyncpg.create_pool(dsn=DATABASE_URL)
      logging.info("Database pool created successfully.")
    except Exception as e:
      logging.error(f"Error creating database connection pool: {e}")
  elif run == "Alpha":
    ALPHA_HOST=os.environ['ALPHA_HOST']
    ALPHA_PORT=os.environ['ALPHA_PORT']
    ALPHA_DBNAME=os.environ['ALPHA_DBNAME']
    ALPHA_USER=os.environ['ALPHA_USER']
    ALPHA_PASSWORD=os.environ['ALPHA_PASSWORD']
    try:
      db_pool = await asyncpg.create_pool(
        host=ALPHA_HOST,
        database=ALPHA_DBNAME,
        user=ALPHA_USER,
        password=ALPHA_PASSWORD
      )
    except Exception as e:
      logging.error(f"Error creating database connection pool: {e}")

async def ensure_db_pool():
  global db_pool
  if db_pool is None or db_pool._closed:
      logging.warning("Recreating the database pool.")
      await create_db_pool()
      client.db_pool = db_pool

@tasks.loop(minutes=1)
async def keep_db_alive():
    if db_pool is None or db_pool._closed:
        logging.warning("Database pool is not initialized.")
        await ensure_db_pool()
      
    async with db_pool.acquire() as cursor:
        try:
            await cursor.execute('SELECT 1')
            logging.info("Executed keep-alive query successfully.")
        except Exception as e:
            logging.error(f"Keep-alive query failed: {e}")

@client.event
async def on_ready(): # from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
    print("Bot is up.") #prints when bot is online from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
    global db_pool
    await create_db_pool()
    client.db_pool = db_pool
    client.load_extension('cogs.levels')
    async with db_pool.acquire() as cursor:
      await cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id BIGINT, guild_id BIGINT, class INTEGER, start INTEGER)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS battles(battle INTEGER, starter_id BIGINT, starter_hp INTEGER, reciever_id BIGINT, reciever_hp INTEGER, evaluation_starter TEXT, evaluation_reciever TEXT)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS moves(user_id BIGINT, opponent_id BIGINT, move_used TEXT, turn_num INTEGER)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS cooldowns(user_id BIGINT, opponent_id BIGINT, weak TEXT, w_cooldown INTEGER, normal TEXT, n_cooldown INTEGER, special TEXT, s_cooldown INTEGER, avalon_blessing TEXT, ab_cooldown INTEGER)') 
      
    if not keep_db_alive.is_running():
       keep_db_alive.start()
    keep_db_alive_task = keep_db_alive
    

    url = randgif("cat")
    print(f"{len(client.guilds)}")
    for i in range(len(client.guilds)):
       print(f"{client.guilds[i].name}")
       print(f"{client.guilds[i].member_count}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

async def close_pool():
  global db_pool
  global keep_db_alive_task
  if db_pool is not None:
    print("Closing connection pools...")
    await db_pool.close()
    db_pool = None 
  else:
    print("No connection pools to close.")

  if keep_db_alive_task is not None:
    keep_db_alive_task.cancel()
    try:
        await keep_db_alive_task
    except asyncio.CancelledError:
        pass

async def shutdown():
  global keep_db_alive_task
  print("Shutting down gracefully...")
  if keep_db_alive_task is not None:
      keep_db_alive_task.cancel()
      try:
          await keep_db_alive_task
      except asyncio.CancelledError:
          pass
  
  if db_pool is not None:
      print("Closing connection pools...")
      await db_pool.close()
      db_pool = None 
    
  await client.close()
  print("Bot has shut down.")

def handle_shutdowns():
  signals = (signal.SIGINT, signal.SIGTERM)
  for s in signals:
      client.loop.add_signal_handler(s, lambda: asyncio.create_task(shutdown()))

@client.command()
async def shutdown(ctx):
  try:
    await ctx.message.delete()
  except nextcord.errors.Forbidden:
    print("User does not have permissions to access command.")
    return
  id = int(os.environ['ID'])
  file = os.environ['FILE']
  guild = int(os.environ['ID_GUILD'])
  if ctx.author.id == id and ctx.guild.id == guild:
      print("Starting closure...")
      await close_pool()
      print("Shutting down bot...")
      await client.http.close()
      await client.close()
  else:
      print("User does not have permissions to access command.")

@client.slash_command(name = "playercount", description = "See how many users are registered with the bot!")
async def count(interaction: Interaction):
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:
      user_data = await cursor.fetch('SELECT start FROM users')
      class_data = await cursor.fetch('SELECT class FROM users')
      user_count = 0 
      if user_data != None: 
        for data in user_data:
          user_count += 1

      class_count = 0
      if class_data != None: 
        for data in class_data:
          if data['class'] in [1, 2, 3]:
            class_count += 1
      await interaction.followup.send(f"User Count: **__{user_count}__**\n \n Users that Picked a Class: **__{class_count}__** \n \n **__Summary__**: \n \n **__{user_count}__** player(s) have used `/start` and **__{class_count}__** of them have picked a class!")

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
  await interaction.response.defer()
  global db_pool
  botName = client.user.name
  bot_avatar_url = client.user.avatar.url

  start_value, check_battle_one, check_battle_two, user_count = await start_page.check_assign(interaction, db_pool)

  if check_battle_one == 1 or check_battle_two == 1 or check_battle_one == 0 or check_battle_two == 0:
      await interaction.followup.send("Cannot start the game when you're in a battle or are requesting/being requested for one! Wait until the battle ends or forfeit the battle when possible! Or just make a move my guy (if it's your turn in the battle)...")
  elif start_value == 1:
      await interaction.followup.send("You have already used /start! If you would like to reset your stats, please use the /reset command.")
  else:
    async with db_pool.acquire() as cursor:

      await cursor.execute('INSERT INTO users (user_id, guild_id, start) VALUES ($1, $2, $3)', interaction.user.id, interaction.guild_id, 1)

    await start_page.start(interaction, botName, bot_avatar_url, db_pool)

class ConfirmDeny(nextcord.ui.View):
  def __init__(self, interaction_id):
    super().__init__(timeout=30)
    self.interaction_id = interaction_id
    self.value = None

# The function below creates the "yes" button for the reset function, which is red is color, and what it does is it deletes the row in the table of the user that used /reset, resetting their stats and allowing them to use /reset again. Additinally, after the button is pressed, it cannot be pressed again, as the buttons stop working.
  @nextcord.ui.button(label = 'Yes', style=nextcord.ButtonStyle.green)
  async def y(self, button: nextcord.ui.Button, interaction: Interaction):
      if interaction.user.id != self.interaction_id:
          await interaction.response.send_message("You can't reset stats that aren't yours!", ephemeral=True)
      else:
        await interaction.response.defer()
        async with db_pool.acquire() as cursor:

          await cursor.execute('DELETE FROM users WHERE user_id = $1', interaction.user.id)
          await cursor.execute('DELETE FROM levels WHERE user_id = $1', interaction.user.id)

        await interaction.followup.send('Stats successfully deleted. You may use /start to get started again!', ephemeral=True) # Ephermeral makes the message only visible to the user that used the command.
        self.value = True
        self.stop()

# The function below creates the "no" button for the reset function, which is red in color. It merely cancels the command by responding to the interaction by sending a message that says the request was cancelled.
  @nextcord.ui.button(label = 'No', style=nextcord.ButtonStyle.red)
  async def n(self, button: nextcord.ui.Button, interaction: Interaction):
    if interaction.user.id != self.interaction_id:
        await interaction.response.send_message("You can't reset stats that aren't yours!", ephemeral=True)
    else:
      await interaction.response.send_message('Request cancelled.', ephemeral=True)
      self.value = False
      self.stop()

# The reset function below implements the ConfirmDeny class created above and ensures to wait for the user to press a button and eventually times out. Additionally, the function checks that start value is one in the users table so that stats can actually be deleted.
@client.slash_command(name = "reset", description = "Reset your stats and start from scratch!")
async def re(interaction: Interaction):
  await interaction.response.defer()
  view = ConfirmDeny(interaction.user.id)
  async with db_pool.acquire() as cursor:

    battle_check_one = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)
    battle_check_two = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)
    if battle_check_one == 1 or battle_check_two == 1 or battle_check_one == 0 or battle_check_two == 0:
        await interaction.follouwp.send("You cannot use /reset during battle! Wait until the battle ends or forfeit the battle when possible!", ephemeral=True)
    else:
        start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', interaction.user.id)
        if start_value == 1:
            await interaction.followup.send("Hold up! Once you reset your stats, you cannot go back, are you sure you want to proceed?", view=view, ephemeral=True)
            await view.wait()
            if view.value is None:
              await interaction.send("Request timed out.", ephemeral=True)
              return
        else:
            await interaction.followup.send("Cannot erase stats that don't exist!", ephemeral=True)

# The pick command allows the user to pick the class they will use until they reset their stats, which takes the arguments Knight with a value of one, Archer with a value of 2, and Mage with a value of 3. It ensures first that the start value is 1, or in other words that the user has used start, if so the program continues, and it also checks if the pick command has already been used by checking if the value of the class column is either 1, 2, or 3 for each class respectively. Afterwards, whatever the value of the argument is, function will insert that value into the users table for that user. Additionally, it will send a message notifying the user that they selected their class with the class they chose, dependent on the value of the argument.
@client.slash_command(name = "pick", description = "Pick a class of your choice: Knight, Archer, or Mage!")
async def pck(interaction: Interaction, number: int = SlashOption(name="class", choices={"Knight": 1, "Archer": 2, "Mage": 3})):  
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:

      start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', interaction.user.id)

      check_battle_one = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)

      check_battle_two = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)

      if start_value != 1:
        await interaction.followup.send("Cannot pick class when /start has not been used!")
      elif check_battle_one == 1 or check_battle_two == 1 or check_battle_one == 0 or check_battle_two == 0:
        await interaction.followup.send("Cannot pick a class during a battle! Wait until the battle ends or forfeit the battle when possible!")
      else:
        class_value = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', interaction.user.id)
        if class_value == 1 or class_value == 2 or class_value == 3:
           await interaction.followup.send("You have already picked a class! To pick a new class, you must reset your stats.")
        else:
          await cursor.execute('UPDATE users SET class = $1 WHERE user_id = $2', number, interaction.user.id)
          if number == 1:
            await interaction.followup.send("You picked the Knight class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 
          elif number == 2:
            await interaction.followup.send("You picked the Archer class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 
          elif number == 3:
            await interaction.followup.send("You picked the Mage class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 


@client.slash_command(name = "battle", description = "Battle an opponent of your choice!")   
# gotten from: https://stackoverflow.com/questions/68646719/discord-py-set-user-id-as-an-
async def battle(interaction: Interaction, member: nextcord.Member):    #.battle command, request battles to other users
  global db_pool
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:

    # Various 'select' queries to check various conditions.
    start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', interaction.user.id)
    class_value_initial = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', interaction.user.id)
    class_value_final = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', member.id)
    check_battle_one = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)
    check_battle_two = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)
    check_battle_three = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', member.id)
    check_battle_four = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', member.id)
    battle_requested = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)
    requesting_battle = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)
    requested_battle =  await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', member.id) # To check if the reciever has alraeady been requested for a battle.

  if start_value != 1: # Has the user used start?
    await interaction.followup.send("Please use /start and try again.")
  elif class_value_initial != 1 and class_value_initial != 2 and class_value_initial != 3: # Has the starter picked a class?
    await interaction.followup.send("Please use /pick and try again.")
  elif battle_requested == 0 or requesting_battle == 0: # Has the starter requested or been requested for a battle?
    await interaction.followup.send("You have already requested or been requested for a battle! Please await for your request to timeout or be accepted/rejected or accept/reject your request to try again.")
  elif check_battle_one == 1 or check_battle_two == 1: # Is the user in a battle?
    await interaction.followup.send("Cannot initiate another battle during a battle! Wait until the battle ends or forfeit the battle!")
  elif check_battle_three == 1 or check_battle_four == 1 or requested_battle == 0: # Is the reciever in a battle or has been requested for one already?
    await interaction.followup.send("Cannot battle someone who is already in a battle or has requested for a battle! Try again later.")
  elif member.id == interaction.user.id: # Is the starter attempting to battle himself?
    await interaction.followup.send("You cannot battle yourself!")
  elif class_value_final != 1 and class_value_final != 2 and class_value_final != 3: # Has the reciever picked a class?
    await interaction.followup.send("Cannot battle user who has not picked a class!")
  else: # If the conditions have been met and none of the players are in a battle or have requested for one are requesting one, then battle can start being initialized.
    async with db_pool.acquire() as cursor:

      await cursor.execute('INSERT INTO battles (battle, starter_id, reciever_id) VALUES ($1, $2, $3)', 0, interaction.user.id, member.id) # Insert these temporary values, in which 0 as the battle value means both the starter (interaction.user.id), and the reciever (member.id) are in a battle request state. Also, interaction.channel_id ensures that a command such as /ff can only be used in the channel where the battle between these users was started.

    await interaction.followup.send(f"Before you fight {member.mention}, they must consent to your worthy request! \n {member.mention}, would you like to fight, {interaction.user.mention}? Respond `yes` or something similar to confirm, respond anything else to cancel.") # Send a message to inform both users of the battle and ask the reciever for their consent to the battle.  
    if battle_requested != 0: # If the starter has not started a battle request or has been requested for a battle then do what is below.
      # Below from https://www.youtube.com/watch?v=zamNFx3L7oA&t=2s&ab_channel=Dannycademy
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == member.id) # Await for a message from the reciever.
      except asyncio.TimeoutError: # If 60 seconds have passed and the reciever hasn't responded, inform that the reciever took too long to respond and cancel the battle.
        await interaction.followup.send("User took too long to respond. Use /battle to try again.")
      # Above from https://www.youtube.com/watch?v=zamNFx3L7oA&t=2s&ab_channel=Dannycademy
        async with db_pool.acquire() as cursor:

          await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id)

        return 

      if msg.content == "yes" or msg.content == "Yes" or msg.content == "Yes" or msg.content == "ye" or msg.content == "Yeah" or msg.content == "yeah" or msg.content == "Ye" or msg.content == "sure" or msg.content == "Sure" or msg.content == "ok" or msg.content == "Ok" or msg.content == "Y" or msg.content == "y" or msg.content == "k" or msg.content == "K" or msg.content == "Okay" or msg.content == "okay": # However, if the reciever strictly says "yes", do what is below.
        start_rand = random.choice([1,2]) #currently, we are deciding the person who gets first move by random
        await interaction.followup.send("Starting battle...") # Inform the users that the battle is starting.
        await battle_command.battle(interaction, member, start_rand, db_pool) # Call the battle function in the battle_command file and proceed.
      else: # If the reciever responds with anything else, cancel the battle.
        async with db_pool.acquire() as cursor:

          await interaction.followup.send("Battle request cancelled.")
          await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id) # Delete that battle instance row in the table as a result of the cancellation of the battle.
    else:
      return

# The stats command diplays the stats of a user that is mentioned, for now displaying the user's class only. The function checks that the start value is one for the user so stats can be actually displayed for the user. Then the value of the class column for that user is checked to display their class, which is then proceeded to deferring the need to respond to the interaction and then following up by sending the embed for the user's stats, which is for now only their class. If the user has not used the pick function ypet, the class displayed will simply be N/A.
@client.slash_command(name = "stats", description = "Display the stats for any person on the server!")
async def st(interaction: Interaction, member: nextcord.Member):    #.stats command, displays the stats of user's chosen class in an embed
  # member: nextcord.Member arg gotten from https://stackoverflow.com/questions/68646719/discord-py-set-user-id-as-an-argument
  async with db_pool.acquire() as cursor:

    start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', member.id)
    if start_value != 1:
        await interaction.response.send_message(f"Cannot view stats for {member} that don't exist!")
    else:
        class_value = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', member.id)
        level = await cursor.fetchval('SELECT level FROM levels WHERE user_id = $1', member.id)
        level_value = None
        if level != None:
          level_value = int(level // 1)
        classing = None
        if class_value != None:
          classing = class_value
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

@client.slash_command(name = "about", description = "Learn more about each class!") #slash command to print out info on the three classes, based on user arg, it will call a function from another py file and send an embed on the corresponding class
async def about(interaction: Interaction, number: int = SlashOption(name = "class", choices = {"Knight": 1, "Archer": 2, "Mage": 3})):
    if number == 1: 
        await (about_knight.about(interaction))
    elif number == 2: 
        await (about_archer.about(interaction))
    elif number == 3: 
        await (about_mage.about(interaction))
  
@client.event
async def on_disconnect():
    print("Double checking connection pools...")
    await close_pool()
    print("Bot shut down successfully!")

# Below from https://docs.replit.com/tutorials/python/build-basic discord-bot-python

if not asyncio.get_event_loop().is_running():
  my_secret = os.environ['DISCORD_BOT_SECRET']
  handle_shutdowns()
  client.run(my_secret)  